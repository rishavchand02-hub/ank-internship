from campaign import TestCampaign
import pandas as pd


def main():
    try:
        campaign = TestCampaign()
        campaign.load_tests()

        summary = campaign.create_summary()
        campaign.save_summary(summary)
        campaign.create_plots(summary)

        averages = summary.groupby("material")[
            ["E_GPa", "yield_MPa", "uts_MPa"]
        ].mean()

        print("\nAverage Mechanical Properties by Material:")
        print(averages.round(2))

    except (FileNotFoundError, pd.errors.ParserError) as error:
        print(f"Could not process file: {error}")
    except Exception as error:
        print(f"Analysis failed: {error}")


if __name__ == "__main__":
    main()
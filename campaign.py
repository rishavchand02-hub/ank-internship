from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from specimen import Specimen, TensileTest


class TestCampaign:

    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)
        self.tests = []

    def load_tests(self):
        metadata = pd.read_csv(self.data_dir / "specimens.csv")

        for _, row in metadata.iterrows():
            specimen = Specimen(
                test_id=row["test_id"],
                material=row["material"],
                area=row["area_mm2"],
                gauge_length=row["gauge_length_mm"]
            )

            file_path = self.data_dir / "raw" / f"{specimen.test_id}.csv"

            test = TensileTest(specimen, file_path)

            test.clean_data()
            test.remove_slack()
            

            self.tests.append(test)
            
    def get_completion_status(self, test_id):
        incomplete_tests = {"test_02", "test_03", "test_26"}
        return test_id not in incomplete_tests 

    def create_summary(self):
        results = []

        for test in self.tests:
            complete = self.get_completion_status(test.specimen.test_id)

            E = test.youngs_modulus()
            yield_strength = test.yield_strength(E)

            if complete:
                uts = test.ultimate_strength()
                fracture_strain = test.fracture_strain()
            else:
                uts = float("nan")
                fracture_strain = float("nan")

            results.append({
                "test_id": test.specimen.test_id,
                "material": test.specimen.material,
                "E_GPa": E,
                "yield_MPa": yield_strength,
                "uts_MPa": uts,
                "fracture_strain": fracture_strain,
                "complete": complete
            })

        return pd.DataFrame(results)    
    
    def save_summary(self, summary):
        output_dir = Path("outputs")
        output_dir.mkdir(exist_ok=True)

        summary.to_csv(output_dir / "summary.csv", index=False)

        print("Summary saved to outputs/summary.csv")   

    def create_plots(self, summary):
        output_dir = Path("outputs")
        output_dir.mkdir(exist_ok=True)

        # Stress-strain curves by material
        for material in summary["material"].unique():
            plt.figure(figsize=(9, 6))

            for test in self.tests:
                if test.specimen.material == material:
                    plt.plot(
                        test.strain,
                        test.stress,
                        label=test.specimen.test_id
                    )

            plt.xlabel("Strain")
            plt.ylabel("Stress (MPa)")
            plt.title(f"Stress-Strain Curves - {material}")
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            plt.savefig(output_dir / f"{material}_stress_strain.png")
            plt.close()

        # Yield strength boxplot
        summary.boxplot(
            column="yield_MPa",
            by="material",
            figsize=(8, 6)
        )

        plt.title("Yield Strength by Material")
        plt.suptitle("")
        plt.xlabel("Material")
        plt.ylabel("Yield Strength (MPa)")
        plt.tight_layout()
        plt.savefig(output_dir / "yield_strength_boxplot.png")
        plt.close()

        print("Plots saved in outputs/")    

    def check_completion(self):
        for test in self.tests:
            force = test.data["force_N"]
            peak_index = force.idxmax()

            final_ratio = force.iloc[-1] / force.max()

            print(
                f"{test.specimen.test_id}: "
                f"peak at {peak_index}/{len(force)-1}, "
                f"final/peak force = {final_ratio:.2f}"
            )
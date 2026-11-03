from campaign import TestCampaign
import matplotlib.pyplot as plt

campaign = TestCampaign()
campaign.load_tests()

summary = campaign.create_summary()
campaign.save_summary(summary)
campaign.create_plots(summary)

print(summary)
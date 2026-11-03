import pandas as pd
from specimen import Specimen, TensileTest

# Load specimen information
specimens = pd.read_csv("data/specimens.csv")

row = specimens.iloc[0]

specimen = Specimen(
    test_id=row["test_id"],
    material=row["material"],
    area=row["area_mm2"],
    gauge_length=row["gauge_length_mm"]
)

# Load tensile test
test = TensileTest(specimen, "data/raw/test_01.csv")

print("Material:", test.specimen.material)
print("Stress (MPa):")
print(test.stress.head())

print("Strain:")
print(test.strain.head())
test = TensileTest(specimen, "data/raw/test_01.csv")
test.clean_data()
print("Rows after cleaning:", len(test.data))
print("Missing values:", test.data.isnull().sum().sum())
print("Duplicate rows:", test.data.duplicated().sum())
import matplotlib.pyplot as plt

plt.plot(test.data["displacement_mm"], test.data["force_N"])

plt.xlabel("Displacement (mm)")
plt.ylabel("Force (N)")
plt.title("Raw Force vs Displacement - test_01")
plt.grid(True)

plt.show()
print(test.data[["displacement_mm", "force_N"]].head(10).to_string(index=False))
test.clean_data()
test.remove_slack()

def remove_spikes(self):
    force_change = self.data["force_N"].diff().abs()

    median_change = force_change.median()
    threshold = 10 * median_change

    spikes = force_change > threshold

    self.data = self.data.loc[~spikes].reset_index(drop=True)

    self.stress = self.data["force_N"] / self.specimen.area
    self.strain = self.data["displacement_mm"] / self.specimen.gauge_length


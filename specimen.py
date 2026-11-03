from dataclasses import dataclass
import pandas as pd
import numpy as np


@dataclass
class Specimen:
    test_id: str
    material: str
    area: float
    gauge_length: float

class TensileTest:

    def __init__(self, specimen, file_path):
        self.specimen = specimen
        self.data = pd.read_csv(file_path)

        # Convert displacement to mm
        if "displacement_m" in self.data.columns:
            self.data["displacement_mm"] = self.data["displacement_m"] * 1000

        elif "displacement_mm" in self.data.columns:
            self.data["displacement_mm"] = self.data["displacement_mm"]

        else:
            raise ValueError("Displacement column not found")

        # Calculate stress and strain
        self.stress = self.data["force_N"] / self.specimen.area
        self.strain = self.data["displacement_mm"] / self.specimen.gauge_length

class TensileTest:

    def __init__(self, specimen, file_path):
        self.specimen = specimen
        self.data = pd.read_csv(file_path)

        if "displacement_m" in self.data.columns:
            self.data["displacement_mm"] = self.data["displacement_m"] * 1000

        elif "displacement_mm" in self.data.columns:
            pass

        else:
            raise ValueError("Displacement column not found")

        self.stress = self.data["force_N"] / self.specimen.area
        self.strain = self.data["displacement_mm"] / self.specimen.gauge_length

    def clean_data(self):
        self.data = self.data.drop_duplicates()
        self.data = self.data.dropna()
        self.data = self.data.reset_index(drop=True)

        self.stress = self.data["force_N"] / self.specimen.area
        self.strain = self.data["displacement_mm"] / self.specimen.gauge_length

    def remove_slack(self):
        start = self.data["force_N"].gt(0).idxmax()

        self.data = self.data.loc[start:].reset_index(drop=True)

        self.stress = self.data["force_N"] / self.specimen.area
        self.strain = self.data["displacement_mm"] / self.specimen.gauge_length  

    def remove_spikes(self):
        force_change = self.data["force_N"].diff().abs()
        median_change = force_change.median()
        threshold = 10 * median_change

        spikes = force_change > threshold
        self.data = self.data.loc[~spikes].reset_index(drop=True)

        self.stress = self.data["force_N"] / self.specimen.area
        self.strain = self.data["displacement_mm"] / self.specimen.gauge_length          

    def youngs_modulus(self):
        elastic = (self.strain >= 0.0005) & (self.strain <= 0.0025)

        slope = np.polyfit(
            self.strain[elastic],
            self.stress[elastic],
            1
        )[0]

        return slope / 1000

    def yield_strength(self, E_GPa):
        E_MPa = E_GPa * 1000
        offset_line = E_MPa * (self.strain - 0.002)

        difference = self.stress - offset_line

        crossing = np.where(difference <= 0)[0]

        if len(crossing) == 0:
            return np.nan

        return self.stress.iloc[crossing[0]]

    def ultimate_strength(self):
        return self.stress.max()

    def fracture_strain(self, complete=True):
        if not complete:
            return np.nan

        return self.strain.iloc[-1]
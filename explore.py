import pandas as pd
import matplotlib.pyplot as plt

for test_id in ["test_02", "test_03", "test_26"]:
    data = pd.read_csv(f"data/raw/{test_id}.csv")

    if "displacement_m" in data.columns:
        displacement = data["displacement_m"] * 1000
    else:
        displacement = data["displacement_mm"]

    plt.figure(figsize=(8, 5))
    plt.plot(displacement, data["force_N"])

    plt.xlabel("Displacement (mm)")
    plt.ylabel("Force (N)")
    plt.title(f"Force vs Displacement - {test_id}")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
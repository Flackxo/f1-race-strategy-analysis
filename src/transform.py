import json
import pandas as pd
from pathlib import Path


RAW_DATA_DIR = Path("data/raw")


def load_json(filename):
    file_path = RAW_DATA_DIR / filename

    with open(file_path, "r") as file:
        data = json.load(file)

    return pd.DataFrame(data)


# Load raw datasets
drivers_df = load_json("drivers.json")
stints_df = load_json("stints.json")
laps_df = load_json("laps.json")
pit_stops_df = load_json("pit_stops.json")
results_df = load_json("session_result.json")
race_control_df = load_json("race_control.json")


# Inspect datasets
print("Drivers shape:", drivers_df.shape)
print("Stints shape:", stints_df.shape)
print("Laps shape:", laps_df.shape)
print("Pit stops shape:", pit_stops_df.shape)
print("Results shape:", results_df.shape)

print("\nLap columns:")
print(laps_df.columns.tolist())

print("\nFirst 5 lap records:")
print(laps_df.head())

print("\nMissing values in lap data:")
print(laps_df.isna().sum())

print("\nLap duration summary:")
print(laps_df["lap_duration"].describe())

print("\nPit-out laps:")
print(laps_df["is_pit_out_lap"].value_counts(dropna=False))


# Safety Car period
safety_car_laps = [32, 33, 34, 35]


# Identify pit-in laps using the end of every stint
# except each driver's final stint
pit_in_laps = set()

for driver_number, driver_stints in stints_df.groupby("driver_number"):

    driver_stints = driver_stints.sort_values("stint_number")

    for _, stint in driver_stints.iloc[:-1].iterrows():
        pit_in_laps.add(
            (driver_number, stint["lap_end"])
        )


# Create pit-in flag for each lap
laps_df["is_pit_in_lap"] = laps_df.apply(
    lambda row: (
        row["driver_number"],
        row["lap_number"]
    ) in pit_in_laps,
    axis=1
)


# Create clean lap dataset
clean_laps_df = laps_df[
    (laps_df["lap_duration"].notna()) &
    (laps_df["is_pit_out_lap"] == False) &
    (laps_df["is_pit_in_lap"] == False) &
    (~laps_df["lap_number"].isin(safety_car_laps)) &
    (laps_df["lap_number"] != 1)
].copy()


# Inspect cleaned dataset
print("\nOriginal lap records:", len(laps_df))
print("Clean lap records:", len(clean_laps_df))
print("Removed records:", len(laps_df) - len(clean_laps_df))

print("\nSlowest 10 remaining laps:")

print(
    clean_laps_df[
        ["driver_number", "lap_number", "lap_duration"]
    ]
    .sort_values("lap_duration", ascending=False)
    .head(10)
)


# Inspect race control data
print("\nRace control columns:")
print(race_control_df.columns.tolist())

print("\nRace control events:")
print(
    race_control_df[
        ["lap_number", "category", "message"]
    ].to_string(index=False)
)
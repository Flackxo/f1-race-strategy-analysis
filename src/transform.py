import json
import pandas as pd
from pathlib import Path


RAW_DATA_DIR = Path("data/raw")
PROCESSED_DATA_DIR = Path("data/processed")

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


# Add tire/stint information to each clean lap
clean_laps_df["stint_number"] = None
clean_laps_df["compound"] = None
clean_laps_df["tire_age"] = None

for _, stint in stints_df.iterrows():

    driver_number = stint["driver_number"]
    lap_start = stint["lap_start"]
    lap_end = stint["lap_end"]

    matching_laps = (
        (clean_laps_df["driver_number"] == driver_number) &
        (clean_laps_df["lap_number"] >= lap_start) &
        (clean_laps_df["lap_number"] <= lap_end)
    )

    clean_laps_df.loc[matching_laps, "stint_number"] = stint["stint_number"]
    clean_laps_df.loc[matching_laps, "compound"] = stint["compound"]

    clean_laps_df.loc[matching_laps, "tire_age"] = (
        stint["tyre_age_at_start"]
        + clean_laps_df.loc[matching_laps, "lap_number"]
        - lap_start
    )


# Select useful driver information
driver_info_df = drivers_df[
    [
        "driver_number",
        "name_acronym",
        "full_name",
        "team_name"
    ]
]


# Select useful race result information
result_info_df = results_df[
    [
        "driver_number",
        "position",
        "points",
        "dnf",
        "dns",
        "dsq"
    ]
]


# Merge driver information into clean lap data
clean_laps_df = clean_laps_df.merge(
    driver_info_df,
    on="driver_number",
    how="left"
)


# Merge race results into clean lap data
clean_laps_df = clean_laps_df.merge(
    result_info_df,
    on="driver_number",
    how="left"
)


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


print("\nPiastri clean laps with tire data:")

print(
    clean_laps_df[
        clean_laps_df["driver_number"] == 81
    ][
        [
            "lap_number",
            "lap_duration",
            "stint_number",
            "compound",
            "tire_age"
        ]
    ].head(20).to_string(index=False)
)


print("\nDriver columns:")
print(drivers_df.columns.tolist())

print("\nResult columns:")
print(results_df.columns.tolist())


# Inspect enriched final dataset
print("\nFinal enriched lap sample:")

print(
    clean_laps_df[
        [
            "driver_number",
            "name_acronym",
            "full_name",
            "team_name",
            "lap_number",
            "lap_duration",
            "stint_number",
            "compound",
            "tire_age",
            "position",
            "points"
        ]
    ].head(15).to_string(index=False)
)


# Check for missing values after enrichment
print("\nMissing enriched values:")

print(
    clean_laps_df[
        [
            "name_acronym",
            "full_name",
            "team_name",
            "stint_number",
            "compound",
            "tire_age",
            "position"
        ]
    ].isna().sum()
)

print("\nDrivers with missing finishing positions:")

print(
    clean_laps_df[
        clean_laps_df["position"].isna()
    ][
        [
            "driver_number",
            "name_acronym",
            "full_name",
            "position",
            "points",
            "dnf",
            "dns",
            "dsq"
        ]
    ]
    .drop_duplicates()
    .to_string(index=False)
)

print("\nDuplicate driver/lap combinations:")
print(
    clean_laps_df.duplicated(
        subset=["driver_number", "lap_number"]
    ).sum()
)

print("\nCompound counts:")
print(clean_laps_df["compound"].value_counts())

# Create processed data directory if needed
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)


# Export clean lap-level analysis dataset
output_file = PROCESSED_DATA_DIR / "clean_laps.csv"

clean_laps_df.to_csv(
    output_file,
    index=False
)

print(f"\nSaved processed dataset to {output_file}")
print("Final dataset shape:", clean_laps_df.shape)
import json
import requests
from pathlib import Path


SESSION_KEY = 10014

RAW_DATA_DIR = Path("data/raw")


def fetch_data(endpoint):
    url = f"https://api.openf1.org/v1/{endpoint}?session_key={SESSION_KEY}"

    response = requests.get(url)

    response.raise_for_status()

    return response.json()


def save_json(data, filename):
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    file_path = RAW_DATA_DIR / filename

    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

    print(f"Saved {filename}")


endpoints = {
    "drivers": "drivers.json",
    "stints": "stints.json",
    "laps": "laps.json",
    "pit": "pit_stops.json",
    "session_result": "session_result.json",
    "race_control": "race_control.json"
}

for endpoint, filename in endpoints.items():
    data = fetch_data(endpoint)
    save_json(data, filename)
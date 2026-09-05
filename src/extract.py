import requests

session_key = 10014

# Get driver information
drivers_url = f"https://api.openf1.org/v1/drivers?session_key={session_key}"
drivers = requests.get(drivers_url).json()

# Create a lookup:
# driver number -> driver abbreviation
driver_lookup = {}

for driver in drivers:
    driver_lookup[driver["driver_number"]] = driver["name_acronym"]


# Get tire stint information
stints_url = f"https://api.openf1.org/v1/stints?session_key={session_key}"
stints = requests.get(stints_url).json()


# Display each driver's strategy
for stint in stints:
    driver_number = stint["driver_number"]
    driver_name = driver_lookup[driver_number]

    print(
        driver_name,
        "| Stint", stint["stint_number"],
        "|", stint["compound"],
        "| Laps", stint["lap_start"], "-", stint["lap_end"],
        "| Starting tire age:", stint["tyre_age_at_start"]
    )
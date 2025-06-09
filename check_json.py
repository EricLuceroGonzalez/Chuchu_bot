import json
import random
from datetime import datetime, timedelta
import os

# Define the range for random dates
start_date = datetime(2025, 5, 15, 18, 0, 0)  # Start of the interval
end_date = datetime(2025, 7, 15, 18, 0, 0)  # End of the interval

# Set to track used dates
used_dates = set()


def generate_unique_random_date(start, end):
    """Generate a unique random datetime between two datetime objects."""
    while True:
        delta = end - start
        random_days = random.randint(0, delta.days)
        random_date = start + timedelta(days=random_days)
        # Preserve the time (18:00:00)
        random_date = random_date.replace(hour=18, minute=0, second=0)
        # Check if the date is already used
        if random_date.strftime("%Y-%m-%dT%H:%M:%S") not in used_dates:
            used_dates.add(random_date.strftime("%Y-%m-%dT%H:%M:%S"))
            return random_date


def SetDatesToJSON():
    json_path = os.path.join(os.path.dirname(__file__), "frases_chuchu.json")
    print(f"Loading JSON file from {json_path}...")
    # Open and load the JSON file
    with open(json_path, "r") as openfile:
        json_object = json.load(openfile)

    # Check for repeated dates
    seen_dates = set()
    repeated_or_empty_dates = []

    for file in json_object:
        date = file["date"]
        if date == "" or date in seen_dates:
            repeated_or_empty_dates.append(file)
        else:
            seen_dates.add(date)
            used_dates.add(date)

    # Replace repeated or invalid dates with unique random dates
    for file in repeated_or_empty_dates:
        random_date = generate_unique_random_date(start_date, end_date)
        print(
            f"Setting repeated date to random date: {random_date.strftime('%Y-%m-%dT%H:%M:%S')}"
        )
        file["date"] = random_date.strftime("%Y-%m-%dT%H:%M:%S")

    for file in json_object:
        if file["date"] == "2025-00-00T00:00:00":
            print(f"Invalid date found in: {file["text"]}")
            random_date = generate_unique_random_date(start_date, end_date)
            print(
                f"Setting invalid date to random date: {random_date.strftime('%Y-%m-%dT%H:%M:%S')}"
            )
            file["date"] = random_date.strftime("%Y-%m-%dT%H:%M:%S")

    # Save the updated JSON object back to the file
    with open(json_path, "w") as outfile:
        json.dump(json_object, outfile, indent=4)

    print("Dates updated successfully!")


def CheckIfRepeatedDates():
    # Open and load the JSON file
    json_path = os.path.join(os.path.dirname(__file__), "frases_chuchu.json")
    with open(json_path, "r") as openfile:
        json_object = json.load(openfile)
    print("\n\nCheck if repeated:")
    seen_dates = set()
    repeated_dates = []
    for file in json_object:
        date = file["date"]
        if date in seen_dates:
            repeated_dates.append(date)
        else:
            seen_dates.add(date)
    # Output the results
    if repeated_dates:
        print("Repeated dates found:")
        for date in repeated_dates:
            print(date)
    else:
        print("No repeated dates found.")


def CheckAndSortDates():
    # Open and load the JSON file
    json_path = os.path.join(os.path.dirname(__file__), "frases_chuchu.json")
    with open(json_path, "r") as openfile:
        json_object = json.load(openfile)

    # Check for invalid or empty dates
    for file in json_object:
        if "date" not in file or file["date"] == "":
            print(f"Invalid or missing date found in: {file}")
        else:
            try:
                # Validate the date format
                datetime.strptime(file["date"], "%Y-%m-%dT%H:%M:%S")
            except ValueError:
                print(f"Invalid date format in: {file}")

    # Sort the JSON array by the "date" field
    sorted_json = sorted(
        json_object,
        key=lambda x: (
            datetime.strptime(x["date"], "%Y-%m-%dT%H:%M:%S")
            if "date" in x and x["date"]
            else datetime.max
        ),
    )

    # Save the sorted JSON back to the file
    with open(json_path, "w") as outfile:
        json.dump(sorted_json, outfile, indent=4)

    print("Dates checked and sorted successfully!")


# Call the function


# SetDatesToJSON()
CheckIfRepeatedDates()
# CheckAndSortDates()

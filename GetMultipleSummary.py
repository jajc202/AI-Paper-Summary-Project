'''
    File:       GetMultipleSummary.py
    Purpose:    Script to get daily summaries for a number of days (in order to populate the site's database)
'''

# Import dependencies
import json
from datetime import datetime
from DailyPaperSummarizer import DailyPaperSummarizer

# Path to your JSON file
file_path = r"C:\Users\josha\OneDrive\Attachments\Documents\Python\AI Paper Summary Data\DailySummaryData.json"

# Let user specify date ranges to summarise
start_date_str = input("Specify start date (\"YYYY-MM-DD\"): ")
end_date_str = input("Specify end date (\"YYYY-MM-DD\"): ")

# Get datetime from input strings
start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

# Initialize an empty list to store the weekdays
weekdays = []

# Iterate over each day in the date range
current_date = start_date
while current_date <= end_date:
    # Check if the current day is a weekday (0 = Monday, 6 = Sunday)
    if current_date.weekday() < 5:  # 0-4 are weekdays
        weekdays.append(current_date.strftime("%Y-%m-%d"))
    current_date += timedelta(days=1)

# Function to append daily data to the JSON file
def append_multiple_data():
    # Load existing data if the file exists, otherwise create an empty dictionary
    try:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("FILE NOT FOUND: Creating new file...")
        data = {}

    # Loop through weekdays and add summaries to data
    for day in weekdays:
        # Get string of current date
        date_string = day.strftime("%Y-%m-%d")

        # Create instance of DailyPaperSummarizer
        summarizer = DailyPaperSummarizer(date_string)

        # Summarize the day's papers
        summarized_papers = summarizer.summary_output()

        # Append new data to the dictionary
        data[date_string] = summarized_papers

    # Write the updated data back to the JSON file
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    print("New data appended successfully!")

# Run the function
if __name__ == "__main__":
    append_multiple_data()

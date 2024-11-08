'''
    File:       GetDailySummary.py
    Purpose:    Script to be run daily in order to summarise the day's papers
'''

# Import dependencies
import json
from datetime import datetime
from DailyPaperSummarizer import DailyPaperSummarizer

# Path to your JSON file
file_path = 'DailySummaryData.json'

# Function to append daily data to the JSON file
def append_daily_data():
    # Load existing data if the file exists, otherwise create an empty dictionary
    try:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("FILE NOT FOUND: Creating new file...")
        data = {}

    # Get today's date
    today_date = datetime.now().strftime("%Y-%m-%d")

    # Create instance of DailyPaperSummarizer
    summarizer = DailyPaperSummarizer(today_date)

    # Summarize the day's papers
    summarized_papers = summarizer.summary_output()

    # Append new data to the dictionary
    data[today_date] = summarized_papers

    # Write the updated data back to the JSON file
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    print("New data appended successfully!")

# Run the function
if __name__ == "__main__":
    append_daily_data()

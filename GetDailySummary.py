'''
    File:       GetDailySummary.py
    Purpose:    Script to be run daily in order to summarise the day's papers
'''

#--------------------------------------------------------------------------------------------------------------
#   Import dependencies
#--------------------------------------------------------------------------------------------------------------
import json
from datetime import datetime
from DailyPaperSummarizer import DailyPaperSummarizer
import requests

#--------------------------------------------------------------------------------------------------------------
#   Get summaries for today's papers
#--------------------------------------------------------------------------------------------------------------
# Path to your JSON file
data_file_path = r"C:\Users\josha\OneDrive\Attachments\Documents\Python\AI Paper Summary Data\DailySummaryData.json"

# Function to append daily data to the JSON file
def append_daily_data():
    # Load existing data if the file exists, otherwise create an empty dictionary
    try:
        with open(data_file_path, 'r') as json_file:
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
    with open(data_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    print("New data appended successfully!")

# Run the function
if __name__ == "__main__":
    append_daily_data()


#--------------------------------------------------------------------------------------------------------------
#   Push updated data to PythonAnywhere
#--------------------------------------------------------------------------------------------------------------
# Path to your config file
config_file_path = r"C:\Users\josha\OneDrive\Attachments\Documents\Python\AI Paper Summary Data\config.json"

# Store PythonAnywhere API token and username in variables from JSON file
with open(config_file_path, 'r') as file:
    config = json.load(file)
api_token = config['api_token']
username = config['username']
host = 'www.pythonanywhere.com'

# Update the data JSON file at PythonAnywhere using API
with open(data_file_path, 'rb') as file_data:
    response = requests.post(
        f'https://{host}/api/v0/user/{username}/files/path/home/{username}/mysite/data/DailySummaryData.json',
        headers={'Authorization': f'Token {api_token}'},
        files={'content': file_data}
    )

# Display results info
if response.status_code == 200:
    print("File updated successfully.")
elif response.status_code == 201:
    print("WARNING: New data file created. Check files directory.")
else:
    print(f"Failed to upload file. Status code: {response.status_code}")


#--------------------------------------------------------------------------------------------------------------
#   Refresh the site
#--------------------------------------------------------------------------------------------------------------
# Set website domain name
domain_name = 'bitesizeai.pythonanywhere.com'

# Reload website
response = requests.post(
    f'https://{host}/api/v0/user/{username}/webapps/{domain_name}/reload/',
    headers={'Authorization': f'Token {api_token}'}
)

# Display results info
if response.status_code == 200:
    print("Page reloaded successfully.")
else:
    print('Got unexpected status code {}: {!r}'.format(response.status_code, response.content))
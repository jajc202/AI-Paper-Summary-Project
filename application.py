'''
    File:       application.py
    Purpose:    Main engine for the webpage
'''

from flask import Flask, render_template, request, jsonify
import json
from user_agents import parse

app = Flask(__name__)

# Sample data: replace this with your actual dictionary
with open(r"/home/bitesizeai/mysite/data/DailySummaryData.json", 'r') as json_file:
    papers_by_date = json.load(json_file)

# Helper function to get min and max dates
def get_date_range(papers_by_date):
    # Extract the date keys and convert them to date objects
    date_keys = papers_by_date.keys()
    date_objects = [date for date in date_keys]

    # Find the most recent and the oldest dates
    recent_valid_date = max(date_objects)  # Most recent date
    oldest_valid_date = min(date_objects)  # Oldest date

    return recent_valid_date, oldest_valid_date

@app.route('/')
def home():
    user_agent = request.headers.get('User-Agent')
    parsed_user_agent = parse(user_agent)

    # Get the min and max dates
    recent_valid_date, oldest_valid_date = get_date_range(papers_by_date)

    # Check if the user is on a mobile device
    if parsed_user_agent.is_mobile:
        return render_template('mobile_index.html')  # Your mobile-specific template
    else:
        return render_template('index.html')  # Your original desktop template

# Define required keys set
required_keys = {"Summary", "Specific Area of AI", "Key Findings", "Real-World Applications"}

@app.route('/get_papers')
def get_papers():
    selected_date = request.args.get('date')
    if selected_date in papers_by_date:
        papers = papers_by_date[selected_date]

        # Filtering the dictionary for records only with all 4 keys
        papers = {key: value for key, value in papers.items() if isinstance(value[0], dict) and set(value[0].keys()) == required_keys}

        return jsonify(papers)
    else:
        return jsonify({"error": "No papers found for this date"})

if __name__ == '__main__':
        app.run(debug=True, use_reloader=False)  # use_reloader=False to avoid scheduler duplication

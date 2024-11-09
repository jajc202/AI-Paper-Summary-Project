'''
    File:       application.py
    Purpose:    Main engine for the webpage
'''

from flask import Flask, render_template, request, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import json

app = Flask(__name__)

# Sample data: replace this with your actual dictionary
with open(r"C:\Users\josha\OneDrive\Attachments\Documents\Python\AI Paper Summary Data\DailySummaryData.json", 'r') as json_file:
    papers_by_date = json.load(json_file)

# Function to update the content
def update_content():
    # Here you would add your code to fetch or generate new data
    # For now, this is just a placeholder to show content updating logic
    print("Content updated")

@app.route('/')
def home():
    return render_template('index.html')

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
    # Initialize the scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_content, 'interval', days=1)  # Run daily
    scheduler.start()
    
    # Start with an initial update
    update_content()
    
    app.run(debug=True, use_reloader=False)  # use_reloader=False to avoid scheduler duplication

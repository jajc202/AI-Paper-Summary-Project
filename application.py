'''
    File:       application.py
    Purpose:    Main engine for the webpage
'''

from flask import Flask, render_template, request, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
import json

app = Flask(__name__)

# Sample data: replace this with your actual dictionary
with open(r"C:\Users\josha\OneDrive\Attachments\Documents\Python\AI Paper Summary Data\DailySummaryData.json", 'r') as json_file:
    papers_by_date = json.load(json_file)

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
        app.run(debug=True, use_reloader=False)  # use_reloader=False to avoid scheduler duplication

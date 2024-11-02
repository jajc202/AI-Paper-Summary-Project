'''
    File:       app.py
    Purpose:    Main engine for the webpage
'''

from flask import Flask, render_template
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import json

app = Flask(__name__)

# Sample data: replace this with your actual dictionary
with open('summarized_papers.json', 'r') as json_file:
    papers = json.load(json_file)

# Function to update the content
def update_content():
    # Here you would add your code to fetch or generate new data
    # For now, this is just a placeholder to show content updating logic
    print("Content updated")

@app.route('/')
def home():
    return render_template('index.html', papers=papers)

if __name__ == '__main__':
    # Initialize the scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_content, 'interval', days=1)  # Run daily
    scheduler.start()
    
    # Start with an initial update
    update_content()
    
    app.run(debug=True, use_reloader=False)  # use_reloader=False to avoid scheduler duplication

'''
    Module:     paperscraper.py
    Purpose:    To extract the pdfs of all the papers published on a given day
'''

# Import libraries
import requests
from bs4 import BeautifulSoup
import os

# Define base URL for HuggingFace
BASE_URL = "https://huggingface.co"

# Define class
class paperscraper:

    # Initialise the class
    def __init__(self, date):
        self.date = date

        # Define base URL for HuggingFace
        self.BASE_URL = "https://huggingface.co"

    # Define function to get links to all paper webpages
    def get_links(self):
        # Define URL for daily papers for given date
        URL = f"{self.BASE_URL}/papers?date={self.date}"

        # Parse the html from the daily papers page
        response = requests.get(URL)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Initialise dictionary to store links into
        papers = {}

        # Extract links to individual papers using huggingface html structure
        paper_links = soup.find_all('a', class_='line-clamp-3 cursor-pointer text-balance')

        # Loop through papers to store paper_title: url pairs
        for paper in paper_links:
            paper_title = paper.text.strip()        # Get the title of the paper
            paper_page_url = paper['href']          # Get the relative link to the paper's Hugging Face page
            papers[paper_title] = f"{URL}{paper_page_url}"    # Store the title: url pair into dict

        return papers
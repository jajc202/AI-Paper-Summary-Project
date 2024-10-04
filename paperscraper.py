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
class paperscraper(self, date):

    # Initialise the class
    def __init__(self, date):
        self.date = date
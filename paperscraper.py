'''
    Module:     paperscraper.py
    Purpose:    To extract the pdfs of all the papers published on a given day
'''

# Import libraries
import requests
from bs4 import BeautifulSoup
import os
import PyPDF2
import io

# Define class
class PaperScraper:

    # Initialise the class
    def __init__(self, date):
        self.date = date

        # Define base URL for HuggingFace
        self.HF_BASE_URL = "https://huggingface.co"
        self.PDF_BASE_URL = "https://arxiv.org/pdf/"
        self.ARXIV_BASE_URL = "https://arxiv.org/abs/"

    # Define function to get links to all paper pdfs
    def get_links(self):
        # Define URL for daily papers for given date
        URL = f"{self.HF_BASE_URL}/papers?date={self.date}"

        # Parse the html from the daily papers page
        response = requests.get(URL)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Initialise dictionary to store links into
        paper_pdfs = {}

        # Extract links to individual papers using huggingface html structure
        paper_links = soup.find_all('a', class_='line-clamp-3 cursor-pointer text-balance')

        # Loop through papers to store paper_title: url pairs
        for paper in paper_links:
            paper_title = paper.text.strip()                                                    # Get the title of the paper
            paper_page_url = paper['href']                                                      # Get the relative link to the paper's Hugging Face page
            
            # Store the title: [author, url] pair into dict
            paper_pdfs[paper_title] = [
                f"{self.ARXIV_BASE_URL}{paper_page_url.strip('/papers/')}",                     # URL of arxiv page                            
                f"{self.PDF_BASE_URL}{paper_page_url.strip('/papers/')}",                       # URL of pdf
            ]

        return paper_pdfs
    

    # Define function to extract text from pdf link
    def get_pdf_text(self, paper_pdfs):
        # Initialise dictionary to store plain text into
        pdf_texts = {}

        # Loop through each paper
        for paper, (_, url) in paper_pdfs.items():
            try:
                # Send a get request to the pdf url
                response = requests.get(url)

                # Check if the request was successful (status code 200)
                if response.status_code == 200:
                    # Read the PDF content from the response
                    pdf_file = io.BytesIO(response.content)
                    
                    # Define a PyPDF2 reader
                    reader = PyPDF2.PdfReader(pdf_file)

                    # Extract the text
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text() + "\n"  # Adding a newline for separation

                    # Save the text to the output dict
                    pdf_texts[paper] = text
                else:
                    print(f"Failed to download PDF. Status code: {response.status_code}")

            except Exception as e:
                print(f"An error occurred: {e}")

        return pdf_texts
    
    # Define function to get authors of the paper
    def get_authors(self, paper_pdfs):
        # Initialise dictionary to store author names into
        authors = {}

        # Loop through each paper
        for paper, (arxix_url, _) in paper_pdfs.items():
            try:
                # Send a get request to the arxiv url
                response = requests.get(arxix_url)

                # Check if the request was successful (status code 200)
                if response.status_code == 200:
                    # Get html content from arxiv page
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Extract links to individual papers using huggingface html structure
                    author_tags = soup.find_all('a', href=lambda href: href and 'searchtype=author' in href)
                    
                    # Extract and print the author names
                    author_names = [tag.get_text() for tag in author_tags]

                    # Save the authors to the output dict
                    authors[paper] = author_names
                else:
                    print(f"Failed to download arxiv html. Status code: {response.status_code}")

            except Exception as e:
                print(f"An error occurred: {e}")

        return authors
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
class paperscraper:

    # Initialise the class
    def __init__(self, date):
        self.date = date

        # Define base URL for HuggingFace
        self.HF_BASE_URL = "https://huggingface.co"
        self.ARXIV_BASE_URL = "https://arxiv.org/abs/"

    # Define function to get links to arxiv page for all papers
    def get_links(self):
        # Define URL for daily papers for given date
        URL = f"{self.HF_BASE_URL}/papers?date={self.date}"

        # Parse the html from the daily papers page
        response = requests.get(URL)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Initialise dictionary to store links into
        paper_pages = {}

        # Extract links to individual papers using huggingface html structure
        paper_links = soup.find_all('a', class_='line-clamp-3 cursor-pointer text-balance')

        # Loop through papers to store paper_title: url pairs
        for paper in paper_links:
            paper_title = paper.text.strip()                                                    # Get the title of the paper
            paper_page_url = paper['href']                                                      # Get the relative link to the paper's Hugging Face page
            paper_pages[paper_title] = f"{self.ARXIV_BASE_URL}{paper_page_url.strip('/papers/')}"  # Store the title: url pair into dict

        return paper_pages
    
    
    # Define function to extract html link from arxiv link
    def get_html_links(self, paper_pages):
        # Initialise dictionary to store html into
        html_links = {}

        # Loop through each paper
        for paper, url in paper_pages.items():
            try:
                # Send a get request to the arxiv url
                response = requests.get(url)

                # Check if the request was successful (status code 200)
                if response.status_code == 200:
                    # Parse the html from the arxiv page
                    response = requests.get(url)
                    soup = BeautifulSoup(response.content, 'html.parser')

                    # Find the <a> tag with the specific class and id
                    html_class = soup.find('a', class_='abs-button', id='latexml-download-link')

                    # Extract the link from the href attribute
                    html_link = html_class.get('href')

                    html_links[paper] = html_link

                else:
                    print(f"Failed to access arxiv page. Status code: {response.status_code}")

            except Exception as e:
                print(f"An error occurred: {e}")

        return html_links
    

    # Define function to create a dictionary of subheading: content for a html page
    def html_subdivide(self, html_page):
        try:
            # Send a get request to the html url
            response = requests.get(html_page)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Parse the HTML content using BeautifulSoup
                soup = BeautifulSoup(response.content, 'html.parser')

                # Initialize dictionary to hold section titles and their content
                html_divide = {}

                # Find all the headers that represent sections and subsections (h2, h3, etc.)
                # ArXiv HTML pages typically use <h2> for main sections and <h3> for subsections.
                section_tags = soup.find_all(['h2', 'h3', 'h6'])  # Adjust this based on the section hierarchy

                # Iterate through each section header and capture its content
                for tag in section_tags:
                    # Remove any <span> tags inside the header, which usually hold the section numbering
                    for span in tag.find_all('span', class_='ltx_tag'):
                        span.decompose()  # Removes the span tag from the soup

                    # Get the section title without the numbering
                    section_title = tag.get_text(strip=True)
                    
                    # Find the next sibling and extract all the text until the next section header is found
                    section_content = []
                    for sibling in tag.find_next_siblings():
                        if sibling.name in ['h2', 'h3', 'h6']:  # Stop if we reach a new section header
                            break
                        section_content.append(sibling.get_text(strip=True))
                    
                    # Join the content list into a single string and save in the dictionary
                    html_divide[section_title] = ' '.join(section_content)

            else:
                print(f"Failed to access html page. Status code: {response.status_code}")

        except Exception as e:
                print(f"An error occurred: {e}")

        return html_divide
        


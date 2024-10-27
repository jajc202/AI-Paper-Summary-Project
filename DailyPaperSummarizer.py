'''
    Module:     DailyPaperSummarizer.py
    Purpose:    To combine all modules and summarize each paper from a given day
'''

# Import paperscraper and PaperSummary modules
from paperscraper import PaperScraper
from PaperSummary import PaperSummary

class DailyPaperSummarizer:

    # Initialise the class
    def __init__(date, self):
        # Create instance of paperscraper
        self.PaperScraper = PaperScraper(self.date)

        # Create instance of PaperSummary
        self.PaperSummary = PaperSummary()

    # Define function to summarize all papers from the date
    def daily_summary(self):
        # Get dictionary of papers: content using PaperScraper
        paper_links = self.PaperScraper.get_links()
        pdf_dict = self.PaperScraper.get_pdf_text(paper_links)

        # Summarize each paper and save result in dictionary
        summarized_papers = {name: self.PaperSummary(content) for name, content in pdf_dict.items()}
        return summarized_papers

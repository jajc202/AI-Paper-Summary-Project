'''
    Module:     DailyPaperSummarizer.py
    Purpose:    To combine all modules and summarize each paper from a given day
'''

# Import paperscraper and PaperSummary modules
from paperscraper import PaperScraper
from PaperSummary import PaperSummary

# Import re to enable post-processing with regex
import re

class DailyPaperSummarizer:

    # Initialise the class
    def __init__(self, date):
        # Create instance of paperscraper
        self.PaperScraper = PaperScraper(date)

        # Create instance of PaperSummary
        self.PaperSummary = PaperSummary()

    # Define function to summarize all papers from the date (and get links to their pdfs)
    def daily_summary(self):
        # Get dictionary of papers: content using PaperScraper
        paper_links = self.PaperScraper.get_links()
        pdf_dict = self.PaperScraper.get_pdf_text(paper_links)

        # Summarize each paper and save result in dictionary
        summarized_papers = {name: self.PaperSummary.paper_summarizer(content) for name, content in pdf_dict.items()}
        return paper_links, summarized_papers

    # Define function to post-process a summarized paper
    def format_summary(self, summary):
        # Define the section patterns based on keywords
        section_patterns = {
            'Summary': r'\*\*.*summary.*\*\*.*',
            'Specific Area of AI': r'\*\*.*area.*\*\*.*',
            'Key Findings': r'\*\*.*key.*findings.*\*\*.*',
            'Real-World Applications': r'\*\*.*real.*world.*\*\*.*'
        }
        
        # Find all section start points
        pattern = '|'.join(section_patterns.values())
        matches = [(m.group(0), m.start()) for m in re.finditer(pattern, summary, re.IGNORECASE)]
        
        # Sort the matches by their start positions
        matches.sort(key=lambda x: x[1])
        
        # Split the text into sections based on found matches
        sections = {}
        for i, (match, start) in enumerate(matches):
            # Determine end of the current section
            end = matches[i+1][1] if i+1 < len(matches) else len(summary)
            
            # Identify the section name by matching pattern
            for key, pat in section_patterns.items():
                if re.match(pat, match, re.IGNORECASE):
                    sections[key] = summary[start:end].replace(match, '').strip()
                    break

        # Remove any text starting with '**' after the last meaningful section
        if 'Real-World Applications' in sections:
            sections['Real-World Applications'] = re.split(r'\n\n\*\*', sections['Real-World Applications'])[0].strip()

        # Remove any extra * in text and leading whitespace
        sections = {heading: content.replace('*', '').lstrip() for heading, content in sections.items()}

        return sections
    
    # Define function to apply post-processing to each paper to give final output
    def summary_output(self):
        # Call daily_summary to get summarized outputs
        paper_links, summarized_papers = self.daily_summary()

        # Apply post processing to each summary
        # Also save the links to the pdf of each paper
        formatted_output = {
            name: [self.format_summary(summary), paper_links[name]]
            for name, summary in summarized_papers.items()
        }
        return formatted_output

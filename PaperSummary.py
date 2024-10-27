'''
    Module:     papersummarizer.py
    Purpose:    To summarise the text from an academic paper on AI/Machine Learning
'''

# Import Ollama dependencies to for the model
from langchain_ollama import OllamaLLM

class PaperSummary:
    
    # Initialise the class
    def __init__(self):
        # Initialise the model (Llama 3.2 - 1B)
        self.model = OllamaLLM(model="llama3.2:1b")

    # Define function to summarize the text
    def paper_summarizer(self, text):
        # Define prompt
        prompt = f"""
        From this academic paper: {text} 
        Give the following points
            1) A general 3-4 line summary of the paper
            2) The specific area of AI it applies to
            3) The key findings
            4) How the findings can be used in real-world deployment
        """

        # Summarize the text
        summarized_text = chain.invoke(input=prompt)
        return summarized_text
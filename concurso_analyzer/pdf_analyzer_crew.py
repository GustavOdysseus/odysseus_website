from crewai import Agent, Task, Crew, Process
from langchain.tools import Tool, tool
from PyPDF2 import PdfReader
import os
from typing import List



class PdfQuestionExtractor:
    @tool("extract_text_from_pdf")
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from a PDF file.
        
        Args:
            pdf_path (str): Path to the PDF file to extract text from
            
        Returns:
            str: Extracted text from the PDF
        """
        if not os.path.exists(pdf_path):
            return f"Error: File {pdf_path} not found."
        
        try:
            reader = PdfReader(pdf_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            return f"Error extracting text from PDF: {str(e)}"

def create_agents():
    # Create PDF extractor instance
    pdf_extractor = PdfQuestionExtractor()
    
    # PDF Reader Agent
    pdf_reader_agent = Agent(
        role='PDF Question Reader',
        goal='Extract and structure questions from PDF files',
        backstory="""You are an expert at reading and understanding PDF documents 
        containing exam questions. Your expertise lies in identifying individual 
        questions, their components, and organizing them in a clear structure.""",
        tools=[pdf_extractor.extract_text_from_pdf],
        verbose=True
    )
    
    return pdf_reader_agent

def create_tasks(agent, pdf_path: str):
    task = Task(
        description=f"""
        1. Read the PDF file at {pdf_path}
        2. Extract all questions from the document
        3. For each question:
           - Identify the question text
           - Identify any options/alternatives if present
           - Note any special formatting or structure
        4. Organize the questions in a clear, structured format
        5. Return the structured questions
        """,
        agent=agent
    )
    
    return task

def main(pdf_path: str):
    # Create agent
    pdf_reader_agent = create_agents()
    
    # Create task
    pdf_reading_task = create_tasks(pdf_reader_agent, pdf_path)
    
    # Create crew
    crew = Crew(
        agents=[pdf_reader_agent],
        tasks=[pdf_reading_task],
        verbose=2,
        process=Process.sequential
    )
    
    # Start the crew
    result = crew.kickoff()
    
    return result

if __name__ == "__main__":
    # Example usage
    pdf_path = "/Users/gustavomonteiro/Desktop/prova"  # Replace with actual PDF path
    result = main(pdf_path)
    print(result)

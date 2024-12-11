from typing import Optional
from crewai_tools import BaseTool  # Substitua a importação do Langchain Tool
from PyPDF2 import PdfReader
import os
import re
from typing import Dict, List

class PDFQuestionExtractor:
    """Tool for extracting and structuring questions from PDF files."""
    
    def extract_questions(self, pdf_path: str) -> dict:
        """
        Extract questions from a PDF file and return them in a structured format.
        
        Args:
            pdf_path (str): Path to the PDF file
            
        Returns:
            dict: Dictionary containing questions and extraction statistics
        """
        if not os.path.exists(pdf_path):
            return {"error": f"Arquivo {pdf_path} não encontrado."}
        
        try:
            reader = PdfReader(pdf_path)
            questions = []
            question_ids = set()  # Para rastrear IDs únicos
            total_raw_questions = 0
            duplicates = 0
            
            print(f"\nIniciando extração do PDF com {len(reader.pages)} páginas...")
            
            for page_num, page in enumerate(reader.pages, 1):
                text = page.extract_text()
                print(f"Processando página {page_num}/{len(reader.pages)}")
                
                # Procura por questões usando o padrão com código identificador
                question_blocks = re.split(r'\d+\.\s*\[Q\d+\]', text)
                question_ids_found = re.findall(r'\d+\.\s*\[Q(\d+)\]', text)
                
                total_raw_questions += len(question_ids_found)
                
                for i, block in enumerate(question_blocks[1:]):  # Ignora o primeiro split que pode ser vazio
                    if not block.strip():
                        continue
                    
                    question_id = question_ids_found[i]
                    
                    # Verifica se é uma questão duplicada
                    if question_id in question_ids:
                        duplicates += 1
                        continue
                    
                    question_ids.add(question_id)
                    
                    # Estrutura básica da questão
                    question_dict = {
                        "id": question_id,
                        "text": block.strip(),
                        "alternatives": self._extract_alternatives(block),
                        "metadata": {
                            "has_image": self._check_for_images(page),
                            "length": len(block.strip()),
                            "page": page_num
                        }
                    }
                    questions.append(question_dict)
            
            stats = {
                "total_pages": len(reader.pages),
                "total_raw_questions": total_raw_questions,
                "unique_questions": len(questions),
                "duplicates_found": duplicates
            }
            
            print("\nEstatísticas da extração:")
            print(f"Total de páginas processadas: {stats['total_pages']}")
            print(f"Total de questões encontradas: {stats['total_raw_questions']}")
            print(f"Questões únicas: {stats['unique_questions']}")
            print(f"Duplicatas ignoradas: {stats['duplicates_found']}")
            
            return {
                "questions": questions,
                "stats": stats
            }
            
        except Exception as e:
            return {"error": f"Erro ao processar PDF: {str(e)}"}
    
    def _extract_alternatives(self, text: str) -> dict:
        """Extract multiple choice alternatives if they exist."""
        alternatives = {}
        pattern = r'([A-E])\)(.*?)(?=[A-E]\)|$)'
        matches = re.finditer(pattern, text, re.DOTALL)
        
        for match in matches:
            letter = match.group(1)
            content = match.group(2).strip()
            alternatives[letter] = content
            
        return alternatives
    
    def _check_for_images(self, page) -> bool:
        """Check if the page contains any images."""
        return '/XObject' in page['/Resources']

def get_pdf_tool() -> BaseTool:
    """Get the PDF extraction tool."""
    pdf_extractor = PDFQuestionExtractor()
    
    class PDFExtractionTool(BaseTool):
        name: str = "PDF Question Extractor"
        description: str = "Extrai e estrutura questões de arquivos PDF"
        
        def _run(self, pdf_path: str) -> dict:
            return pdf_extractor.extract_questions(pdf_path)
    
    return PDFExtractionTool()

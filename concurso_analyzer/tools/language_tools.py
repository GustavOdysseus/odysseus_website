from typing import Dict, List
import spacy
import nltk
import os
import re
import openai
from dotenv import load_dotenv
from collections import Counter
from crewai_tools import BaseTool  # Substitua a importação do Langchain Tool

class PortugueseAnalyzer:
    """Tool for analyzing Portuguese language aspects in questions."""
    
    def __init__(self):
        # Download necessary NLTK data
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        
        # Load Portuguese language model
        try:
            self.nlp = spacy.load('pt_core_news_sm')
        except OSError:
            # If model is not installed, download it
            os.system('python -m spacy download pt_core_news_sm')
            self.nlp = spacy.load('pt_core_news_sm')
        
        # Carrega variáveis de ambiente
        load_dotenv()
        
        # Configura a chave da API
        openai.api_key = os.getenv('OPENAI_API_KEY')
    
    def analyze_question(self, question_text: str) -> Dict:
        """
        Analyze various aspects of a Portuguese language question.
        
        Args:
            question_text (str): The text of the question to analyze
            
        Returns:
            dict: Analysis results including morphological, syntactic, and other features
        """
        doc = self.nlp(question_text)
        
        # Análise morfológica
        morphological_analysis = {
            "pos_tags": Counter([token.pos_ for token in doc]),
            "word_types": {
                "substantivos": [token.text for token in doc if token.pos_ == "NOUN"],
                "verbos": [token.text for token in doc if token.pos_ == "VERB"],
                "adjetivos": [token.text for token in doc if token.pos_ == "ADJ"],
                "adverbios": [token.text for token in doc if token.pos_ == "ADV"]
            }
        }
        
        # Análise de acentuação
        accentuation = self._analyze_accentuation(question_text)
        
        # Análise sintática
        syntactic_analysis = {
            "sentence_types": self._analyze_sentence_type(doc),
            "dependencies": Counter([token.dep_ for token in doc])
        }
        
        return {
            "morphological": morphological_analysis,
            "accentuation": accentuation,
            "syntactic": syntactic_analysis,
            "main_theme": self._identify_main_theme(doc)
        }
    
    def _analyze_accentuation(self, text: str) -> Dict:
        """Analyze accentuation patterns in the text."""
        accent_patterns = {
            "agudo": len(re.findall('[áéíóú]', text, re.IGNORECASE)),
            "circunflexo": len(re.findall('[âêîôû]', text, re.IGNORECASE)),
            "til": len(re.findall('[ãõ]', text, re.IGNORECASE)),
            "crase": len(re.findall('à', text, re.IGNORECASE))
        }
        return accent_patterns
    
    def _analyze_sentence_type(self, doc) -> str:
        """Identify the type of sentence (declarative, interrogative, etc.)."""
        # Basic implementation - can be enhanced
        text = doc.text
        if "?" in text:
            return "interrogative"
        elif "!" in text:
            return "exclamative"
        else:
            return "declarative"
    
    def _identify_main_theme(self, doc) -> str:
        """
        Identify the main theme using OpenAI's GPT model.
        
        Args:
            doc: spaCy document
        
        Returns:
            str: Identified main theme of the text
        """
        try:
            # Chama a API do OpenAI para identificar o tema
            response = openai.ChatCompletion.create(
                model="gpt-4omini",
                messages=[
                    {"role": "system", "content": "Você é um assistente especializado em identificar o tema principal de um texto."},
                    {"role": "user", "content": f"Qual é o tema principal do seguinte texto? Forneça uma resposta concisa em uma palavra ou frase curta:\n\n{doc.text}"}
                ],
                max_tokens=50
            )
            
            # Extrai o tema da resposta
            theme = response.choices[0].message.content.strip()
            
            return theme if theme else "outros"
        
        except Exception as e:
            print(f"Erro ao identificar tema: {e}")
            return "outros"

def get_language_tool() -> BaseTool:
    """Get the Portuguese language analysis tool."""
    analyzer = PortugueseAnalyzer()
    
    class LanguageAnalysisTool(BaseTool):
        name: str = "Portuguese Language Analyzer"
        description: str = "Analyzes Portuguese language aspects in questions"
        
        def _run(self, question: str) -> dict:
            return analyzer.analyze_question(question)
    
    return LanguageAnalysisTool()
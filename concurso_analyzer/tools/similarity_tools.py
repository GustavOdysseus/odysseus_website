from typing import Dict, List
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from crewai_tools import BaseTool as CrewaiBaseTool  # Substitua a importação do Langchain Tool

class QuestionSimilarityAnalyzer:
    """Tool for analyzing similarity between questions."""
    
    def __init__(self, model_name='paraphrase-MiniLM-L6-v2'):
        """
        Initialize the similarity analyzer with a pre-trained model.
        
        Args:
            model_name (str): Name of the sentence transformer model to use
        """
        self.model = SentenceTransformer(model_name)
    
    def find_similar_questions(self, questions: List[str], threshold: float = 0.7) -> Dict:
        """
        Find similar questions based on semantic similarity.
        
        Args:
            questions (List[str]): List of questions to compare
            threshold (float): Similarity threshold for considering questions similar
            
        Returns:
            Dict: Analysis of question similarities
        """
        if len(questions) < 2:
            return {"error": "Forneça pelo menos duas questões para comparação."}
        
        # Encode questions
        embeddings = self.model.encode(questions)
        
        # Compute cosine similarity
        similarity_matrix = cosine_similarity(embeddings)
        
        # Find similar question pairs
        similar_pairs = []
        for i in range(len(questions)):
            for j in range(i+1, len(questions)):
                if similarity_matrix[i][j] >= threshold:
                    similar_pairs.append({
                        "question1": questions[i],
                        "question2": questions[j],
                        "similarity_score": float(similarity_matrix[i][j])
                    })
        
        return {
            "total_questions": len(questions),
            "similar_pairs": similar_pairs,
            "avg_similarity": float(np.mean(similarity_matrix[np.triu_indices(len(questions), k=1)]))
        }

class SimilarityAnalysisTool(CrewaiBaseTool):
    name: str = "Question Similarity Analyzer"
    description: str = "Analyzes similarity between questions and identifies patterns"
    
    def __init__(self):
        self.analyzer = QuestionSimilarityAnalyzer()
    
    def _run(self, questions: List[str]) -> dict:
        return self.analyzer.find_similar_questions(questions)

def get_similarity_tool() -> CrewaiBaseTool:
    """Get the question similarity analysis tool."""
    return SimilarityAnalysisTool()
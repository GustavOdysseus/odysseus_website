from typing import List, Dict
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import json
import os
from crewai_tools import BaseTool

class QuestionStatisticsGenerator:
    """Tool for generating statistics about exam questions."""
    
    def __init__(self):
        self.output_dir = "statistics_output"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_statistics(self, questions: List[Dict], exam_name: str) -> Dict:
        """
        Generate comprehensive statistics about the questions.
        
        Args:
            questions (List[Dict]): List of analyzed questions with their properties
            exam_name (str): Name of the exam for output files
            
        Returns:
            Dict: Statistical analysis results
        """
        # Convert questions to DataFrame for easier analysis
        df = pd.DataFrame(questions)
        
        # Basic statistics
        basic_stats = {
            "total_questions": len(questions),
            "themes_distribution": self._analyze_themes(df),
            "question_lengths": self._analyze_lengths(df),
            "accentuation_patterns": self._analyze_accentuation(df)
        }
        
        # Generate visualizations
        self._generate_visualizations(df, exam_name)
        
        # Save detailed statistics to JSON
        self._save_statistics(basic_stats, exam_name)
        
        return basic_stats
    
    def _analyze_themes(self, df: pd.DataFrame) -> Dict:
        """Analyze the distribution of themes."""
        if 'theme' not in df.columns:
            return {}
            
        theme_counts = df['theme'].value_counts().to_dict()
        return {
            "counts": theme_counts,
            "most_common": max(theme_counts.items(), key=lambda x: x[1])[0],
            "theme_percentages": {k: v/len(df)*100 for k, v in theme_counts.items()}
        }
    
    def _analyze_lengths(self, df: pd.DataFrame) -> Dict:
        """Analyze question lengths."""
        if 'text' not in df.columns:
            return {}
            
        lengths = df['text'].str.len()
        return {
            "average_length": lengths.mean(),
            "min_length": lengths.min(),
            "max_length": lengths.max(),
            "std_dev": lengths.std()
        }
    
    def _analyze_accentuation(self, df: pd.DataFrame) -> Dict:
        """Analyze accentuation patterns."""
        if 'accentuation' not in df.columns:
            return {}
            
        accentuation_data = df['accentuation'].apply(pd.Series)
        return {
            "total_accents": accentuation_data.sum().to_dict(),
            "average_per_question": accentuation_data.mean().to_dict()
        }
    
    def _generate_visualizations(self, df: pd.DataFrame, exam_name: str):
        """Generate visualization plots."""
        # Theme distribution plot
        if 'theme' in df.columns:
            plt.figure(figsize=(10, 6))
            sns.countplot(data=df, y='theme')
            plt.title('Distribution of Question Themes')
            plt.tight_layout()
            plt.savefig(f"{self.output_dir}/{exam_name}_theme_distribution.png")
            plt.close()
        
        # Question length distribution
        if 'text' in df.columns:
            plt.figure(figsize=(10, 6))
            df['text'].str.len().hist(bins=30)
            plt.title('Distribution of Question Lengths')
            plt.xlabel('Length (characters)')
            plt.ylabel('Frequency')
            plt.savefig(f"{self.output_dir}/{exam_name}_length_distribution.png")
            plt.close()
    
    def _save_statistics(self, stats: Dict, exam_name: str):
        """Save detailed statistics to JSON file."""
        output_file = f"{self.output_dir}/{exam_name}_statistics.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)

class StatisticsAnalysisTool(BaseTool):
    name: str = "Question Statistics Generator"
    description: str = "Generates comprehensive statistics about exam questions"
    
    def __init__(self):
        self.generator = QuestionStatisticsGenerator()
    
    def _run(self, questions: List[Dict], exam_name: str = "default_exam") -> Dict:
        return self.generator.generate_statistics(questions, exam_name)

def get_statistics_tool() -> BaseTool:
    """Get the statistics generation tool."""
    return StatisticsAnalysisTool()

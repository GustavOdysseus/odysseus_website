import pdfplumber
import pandas as pd
import json
from openai import OpenAI
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Dict
import os
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()

class QuestionAnalyzer:
    def __init__(self):
        # Carrega variáveis de ambiente do arquivo .env
        load_dotenv()
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY não encontrada no arquivo .env")
        self.client = OpenAI(api_key=api_key)
        
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extrai texto do PDF."""
        with pdfplumber.open(pdf_path) as pdf:
            text = ''
            for page in pdf.pages:
                text += page.extract_text()
        return text
    
    def split_into_questions(self, text: str) -> List[Dict[str, str]]:
        """Separa o texto em questões individuais usando o padrão [Q + números]."""
        import re
        
        # Encontra todas as questões usando o padrão [Q + números]
        pattern = r'\[Q(\d+)\](.*?)(?=\[Q\d+\]|\Z)'
        matches = re.findall(pattern, text, re.DOTALL)
        
        # Cria um dicionário para evitar duplicatas
        questions_dict = {}
        for q_id, content in matches:
            # Se já existe uma questão com esse ID, ignora
            if q_id not in questions_dict:
                questions_dict[q_id] = {
                    'id': q_id,
                    'content': content.strip()
                }
        
        # Converte o dicionário em lista
        return list(questions_dict.values())

    def analyze_question(self, question: Dict[str, str]) -> Dict:
        """Analisa uma questão usando GPT-4-mini."""
        prompt = f"""Analise a seguinte questão de concurso em português e retorne em formato docstring:

Questão:
{question['content']}

Retorne no seguinte formato:
'''
Matéria: [matéria principal]
Subtópicos:
- [subtópico 1]
- [subtópico 2]
- [subtópico 3]

Nível de Dificuldade: [1-5]

Habilidades Avaliadas:
- [habilidade 1]
- [habilidade 2]
- [habilidade 3]
'''
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            # Extrai informações da docstring
            docstring = response.choices[0].message.content.strip()
            
            # Parse da docstring para extrair informações
            import re
            
            materia = re.search(r'Matéria:\s*(.+)', docstring).group(1).strip()
            subtopicos = re.findall(r'- (.+)', docstring.split('Subtópicos:')[1].split('Nível')[0])
            nivel = int(re.search(r'Nível de Dificuldade:\s*(\d+)', docstring).group(1))
            habilidades = re.findall(r'- (.+)', docstring.split('Habilidades Avaliadas:')[1])
            
            result = {
                'id': question['id'],
                'texto_questao': question['content'],
                'materia': materia,
                'subtopicos': subtopicos[:3],  # Limita a 3 subtópicos
                'dificuldade': nivel,
                'habilidades': habilidades[:3]  # Limita a 3 habilidades
            }
            
            return result
        except Exception as e:
            print(f"Erro ao analisar questão {question['id']}: {e}")
            return None

    def analyze_batch(self, questions: List[Dict[str, str]]) -> List[Dict]:
        """Analisa um lote de questões."""
        results = []
        total = len(questions)
        
        print(f"\nAnalisando {total} questões...")
        
        for i, question in enumerate(tqdm(questions, desc="Analisando questões")):
            result = self.analyze_question(question)
            if result:
                results.append(result)
                
                # Salva resultados parciais a cada 10 questões
                if (i + 1) % 10 == 0:
                    self.save_partial_results(results)
                    print(f"\nProgresso: {i + 1}/{total} questões analisadas")
        
        return results
    
    def save_partial_results(self, results: List[Dict], output_dir: str = 'resultados'):
        """Salva resultados parciais em CSV."""
        os.makedirs(output_dir, exist_ok=True)
        df = pd.DataFrame(results)
        df.to_csv(os.path.join(output_dir, 'resultados_parciais.csv'), index=False)

    def generate_visualizations(self, results: List[Dict], output_dir: str = 'resultados'):
        """Gera visualizações interativas com Plotly."""
        # Cria diretório de resultados se não existir
        os.makedirs(output_dir, exist_ok=True)
        
        df = pd.DataFrame(results)
        
        # 1. Distribuição de Matérias
        fig_materias = px.pie(df, names='materia', title='Distribuição de Matérias')
        fig_materias.write_html(os.path.join(output_dir, 'distribuicao_materias.html'))
        
        # 2. Nível de Dificuldade por Matéria
        fig_dificuldade = px.box(df, x='materia', y='dificuldade', 
                                title='Distribuição de Dificuldade por Matéria')
        fig_dificuldade.write_html(os.path.join(output_dir, 'dificuldade_por_materia.html'))
        
        # 3. Análise de Subtópicos
        subtopicos_flat = [sub for subs in df['subtopicos'] for sub in subs]
        subtopicos_freq = pd.Series(subtopicos_flat).value_counts()
        fig_subtopicos = px.bar(x=subtopicos_freq.index, y=subtopicos_freq.values,
                               title='Frequência de Subtópicos')
        fig_subtopicos.write_html(os.path.join(output_dir, 'frequencia_subtopicos.html'))
        
        # Salvar resultados em CSV para análise posterior
        df.to_csv(os.path.join(output_dir, 'resultados_analise.csv'), index=False)
        
        print(f"""
        Análise concluída! Arquivos gerados em {output_dir}:
        - distribuicao_materias.html
        - dificuldade_por_materia.html
        - frequencia_subtopicos.html
        - resultados_analise.csv
        """)

def main():
    # Inicializa o analisador
    try:
        analyzer = QuestionAnalyzer()
    except ValueError as e:
        print(f"Erro: {e}")
        print("Por favor, crie um arquivo .env com sua chave da API OpenAI (OPENAI_API_KEY=sua_chave)")
        return
    
    # Caminho do PDF
    pdf_path = "/Users/gustavomonteiro/Documents/teste/Simulado_port_1.pdf"
    
    try:
        # Extrair e processar texto
        print("Extraindo texto do PDF...")
        text = analyzer.extract_text_from_pdf(pdf_path)
        
        print("Separando questões...")
        questions = analyzer.split_into_questions(text)
        print(f"Encontradas {len(questions)} questões.")
        
        if len(questions) == 0:
            print("Nenhuma questão foi encontrada no PDF. Verifique se o formato está correto.")
            return
        
        # Analisar questões
        print("Iniciando análise das questões...")
        results = analyzer.analyze_batch(questions)
        
        if not results:
            print("Não foi possível analisar as questões. Verifique sua chave da API e tente novamente.")
            return
        
        # Gerar visualizações
        print("Gerando visualizações...")
        analyzer.generate_visualizations(results)
        
    except Exception as e:
        print(f"Erro durante a execução: {e}")
        print("Por favor, verifique se o arquivo PDF está correto e se sua chave da API OpenAI é válida.")

if __name__ == "__main__":
    main()

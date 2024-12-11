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
import time
from datetime import datetime

load_dotenv()

class QuestionAnalyzer:
    def __init__(self):
        # Carrega variáveis de ambiente do arquivo .env
        load_dotenv()
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY não encontrada no arquivo .env")
        self.client = OpenAI(api_key=api_key)
        self.total_analysis_time = 0
        self.questions_analyzed = 0
        
    def log_time(self, message: str):
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"[{timestamp}] {message}")
        
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extrai texto do PDF."""
        start_time = time.time()
        self.log_time(f"Extraindo texto do PDF...")
        with pdfplumber.open(pdf_path) as pdf:
            text = ''
            for page in pdf.pages:
                text += page.extract_text()
        extraction_time = time.time() - start_time
        self.log_time(f"Texto extraído em {extraction_time:.2f}s")
        return text
    
    def split_into_questions(self, text: str) -> List[Dict[str, str]]:
        """Separa o texto em questões individuais usando o padrão [Q + números]."""
        start_time = time.time()
        self.log_time(f"Separando questões...")
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
        questions = list(questions_dict.values())
        splitting_time = time.time() - start_time
        self.log_time(f"Questões separadas em {splitting_time:.2f}s")
        self.log_time(f"Encontradas {len(questions)} questões.")
        return questions

    def analyze_question(self, question: Dict[str, str]) -> Dict:
        """Analisa uma questão usando GPT-4o-mini com análise detalhada."""
        start_time = time.time()
        self.questions_analyzed += 1
        
        self.log_time(f"Analisando questão {question['id']} ({self.questions_analyzed})")
        prompt = f"""Analise a seguinte questão de concurso em português e forneça uma análise detalhada.
Para as armadilhas, considere:
1. Identifique armadilhas específicas desta questão
2. Se for uma questão de interpretação de texto, considere aspectos como:
   - Relações de causa e efeito
   - Inferências vs informações explícitas
   - Uso de palavras com múltiplos sentidos
3. Se envolver dados numéricos, considere:
   - Confusão entre percentuais e valores absolutos
   - Interpretação de tendências
4. Inclua trechos do texto APENAS quando forem essenciais para entender a armadilha
5. Não se limite ao que foi falado acima, você tem Discernimento e experiencia na area, seja coeso e coerente nas Decisões. 
Questão:
{question['content']}

Retorne no seguinte formato EXATO:
'''
Categoria Principal: [categoria ampla]

Subtema Específico: [tópico específico]

Nível de Dificuldade: [1-5]
Justificativa da Dificuldade: [explicação breve]

Principais Armadilhas:
• [armadilha específica - se necessário, inclua "Trecho relevante: [trecho]" antes da explicação]
• [armadilha específica - se necessário, inclua "Trecho relevante: [trecho]" antes da explicação]

Resumo Analítico:
[breve análise da questão]
'''
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            analysis_time = time.time() - start_time
            self.total_analysis_time += analysis_time
            avg_time = self.total_analysis_time / self.questions_analyzed
            
            self.log_time(f"Questão {question['id']} analisada em {analysis_time:.2f}s (média: {avg_time:.2f}s)")
            
            # Extrai informações da docstring
            docstring = response.choices[0].message.content.strip()
            
            # Parse da docstring para extrair informações
            import re
            
            categoria = re.search(r'Categoria Principal:\s*(.+)', docstring).group(1).strip()
            subtema = re.search(r'Subtema Específico:\s*(.+)', docstring).group(1).strip()
            nivel = int(re.search(r'Nível de Dificuldade:\s*(\d+)', docstring).group(1))
            justificativa = re.search(r'Justificativa da Dificuldade:\s*(.+)', docstring).group(1).strip()
            armadilhas = re.findall(r'•\s*(.+?)(?=•|\n\n|$)', docstring.split('Principais Armadilhas:')[1].split('Resumo')[0], re.DOTALL)
            armadilhas = [a.strip() for a in armadilhas if a.strip()]
            resumo = re.search(r'Resumo Analítico:\s*(.+)', docstring, re.DOTALL).group(1).strip()
            
            result = {
                'id': question['id'],
                'texto_questao': question['content'],
                'categoria_principal': categoria,
                'subtema_especifico': subtema,
                'dificuldade': nivel,
                'justificativa_dificuldade': justificativa,
                'armadilhas': armadilhas,
                'resumo_analitico': resumo
            }
            
            return result
            
        except Exception as e:
            print(f"Erro ao analisar questão {question['id']}: {str(e)}")
            return None

    def analyze_batch(self, questions: List[Dict[str, str]]) -> List[Dict]:
        """Analisa um lote de questões."""
        start_time = time.time()
        self.log_time(f"Iniciando análise de {len(questions)} questões...")
        results = []
        total = len(questions)
        
        for i, question in enumerate(tqdm(questions, desc="Analisando questões")):
            result = self.analyze_question(question)
            if result:
                results.append(result)
                
                # Salva resultados parciais a cada 10 questões
                if (i + 1) % 10 == 0:
                    self.save_partial_results(results)
                    self.log_time(f"Progresso: {i + 1}/{total} questões analisadas")
        
        batch_time = time.time() - start_time
        self.log_time(f"Análise de lote concluída em {batch_time:.2f}s")
        return results
    
    def save_partial_results(self, results: List[Dict], output_dir: str = 'resultados'):
        """Salva resultados parciais em CSV."""
        start_time = time.time()
        self.log_time(f"Salvando resultados parciais...")
        os.makedirs(output_dir, exist_ok=True)
        df = pd.DataFrame(results)
        df.to_csv(os.path.join(output_dir, 'resultados_parciais.csv'), index=False)
        save_time = time.time() - start_time
        self.log_time(f"Resultados parciais salvos em {save_time:.2f}s")

    def generate_visualizations(self, results: List[Dict], output_dir: str = 'resultados'):
        """Gera visualizações e análises detalhadas."""
        start_time = time.time()
        self.log_time(f"Gerando visualizações...")
        os.makedirs(output_dir, exist_ok=True)
        df = pd.DataFrame(results)
        
        # Análise por categoria
        categorias = {}
        
        # Gerar análises específicas
        for _, row in df.iterrows():
            categoria = row['categoria_principal']
            if categoria not in categorias:
                categorias[categoria] = {
                    'total_questoes': 0,
                    'dificuldade_media': 0,
                    'subtemas': {},
                    'armadilhas': set(),
                    'questoes_ids': []
                }
            
            info = categorias[categoria]
            info['total_questoes'] += 1
            info['dificuldade_media'] += row['dificuldade']
            info['questoes_ids'].append(row['id'])
            
            # Adicionar subtema
            subtema = row['subtema_especifico']
            if subtema not in info['subtemas']:
                info['subtemas'][subtema] = 0
            info['subtemas'][subtema] += 1
            
            # Adicionar armadilhas
            info['armadilhas'].update(row['armadilhas'])
        
        # Calcular percentuais e médias
        total_questoes = len(df)
        for categoria, info in categorias.items():
            info['percentual'] = (info['total_questoes'] / total_questoes) * 100
            info['dificuldade_media'] /= info['total_questoes']
        
        # Gerar relatório detalhado
        with open(os.path.join(output_dir, 'analise_resumida.txt'), 'w', encoding='utf-8') as f:
            f.write("ANÁLISE RESUMIDA DAS QUESTÕES\n\n")
            
            # Análise Quantitativa Geral
            f.write("ANÁLISE QUANTITATIVA GERAL\n")
            f.write("="*50 + "\n")
            f.write(f"Total de questões analisadas: {total_questoes}\n")
            f.write(f"Número de categorias principais: {len(categorias)}\n\n")
            
            # Distribuição por categoria
            f.write("DISTRIBUIÇÃO POR CATEGORIA:\n")
            for categoria, info in sorted(categorias.items(), 
                                        key=lambda x: x[1]['total_questoes'], 
                                        reverse=True):
                f.write(f"• {categoria}: {info['percentual']:.1f}% ({info['total_questoes']} questões)\n")
            f.write("\n")
            
            # Detalhamento por Categoria
            for categoria, info in sorted(categorias.items(), 
                                        key=lambda x: x[1]['total_questoes'], 
                                        reverse=True):
                f.write("\n" + "="*50 + "\n")
                f.write(f"CATEGORIA: {categoria} (Total: {info['total_questoes']} questões)\n")
                f.write("="*50 + "\n")
                f.write(f"Dificuldade média: {info['dificuldade_media']:.1f}/5\n\n")
                
                f.write("Subtemas identificados:\n")
                for subtema, count in sorted(info['subtemas'].items(), 
                                           key=lambda x: x[1], 
                                           reverse=True):
                    f.write(f"- {subtema} ({count} questões)\n")
                f.write("\n")
                
                f.write("Principais armadilhas:\n")
                for armadilha in sorted(list(info['armadilhas']))[:5]:  # Limitando a 5 armadilhas
                    f.write(f"• {armadilha}\n")
                f.write("\n")
                
                # Criar gráficos
                self._create_category_charts(df, output_dir)
        
        visualization_time = time.time() - start_time
        self.log_time(f"Visualizações geradas em {visualization_time:.2f}s")
    
    def _create_category_charts(self, df: pd.DataFrame, output_dir: str):
        """Cria gráficos de análise por categoria."""
        start_time = time.time()
        self.log_time(f"Gerando gráficos de análise por categoria...")
        # Gráfico de distribuição por categoria
        fig_dist = px.pie(df, 
                         names='categoria_principal', 
                         title='Distribuição de Questões por Categoria')
        fig_dist.write_html(os.path.join(output_dir, 'distribuicao_categorias.html'))
        
        # Gráfico de dificuldade média por categoria
        df_diff = df.groupby('categoria_principal')['dificuldade'].mean().reset_index()
        fig_diff = px.bar(df_diff, 
                         x='categoria_principal', 
                         y='dificuldade',
                         title='Dificuldade Média por Categoria')
        fig_diff.write_html(os.path.join(output_dir, 'dificuldade_categorias.html'))
        
        chart_time = time.time() - start_time
        self.log_time(f"Gráficos de análise por categoria gerados em {chart_time:.2f}s")

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

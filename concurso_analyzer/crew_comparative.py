from crewai import Agent, Task, Crew, Process
from typing import List, Dict
import PyPDF2
import re
import json
import spacy
from pathlib import Path
from dotenv import load_dotenv
import os
import time
import openai
from collections import defaultdict

# Carrega variáveis de ambiente
load_dotenv()

# Configuração OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI()

class PDFExtractorAgent(Agent):
    def __init__(self):
        super().__init__(
            role='PDF Extractor',
            goal='Extrair questões de PDFs de concursos',
            backstory='Especialista em extração de texto de documentos PDF',
            verbose=True
        )

    def execute_task(self, task):
        pdf_paths = task.context[0].get('pdf_paths', [])
        print(f"\n=== Extraindo questões de {len(pdf_paths)} PDFs ===")
        
        extracted_questions = []
        for pdf_path in pdf_paths:
            try:
                questions = self.extract_questions(pdf_path)
                extracted_questions.append(questions)
                print(f"Extraídas {len(questions.get('questions', []))} questões de {os.path.basename(pdf_path)}")
            except Exception as e:
                print(f"Erro ao extrair questões de {pdf_path}: {e}")
        
        return extracted_questions

    def extract_questions(self, pdf_path: str) -> Dict:
        """
        Extrai perguntas de um arquivo PDF e retorna um dicionário com metadados.
        """
        print(f"\n=== Extraindo questões de {os.path.basename(pdf_path)} ===")
        try:
            text = self.read_pdf(pdf_path)
            print(f"Texto extraído com sucesso: {len(text)} caracteres")
            
            questions = self.split_into_questions(text)
            print(f"Questões encontradas: {len(questions)}")
            for i, q in enumerate(questions, 1):
                print(f"  {i}. Questão {q['number']} - {len(q['text'])} caracteres")
            
            result = {
                "file": pdf_path,
                "total_questions": len(questions),
                "questions": questions
            }
            print(f"Extração concluída: {len(questions)} questões extraídas")
            return result
        except Exception as e:
            print(f"Erro crítico na extração de questões do PDF {pdf_path}: {e}")
            return {
                "file": pdf_path,
                "total_questions": 0,
                "questions": [],
                "error": str(e)
            }

    def read_pdf(self, pdf_path: str) -> str:
        """
        Lê e extrai texto de um arquivo PDF, página por página, preservando quebras e organização.
        """
        print(f"\n=== Lendo PDF: {os.path.basename(pdf_path)} ===")
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"Arquivo PDF não encontrado: {pdf_path}")
        
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                print(f"Total de páginas: {len(reader.pages)}")
                
                if len(reader.pages) == 0:
                    print(f"Aviso: Nenhuma página encontrada no arquivo {pdf_path}")
                    return ""
                
                text = ""
                for page_num, page in enumerate(reader.pages, 1):
                    try:
                        extracted_text = page.extract_text()
                        normalized_text = self.normalize_text(extracted_text)
                        text += normalized_text + "\n"
                        print(f"Página {page_num}: {len(normalized_text)} caracteres extraídos")
                    except Exception as page_error:
                        print(f"Erro ao processar página {page_num} do PDF {pdf_path}: {page_error}")
                
                print(f"Leitura concluída: {len(text)} caracteres totais")
                return text
        except Exception as e:
            print(f"Erro crítico ao processar PDF {pdf_path}: {e}")
            return ""

    def split_into_questions(self, text: str) -> List[Dict]:
        """
        Divide o texto extraído em questões com múltiplas estratégias de extração.
        """
        print("\n=== Dividindo texto em questões ===")
        question_patterns = [
            r'(\d+\.\s*)',  # Questões numeradas com ponto
            r'(\d+\)\s*)',  # Questões numeradas com parênteses
            r'(Questão\s+\d+:)',  # Padrão "Questão X:"
        ]
        
        questions = []
        print("Tentando diferentes padrões de extração:")
        
        for pattern in question_patterns:
            print(f"Testando padrão: {pattern}")
            question_blocks = re.split(pattern, text)
            
            if len(question_blocks) > 2:
                print(f"Padrão encontrou {(len(question_blocks)-1)//2} possíveis questões")
                for i in range(1, len(question_blocks), 2):
                    try:
                        question_number = question_blocks[i].strip()
                        question_text = question_blocks[i + 1].strip()
                        
                        if 10 < len(question_text) < 1000:
                            questions.append({
                                "number": question_number,
                                "text": question_text,
                                "raw_text": f"{question_number} {question_text}",
                                "length": len(question_text)
                            })
                            print(f"  Questão {question_number} extraída: {len(question_text)} caracteres")
                    except Exception as e:
                        print(f"Erro ao processar questão: {e}")
            
            if questions:
                print(f"Padrão {pattern} encontrou {len(questions)} questões válidas")
                break
            else:
                print(f"Padrão {pattern} não encontrou questões válidas")
        
        print(f"\nTotal de questões extraídas: {len(questions)}")
        return questions

    def normalize_text(self, text: str) -> str:
        """
        Limpa e normaliza o texto extraído para melhorar a consistência.
        """
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'…', '...', text)
        return text.strip()

    def extract_structure(self, text: str) -> Dict:
        """
        Adiciona marcadores ao texto para separar títulos, subtítulos, tabelas, etc.
        """
        structured_text = re.sub(r'^\s*[A-Z ]+\s*$', r'<TÍTULO>\g<0>', text, flags=re.MULTILINE)
        structured_text = re.sub(r'(\d+\))', r'<QUESTÃO>\g<1>', structured_text)
        return {"structured_text": structured_text}


class QuestionAnalyzerAgent(Agent):
    def __init__(self):
        super().__init__(
            role='Question Analyzer',
            goal='Analisar padrões específicos de português',
            backstory='Especialista em análise de conteúdo e identificação de padrões em questões de concurso',
            verbose=True
        )

    def execute_task(self, task):
        questions_list = task.context[0].get('extracted_questions', [])
        
        # Achatar a lista de questões
        all_questions = []
        for questions_dict in questions_list:
            if isinstance(questions_dict, dict) and 'questions' in questions_dict:
                all_questions.extend(questions_dict['questions'])
        
        analysis = self.analyze_questions(all_questions)
        
        result = "ANÁLISE DETALHADA DE PORTUGUÊS\n\n"
        
        result += "📚 TÓPICOS GERAIS:\n"
        for topic, count in analysis['tópicos_gerais'].items():
            result += f"- {topic}: {count} questões\n"
        
        result += "\n🔤 TÓPICOS GRAMATICAIS:\n"
        for topic, count in analysis['tópicos_gramática'].items():
            result += f"- {topic}: {count} questões\n"
        
        result += "\n✍️ ACENTUAÇÃO:\n"
        for accent, count in analysis['acentuação'].items():
            result += f"- {accent}: {count} ocorrências\n"
        
        result += "\n📝 PONTUAÇÃO:\n"
        for punct, count in analysis['pontuação'].items():
            result += f"- {punct}: {count} ocorrências\n"
        
        result += "\n⏰ TEMPOS VERBAIS:\n"
        for tense, count in analysis['tempos_verbais'].items():
            result += f"- {tense}: {count} ocorrências\n"
        
        return result

    def analyze_questions(self, questions: List[Dict]) -> Dict:
        """
        Analisa as questões para identificar padrões específicos de português.
        """
        topics = defaultdict(int)
        grammar_topics = defaultdict(int)
        punctuation = defaultdict(int)
        accentuation = defaultdict(int)
        verb_tenses = defaultdict(int)
        
        # Padrões específicos de português
        patterns = {
            'acentuação': {
                'crase': [r'crase', r'à\s', r'às\s', r'àquele', r'àquela'],
                'agudo': [r'[áéíóú]', r'acento agudo'],
                'circunflexo': [r'[âêîôû]', r'acento circunflexo'],
                'til': [r'[ãõ]', r'til']
            },
            'pontuação': {
                'vírgula': [r'vírgula', r',\s'],
                'ponto_vírgula': [r'ponto e vírgula', r';\s'],
                'dois_pontos': [r'dois pontos', r':\s'],
                'travessão': [r'travessão', r'—'],
            },
            'verbos': {
                'presente': [r'presente do indicativo', r'presente simples'],
                'pretérito_perfeito': [r'pretérito perfeito', r'passado perfeito'],
                'pretérito_imperfeito': [r'pretérito imperfeito', r'passado imperfeito'],
                'futuro': [r'futuro do presente', r'futuro simples'],
                'subjuntivo': [r'subjuntivo', r'modo subjuntivo']
            },
            'gramática': {
                'concordância_verbal': [r'concordância verbal', r'sujeito concorda'],
                'concordância_nominal': [r'concordância nominal', r'substantivo concorda'],
                'regência': [r'regência', r'verbo rege'],
                'colocação_pronominal': [r'colocação pronominal', r'próclise', r'ênclise', r'mesóclise'],
                'análise_sintática': [r'análise sintática', r'oração subordinada', r'período composto']
            }
        }
        
        for question in questions:
            text = question['text'].lower()
            
            # Análise por padrões específicos
            for category, subcategories in patterns.items():
                for subcategory, patterns_list in subcategories.items():
                    for pattern in patterns_list:
                        if re.search(pattern, text, re.IGNORECASE):
                            if category == 'acentuação':
                                accentuation[subcategory] += 1
                            elif category == 'pontuação':
                                punctuation[subcategory] += 1
                            elif category == 'verbos':
                                verb_tenses[subcategory] += 1
                            elif category == 'gramática':
                                grammar_topics[subcategory] += 1
            
            # Identificação de tópicos gerais
            if "interpretação" in text or "compreensão" in text:
                topics["Interpretação de Texto"] += 1
            if "literatura" in text:
                topics["Literatura"] += 1
            if "fonética" in text or "fonologia" in text:
                topics["Fonética/Fonologia"] += 1
            if "morfologia" in text:
                topics["Morfologia"] += 1
            if "sintaxe" in text:
                topics["Sintaxe"] += 1
            if "semântica" in text:
                topics["Semântica"] += 1
            if "ortografia" in text:
                topics["Ortografia"] += 1

        return {
            "tópicos_gerais": dict(sorted(topics.items(), key=lambda x: x[1], reverse=True)),
            "tópicos_gramática": dict(sorted(grammar_topics.items(), key=lambda x: x[1], reverse=True)),
            "acentuação": dict(sorted(accentuation.items(), key=lambda x: x[1], reverse=True)),
            "pontuação": dict(sorted(punctuation.items(), key=lambda x: x[1], reverse=True)),
            "tempos_verbais": dict(sorted(verb_tenses.items(), key=lambda x: x[1], reverse=True))
        }

class PatternDiscoveryAgent(Agent):
    def __init__(self):
        super().__init__(
            role='Pattern Discoverer',
            goal='Descobrir tendências e padrões nas questões',
            backstory='Especialista em análise de tendências e identificação de padrões em concursos',
            verbose=True
        )

    def execute_task(self, task):
        analysis_results = task.context[0].get('analysis_results', '')
        
        insights = []
        
        # Extrair informações do resultado da análise
        sections = analysis_results.split('\n\n')
        
        for section in sections:
            if "TÓPICOS GERAIS" in section:
                topics = [line.strip('- ').split(':')[0] for line in section.split('\n')[1:] if line]
                if topics:
                    insights.append(f"🔍 FOCO DO CONCURSO: O concurso tem ênfase especial em {', '.join(topics[:3])}")
            
            if "TIPOS DE QUESTÃO" in section:
                types = [line.strip('- ').split(':')[0] for line in section.split('\n')[1:] if line]
                if types:
                    insights.append(f"📋 ESTILO DE PROVA: Predominam questões do tipo {', '.join(types[:2])}")
        
        # Gerar recomendações práticas
        insights.append("\n💡 RECOMENDAÇÕES PARA ESTUDO:")
        insights.append("1. Focar nos tópicos mais frequentes identificados")
        insights.append("2. Praticar especialmente os tipos de questão predominantes")
        insights.append("3. Revisar os subtópicos específicos que mais aparecem")
        
        return "\n".join(insights)

class ReportGeneratorAgent(Agent):
    def __init__(self):
        super().__init__(
            role='Report Generator',
            goal='Gerar relatório final com insights práticos',
            backstory='Especialista em comunicação e síntese de informações',
            verbose=True
        )

    def execute_task(self, task):
        patterns = task.context[0].get('patterns', '')
        
        report = """
📊 ANÁLISE DE TENDÊNCIAS DO CONCURSO
===================================

"""
        # Adicionar padrões descobertos
        report += patterns

        # Adicionar conclusão
        report += """

🎯 CONCLUSÃO
-----------
Esta análise revela os padrões mais importantes e frequentes nas questões do concurso,
permitindo um direcionamento mais eficiente dos estudos e da preparação.

"""
        return report

def analyze_exam_pdfs(pdf_paths: List[str], subject: str = "Português"):
    """
    Analisa PDFs de provas e gera um relatório completo.
    """
    print("\n=== Iniciando análise de PDFs ===")
    print(f"Número de arquivos a serem analisados: {len(pdf_paths)}")
    for pdf in pdf_paths:
        print(f"- {os.path.basename(pdf)}")

    # Criar agentes
    print("\n=== Inicializando agentes ===")
    extractor = PDFExtractorAgent()
    analyzer = QuestionAnalyzerAgent()
    pattern_discoverer = PatternDiscoveryAgent()
    report_generator = ReportGeneratorAgent()
    print("Agentes inicializados com sucesso")

    # Criar tarefas
    print("\n=== Definindo tarefas ===")
    tasks = [
        Task(
            description=f"Extrair questões de {len(pdf_paths)} PDFs",
            agent=extractor,
            context=[{
                "description": f"Extrair questões de {len(pdf_paths)} PDFs",
                "pdf_paths": pdf_paths,
                "expected_output": "Lista de questões extraídas"
            }],
            expected_output="Lista de questões extraídas"
        ),
        Task(
            description="Analisar cada questão extraída",
            agent=analyzer,
            context=[{
                "description": "Analisar cada questão extraída",
                "extracted_questions": [],
                "expected_output": "Análise detalhada das questões"
            }],
            expected_output="Análise detalhada das questões"
        ),
        Task(
            description="Descobrir padrões entre as questões",
            agent=pattern_discoverer,
            context=[{
                "description": "Descobrir padrões entre as questões",
                "analysis_results": "",
                "expected_output": "Relatório de padrões encontrados"
            }],
            expected_output="Relatório de padrões encontrados"
        ),
        Task(
            description="Gerar relatório final",
            agent=report_generator,
            context=[{
                "description": "Gerar relatório final",
                "patterns": "",
                "expected_output": "Relatório completo de análise"
            }],
            expected_output="Relatório completo de análise"
        )
    ]
    print("Tarefas definidas com sucesso")

    # Criar crew
    print("\n=== Configurando equipe de análise ===")
    crew = Crew(
        agents=[extractor, analyzer, pattern_discoverer, report_generator],
        tasks=tasks,
        verbose=True
    )
    print("Equipe configurada com sucesso")

    # Executar análise
    print("\n=== Iniciando execução da análise ===")
    result = crew.kickoff()
    print("\n=== Análise concluída ===")
    
    # Converter resultado para string e formatar
    print("\n=== Gerando relatório final ===")
    result_str = f"""
Análise de Questões de Concurso
==============================

Arquivos analisados:
{', '.join(os.path.basename(pdf) for pdf in pdf_paths)}

Resultado da Análise:
-------------------
{str(result)}
"""
    
    # Salvar resultado
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(os.path.dirname(__file__), f"analise_comparativa_{timestamp}.txt")
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result_str)
        print(f"\nAnálise salva com sucesso em: {output_file}")
    except Exception as e:
        print(f"Erro ao salvar arquivo: {e}")
    
    return result

if __name__ == "__main__":
    pdf_dir = "/Users/gustavomonteiro/Desktop/prova/"
    pdf_files = [os.path.join(pdf_dir, f) for f in os.listdir(pdf_dir) if f.endswith('.pdf')]
    result = analyze_exam_pdfs(pdf_files)
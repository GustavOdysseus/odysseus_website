#!/usr/bin/env python

import os
import re
import json
import logging
import sys
import traceback
from typing import Any, Dict, Union
from datetime import datetime
from pathlib import Path

# CrewAI imports
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.parser import AgentAction, AgentFinish
from crewai.utilities.logger import Logger
from crewai.tasks.task_output import TaskOutput

# LangChain imports
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

# Local imports
from config.settings import (
    CONTROLES,
    RESTRICOES,
    TEMPLATE_YAML,
    SOLICITACOES
)
from tools.custom_tool import (
    ArxivSearchTool,
    PDFAnalysisTool,
    YAMLValidationTool
)

# Third-party imports
from dotenv import load_dotenv
import yaml

# Encontrar o diretório raiz do projeto (2 níveis acima do diretório atual)
PROJECT_ROOT = Path(__file__).parent.parent.parent.absolute()
# Carregar variáveis de ambiente do arquivo .env no diretório raiz
dotenv_path = os.path.join(PROJECT_ROOT, '.env')
load_dotenv(dotenv_path)

def normalize_filename(text, sep="-"):   
    return sep.join([i.strip() for i in re.split(r'[^a-z0-9]+', text.lower()) if i.strip()])

# Configurações de entrada
INPUT_TOPIC = "quantitative finance"
OUTPUT_FILE = f"{normalize_filename(INPUT_TOPIC)}.yaml"

# Configuração de logging detalhado
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('debug.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)
crewai_logger = Logger()

@CrewBase
class ArxivCrew():
    """Arxiv crew para análise de artigos científicos"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    
    def __init__(self):
        try:
            super().__init__()
            logger.debug("Iniciando ArxivCrew")
            
            # Usar o modelo correto
            model_name = os.getenv('OPENAI_MODEL_NAME', 'gpt-4o-mini')
            
            # Configurar o LLM apropriado para o modelo
            self.llm = ChatOpenAI(
                model=model_name,
                temperature=0.7,
                request_timeout=120,
                max_retries=3
            )

            logger.debug(f"LLM inicializado com modelo: {model_name}")
        except Exception as e:
            logger.error(f"Erro na inicialização do ArxivCrew: {str(e)}")
            logger.error(f"Stack trace: {traceback.format_exc()}")
            raise

    @agent
    def pesquisador_de_dados(self) -> Agent:
        try:
            logger.debug("Criando agente pesquisador_de_dados")
            search_tool = ArxivSearchTool()
            logger.debug(f"ArxivSearchTool criada: {search_tool}")
            
            agent = Agent(
                config=self.agents_config['pesquisador_de_dados'],
                tools=[search_tool],
                verbose=True,
                cache=True,
                use_system_prompt=True,
                max_rpm=30,
                max_iter=5,
                llm=self.llm
            )
            logger.debug(f"Agente criado: {agent}")
            return agent
        except Exception as e:
            logger.error(f"Erro ao criar pesquisador_de_dados: {str(e)}")
            logger.error(f"Stack trace: {traceback.format_exc()}")
            raise

    @agent
    def pdf_reader(self) -> Agent:
        pdf_tool = PDFAnalysisTool()
        return Agent(
            config=self.agents_config['pdf_reader'],
            tools=[pdf_tool],
            verbose=True,
            cache=True,
            use_system_prompt=True,
            max_rpm=30,
            max_iter=5,
            llm=self.llm  # Definir o LLM explicitamente
        )

    @agent
    def revisor_de_artigos(self) -> Agent:
        return Agent(
            config=self.agents_config['revisor_de_artigos'],
            tools=[YAMLValidationTool()],
            verbose=True,
            cache=True,
            use_system_prompt=True,
            max_rpm=30,
            max_iter=5,
            llm=self.llm  # Definir o LLM explicitamente
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'],
            agent=self.pesquisador_de_dados()
        )

    @task
    def leitor_de_pdf_task(self) -> Task:
        return Task(
            config=self.tasks_config['leitor_de_pdf_task'],
            agent=self.pdf_reader()
        )

    @task
    def revisor_de_leitura_task(self) -> Task:
        return Task(
            config=self.tasks_config['revisor_de_leitura_task'],
            agent=self.revisor_de_artigos()
        )

    def task_callback(self, task_output: TaskOutput) -> None:
        """Callback executado após cada tarefa"""
        try:
            logger.debug(f"Processando callback para output: {task_output}")
            
            # Acesso correto aos atributos do TaskOutput
            print(f"\nTarefa: {task_output.description}")
            print(f"Agente: {task_output.agent}")
            print(f"Resultado: {task_output.raw}")
            
            # Salvar em arquivo de log
            with open("task_execution.log", "a", encoding="utf-8") as f:
                f.write(f"\n=== Tarefa Executada em {datetime.now().isoformat()} ===\n")
                f.write(f"Descrição: {task_output.description}\n")
                f.write(f"Agente: {task_output.agent}\n")
                f.write(f"Formato: {task_output.output_format}\n")
                f.write(f"Resultado:\n{task_output.raw}\n")
                if task_output.json_dict:
                    f.write(f"JSON: {json.dumps(task_output.json_dict, indent=2, ensure_ascii=False)}\n")
                f.write("-" * 80 + "\n")
                
        except Exception as e:
            logger.error(f"Erro no task_callback: {str(e)}")
            logger.error(f"Stack trace: {traceback.format_exc()}")
            # Não propagar o erro para não interromper a execução
            print(f"Aviso: Erro no callback de tarefa: {str(e)}")

    def step_callback(self, step_output: Union[AgentAction, AgentFinish]) -> None:
        """Callback executado após cada passo de execução"""
        try:
            if isinstance(step_output, AgentAction):
                # Para ações do agente
                print(f"\nPensamento: {step_output.thought}")
                print(f"Ação: {step_output.tool}")
                print(f"Input da Ação: {step_output.tool_input}")
                if hasattr(step_output, 'result'):
                    print(f"Resultado: {step_output.result}")
                    
                # Log detalhado
                logger.debug(f"Tipo: AgentAction")
                logger.debug(f"Pensamento: {step_output.thought}")
                logger.debug(f"Ferramenta: {step_output.tool}")
                logger.debug(f"Input: {step_output.tool_input}")
                logger.debug(f"Texto completo: {step_output.text}")
                
            elif isinstance(step_output, AgentFinish):
                # Para respostas finais
                print(f"\nPensamento Final: {step_output.thought}")
                print(f"Resposta: {step_output.output}")
                
                # Log detalhado
                logger.debug(f"Tipo: AgentFinish")
                logger.debug(f"Pensamento: {step_output.thought}")
                logger.debug(f"Output: {step_output.output}")
                logger.debug(f"Texto completo: {step_output.text}")
            
            else:
                # Para outros tipos de output (fallback)
                print(f"\nPasso executado: {str(step_output)}")
                logger.warning(f"Tipo de step_output não reconhecido: {type(step_output)}")
                
            # Registrar execução
            with open("crew_execution.log", "a", encoding="utf-8") as f:
                f.write(f"\n=== Passo de Execução ===\n")
                f.write(f"Tipo: {type(step_output).__name__}\n")
                f.write(f"Conteúdo: {str(step_output.__dict__)}\n")
                f.write("-" * 80 + "\n")
                
        except Exception as e:
            logger.error(f"Erro no step_callback: {str(e)}")
            logger.error(f"Stack trace: {traceback.format_exc()}")
            # Não propagar o erro para não interromper a execução
            print(f"Aviso: Erro no callback de passo: {str(e)}")

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            memory=True,
            respect_context_window=True,
            task_callback=self.task_callback,
            step_callback=self.step_callback,
            max_rpm=30,
            planning=True,
            share_crew=False,
            llm=self.llm  # Definir o LLM para o Crew também
        )
    
def run():
    try:
        logger.info("Iniciando execução")
        inputs = {
            'topic': INPUT_TOPIC,
            'solicitacoes': SOLICITACOES,
            'template': TEMPLATE_YAML,
            'restricoes': RESTRICOES,
            'controles': CONTROLES
        }
        logger.debug(f"Inputs configurados: {inputs}")
        
        arxiv_crew = ArxivCrew()
        logger.debug("ArxivCrew instanciado")
        
        crew = arxiv_crew.crew()
        logger.debug(f"Crew criado: {crew}")
        
        result = crew.kickoff()
        logger.debug(f"Resultado do kickoff: {result}")
        
        # Usar raw_output ao invés de output
        final_output = result.raw_output
        task_outputs = result.task_outputs
        
        # Processar YAML final
        yaml_content = final_output
        if isinstance(final_output, str):
            if "```yaml" in final_output:
                yaml_content = final_output.split("```yaml")[1].split("```")[0].strip()
            elif "```" in final_output:
                yaml_content = final_output.split("```")[1].split("```")[0].strip()
        
        # Validar e salvar YAML
        data = yaml.safe_load(yaml_content)
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, sort_keys=False)
            
        print(f"\nResultado salvo em: {OUTPUT_FILE}")
        
        # Salvar relatório de execução
        with open("execution_report.log", "w", encoding="utf-8") as f:
            f.write(f"=== Relatório de Execução ===\n")
            f.write(f"Tópico: {INPUT_TOPIC}\n")
            f.write(f"Data: {datetime.now().isoformat()}\n\n")
            
            for task_output in task_outputs:
                f.write(f"Tarefa: {task_output.task.description}\n")
                f.write(f"Agente: {task_output.task.agent.role}\n")
                f.write(f"Status: {'Sucesso' if task_output.output else 'Falha'}\n")
                f.write("-" * 80 + "\n")
        
    except Exception as e:
        logger.error(f"Erro durante execução: {str(e)}")
        logger.error(f"Stack trace: {traceback.format_exc()}")
        
        with open("error.log", "a", encoding="utf-8") as f:
            f.write(f"\n=== Erro em {datetime.now().isoformat()} ===\n")
            f.write(f"Tópico: {INPUT_TOPIC}\n")
            f.write(f"Erro: {str(e)}\n")
            f.write(f"Stack trace: {traceback.format_exc()}\n")
        raise

if __name__ == "__main__":
    run()
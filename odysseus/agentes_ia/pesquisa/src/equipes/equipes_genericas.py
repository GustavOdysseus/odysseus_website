from pathlib import Path
import yaml
from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel
from crewai import Crew, Agent, Task, Process
from src.logging.logging_config import LoggingConfig
from datetime import datetime
from hashlib import md5
import json

class GerenciadorEquipes:
    """
    Representa um grupo de agentes, definindo como devem colaborar e as tarefas que devem executar.

    Atributos:

        tasks: Lista de tarefas atribuídas ao grupo.
        agents: Lista de agentes que fazem parte deste grupo.
        manager_llm: O modelo de linguagem que será usado para executar o agente gerente.
        manager_agent: Agente personalizado que será utilizado como gerente.
        memory: Indica se o grupo deve usar memória para armazenar informações sobre sua execução.
        cache: Indica se o grupo deve usar cache para armazenar os resultados da execução das ferramentas.
        function_calling_llm: O modelo de linguagem que será usado para gerenciar as chamadas de ferramentas para todos os agentes.
        process: O fluxo de processo que o grupo seguirá (por exemplo, sequencial, hierárquico).
        verbose: Indica o nível de verbosidade para registro durante a execução.
        config: Configurações de configuração para o grupo.
        max_rpm: Número máximo de solicitações por minuto que a execução do grupo deve respeitar.
        prompt_file: Caminho para o arquivo JSON de prompt a ser utilizado pelo grupo.
        id: Identificador único para a instância do grupo.
        task_callback: Função de callback a ser executada após cada tarefa durante a execução de todos os agentes.
        step_callback: Função de callback a ser executada após cada etapa durante a execução de todos os agentes.
        share_crew: Indica se você deseja compartilhar informações completas do grupo e sua execução com o CrewAI para melhorar a biblioteca e permitir o treinamento de modelos.
        planning: Planeja a execução do grupo e adiciona o plano ao grupo.
    """
    def __init__(self, caminho_config: str = "config/equipes.yaml"):
        self.caminho_config = Path(caminho_config)
        self.logger = LoggingConfig().get_logger(__name__)
        self.configuracoes = self._carregar_configuracoes()
        self.equipes: List[Crew] = []

    def _carregar_configuracoes(self) -> Dict:
        try:
            with open(self.caminho_config, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        except Exception as e:
            self.logger.error(f"Erro ao carregar configurações: {e}")
            raise

    def criar_equipes(
        self,
        agentes: List[Agent],
        tarefas: List[Task]
    ) -> List[Crew]:
        """Cria equipes com base nas configurações."""
        try:
            if not self.configuracoes.get('equipes'):
                raise ValueError("Nenhuma equipe encontrada nas configurações")

            self.logger.debug(f"Agentes disponíveis: {[a.role for a in agentes]}")
            self.logger.debug(f"Tarefas disponíveis: {[t.name for t in tarefas]}")

            for config in self.configuracoes['equipes']:
                self.logger.debug(f"Processando configuração de equipe: {config}")
                
                # Filtra tarefas especificadas na configuração
                tarefas_equipe = []
                if 'tasks' in config:
                    # Debug para verificar a correspondência de nomes
                    for task_name in config['tasks']:
                        self.logger.debug(f"Procurando tarefa: '{task_name}'")
                        for tarefa in tarefas:
                            self.logger.debug(f"Comparando com: '{tarefa.name}'")
                    
                    tarefas_equipe = [t for t in tarefas if t.name in config['tasks']]
                    self.logger.debug(f"Tarefas encontradas para a equipe: {[t.name for t in tarefas_equipe]}")
                
                if not tarefas_equipe and tarefas:
                    tarefas_equipe = tarefas
                    self.logger.info("Usando todas as tarefas disponíveis para a equipe")
                
                if not tarefas_equipe:
                    self.logger.warning("Nenhuma tarefa encontrada para a equipe")
                    continue

                # Configurações básicas
                crew_config = {
                    'process': getattr(Process, config.get('process', 'sequential')),
                    'verbose': config.get('verbose', True),
                    'agents': agentes,
                    'tasks': tarefas_equipe,
                }

                # Configurações opcionais
                optional_fields = [
                    'memory', 'cache', 'language', 'full_output',
                    'planning', 'max_rpm', 'share_crew'
                ]
                for field in optional_fields:
                    if field in config:
                        crew_config[field] = config[field]

                # Criação da equipe
                try:
                    equipe = Crew(**crew_config)
                    self.equipes.append(equipe)
                    self.logger.info(
                        f"Equipe criada com sucesso: {len(equipe.agents)} agentes, "
                        f"{len(equipe.tasks)} tarefas"
                    )
                except Exception as e:
                    self.logger.error(f"Erro ao criar equipe: {e}")
                    continue

            if not self.equipes:
                self.logger.warning("Nenhuma equipe foi criada")
                
            return self.equipes

        except Exception as e:
            self.logger.error(f"Erro ao criar equipes: {e}")
            raise

    def executar_equipes(
        self, 
        inputs: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Executa todas as equipes criadas e salva os resultados."""
        resultados = []
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        query_hash = md5(str(inputs).encode()).hexdigest()[:8] if inputs else "no_input"
        
        # Cria diretório para resultados se não existir
        diretorio_base = Path("resultados/execucoes")
        diretorio_base.mkdir(parents=True, exist_ok=True)
        
        for equipe in self.equipes:
            try:
                self.logger.info(f"Iniciando execução da equipe: {equipe}")
                crew_output = equipe.kickoff(inputs=inputs)
                
                # Coleta métricas e resultados
                metricas = equipe.calculate_usage_metrics()
                
                # Prepara resultado completo
                resultado = {
                    'raw_output': crew_output.raw,
                    'json_output': crew_output.json_dict if hasattr(crew_output, 'json_dict') else None,
                    'tasks_output': [task.output for task in equipe.tasks if task.output],
                    'metricas': metricas.model_dump(),
                    'equipe_id': str(equipe.id),
                    'timestamp': timestamp,
                    'query_hash': query_hash
                }
                
                # Salva resultado em arquivo
                nome_arquivo = f"arxiv_{timestamp}_{query_hash}_{equipe.id}.json"
                caminho_arquivo = diretorio_base / nome_arquivo
                
                with open(caminho_arquivo, 'w', encoding='utf-8') as f:
                    json.dump(resultado, f, ensure_ascii=False, indent=2)
                
                self.logger.info(f"Resultados salvos em: {caminho_arquivo}")
                resultados.append(resultado)
                
                self.logger.info(f"Execução concluída: {equipe}")
                
            except Exception as e:
                self.logger.error(f"Erro na execução da equipe {equipe}: {e}")
                raise
                
        return resultados

    def obter_equipes(self) -> List[Crew]:
        """Retorna lista de equipes criadas."""
        return self.equipes

if __name__ == "__main__":
    from dotenv import load_dotenv
    import tempfile
    import os
    from crewai_tools import SerperDevTool
    from src.agentes.agentes_genericos import GerenciadorAgentes
    from src.tarefas.tarefas_genericas import GerenciadorTarefas
    from src.modelos.pydantic_models import (  # Importando os modelos
    EventOutput,
    MarketAnalysis,
    NewsOutput
)
    from crewai import Process
    
    # Carrega variáveis de ambiente
    load_dotenv()
    
    # Configura logging
    logging_config = LoggingConfig()
    logger = logging_config.get_logger(__name__)
    
    def testar_equipes():
        """Testa a criação e execução de equipes"""
        temp_files = []
        try:
            # YAML de teste para agentes
            yaml_agentes = """
agentes:
  - role: "AI Research Specialist"
    quantidade: 2
    goal: "Realizar pesquisas aprofundadas sobre criptomoedas que são novas no mercado e ainda não foram adicionadas as corretoras centralizadas"
    backstory: "PhD em trading quantitativo com foco em pesquisa avançada"
    verbose: true
    allow_delegation: false
    tools:
      - name: "SerperDevTool"
        params:
          country: "br"
          locale: "pt-br"
          n_results: 5

  - role: "Data Analysis Expert"
    goal: "Analisar e sintetizar dados de pesquisa"
    backstory: "Especialista em análise de dados com 10 anos de experiência"
    verbose: true
    allow_delegation: false
    allow_code_execution: true
    code_execution_mode: "safe"
    tools:
      - name: "SerperDevTool"
        params:
          country: "br"
          locale: "pt-br"
          n_results: 5
      - name: "CodeInterpreterTool"
        params:
          unsafe_mode: false
"""

            # YAML de teste para tarefas
            yaml_tarefas = """
tasks:
  - name: "pesquisa_inicial"
    description: "Pesquisar últimas tendências em novas criptomoedas em 2024, que ainda não foram adicionadas as corretoras centralizadas"
    agent_role: "AI Research Specialist_1"
    expected_output: "Relatório detalhado sobre tendências de novas criptomoedas, que ainda não foram adicionadas as corretoras centralizadas"
    output_pydantic: "NewsOutput"
    tools:
      - name: "SerperDevTool"
        params:
          country: "br"
          locale: "pt-br"
          n_results: 5

  - name: "analise_dados"
    description: "Analisar dados da pesquisa inicial"
    agent_role: "Data Analysis Expert"
    expected_output: "Análise estruturada dos dados"
    output_pydantic: "MarketAnalysis"
    tools:
      - name: "SerperDevTool"
        params:
          country: "br"
          locale: "pt-br"
          n_results: 5
    context_tasks: ["pesquisa_inicial"]
"""

            # YAML de teste para equipes
            yaml_equipes = """
equipes:
  - name: "Equipe de Pesquisa Criptomoedas"
    description: "Equipe responsável por pesquisar e analisar tendências de novas criptomoedas, que ainda não foram adicionadas as corretoras centralizadas"
    process: "sequential"
    verbose: true
    memory: true
    cache: true
    planning: true
    max_rpm: 10
    language: "portuguese"
    tasks: ["pesquisa_inicial", "analise_dados"]
"""

            # Cria arquivos temporários
            for yaml_content, filename in [
                (yaml_agentes, "agentes.yaml"),
                (yaml_tarefas, "tarefas.yaml"),
                (yaml_equipes, "equipes.yaml")
            ]:
                with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', suffix='.yaml', delete=False) as temp_file:
                    temp_file.write(yaml_content)
                    temp_files.append((temp_file.name, filename))
                    logger.debug(f"Arquivo temporário criado: {temp_file.name}")
            
            # Inicializa gerenciadores com os arquivos temporários
            gerenciador_agentes = GerenciadorAgentes(temp_files[0][0])
            gerenciador_tarefas = GerenciadorTarefas(temp_files[1][0])
            gerenciador_equipes = GerenciadorEquipes(temp_files[2][0])
            
            # Obtém os agentes
            agentes = gerenciador_agentes.obter_agentes()
            
            # Cria as tarefas passando os agentes
            tarefas = gerenciador_tarefas.criar_tarefas(agentes)
            
            # Cria equipes
            equipes = gerenciador_equipes.criar_equipes(
                agentes=agentes,
                tarefas=tarefas
            )
            
            # Testes básicos
            assert len(equipes) > 0, "Nenhuma equipe criada"
            logger.info(f"✓ {len(equipes)} equipe(s) criada(s) com sucesso")
            
            # Testa cada equipe
            for equipe in equipes:
                # Verifica configurações básicas
                assert equipe.process == Process.sequential, "Processo deveria ser sequential"
                assert equipe.verbose is True, "Verbose deveria ser True"
                assert equipe.memory is True, "Memory deveria ser True"
                assert equipe.cache is True, "Cache deveria ser True"
                assert equipe.planning is True, "Planning deveria ser True"
                assert equipe.max_rpm == 10, "Max RPM deveria ser 10"
                
                # Verifica agentes e tarefas
                assert len(equipe.agents) > 0, "Equipe sem agentes"
                assert len(equipe.tasks) > 0, "Equipe sem tarefas"
                
                # Exibe configurações
                print(f"\nEquipe ID: {equipe.id}")
                print(f"Processo: {equipe.process}")
                print(f"Número de Agentes: {len(equipe.agents)}")
                print(f"Número de Tarefas: {len(equipe.tasks)}")
                print("Configurações:")
                print(f"  - Verbose: {equipe.verbose}")
                print(f"  - Memory: {equipe.memory}")
                print(f"  - Cache: {equipe.cache}")
                print(f"  - Planning: {equipe.planning}")
                print(f"  - Max RPM: {equipe.max_rpm}")
                print("-" * 50)
            
            # Testa execução
            logger.info("Testando execução das equipes...")
            resultados = gerenciador_equipes.executar_equipes(
                inputs={
                    "topic": "Inteligência Artificial",
                    "customer_domain": "ia-research.com"
                }
            )
            
            assert len(resultados) > 0, "Nenhum resultado retornado"
            for resultado in resultados:
                assert 'resultado' in resultado, "Resultado não contém output"
                assert 'metricas' in resultado, "Resultado não contém métricas"
                assert 'equipe_id' in resultado, "Resultado não contém ID da equipe"
            
            logger.info("✓ Execução das equipes concluída com sucesso")
            logger.info("✓ Todos os testes passaram com sucesso!")
            
        finally:
            # Limpa todos os arquivos temporários
            for temp_path, _ in temp_files:
                try:
                    os.unlink(temp_path)
                    logger.debug(f"Arquivo temporário removido: {temp_path}")
                except Exception as e:
                    logger.error(f"Erro ao remover arquivo temporário: {e}")
    
    # Executa os testes
    testar_equipes()

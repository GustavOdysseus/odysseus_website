from typing import Dict, List, Optional, Any, Type, Union
from pathlib import Path
import yaml
from pydantic import BaseModel
from crewai import Task, Agent
import crewai_tools
from crewai_tools import Tool
from src.logging.logging_config import LoggingConfig


class GerenciadorTarefas:
    """
    Gerenciador central para criação e administração de tarefas baseadas em YAML.

    Atributos:

        agent: Agente responsável pela execução da tarefa. Representa a entidade que realiza a tarefa.
        async_execution: Indicador booleano que determina se a execução da tarefa será assíncrona.
        callback: Função ou objeto executado após a conclusão da tarefa para realizar ações adicionais.
        config: Dicionário contendo os parâmetros de configuração específicos da tarefa.
        context: Lista de instâncias de Task que fornecem o contexto ou dados de entrada para a tarefa.
        description: Texto descritivo que detalha o propósito e a execução da tarefa.
        expected_output: Definição clara do resultado esperado da tarefa.
        output_file: Caminho do arquivo para armazenar o resultado da tarefa.
        output_json: Modelo Pydantic para estruturar o resultado em formato JSON.
        output_pydantic: Modelo Pydantic para o resultado da tarefa.
        tools: Lista de ferramentas ou recursos limitados para a execução da tarefa.
    """

    def __init__(self, caminho_config: str = "config/tarefas.yaml"):
        """Inicializa o gerenciador de tarefas."""
        # Inicializa o logger
        logging_config = LoggingConfig()
        self.logger = logging_config.get_logger(__name__)
        
        self.caminho_config = Path(caminho_config)
        self.tarefas: List[Task] = []
        self.configuracoes: Dict = {}
        self._carregar_configuracoes()

    def criar_tarefa(
        self,
        config_tarefa: Dict[str, Any],
        agente: Optional[Agent] = None
    ) -> Task:
        """
        Cria uma única tarefa com base na configuração fornecida.
        """
        try:
            # Validação de campos obrigatórios
            campos_obrigatorios = ["description", "expected_output"]
            for campo in campos_obrigatorios:
                if not config_tarefa.get(campo):
                    raise ValueError(f"{campo} é obrigatório para a tarefa")

            # Prepara as ferramentas
            tools = []
            if config_tarefa.get('tools'):
                tools = self._carregar_ferramentas(config_tarefa['tools'])

            # Configuração do output
            output_config = {}
            if config_tarefa.get('output_json'):
                output_config['output_json'] = True
            if config_tarefa.get('output_pydantic'):
                if isinstance(config_tarefa['output_pydantic'], str):
                    # Carrega a classe Pydantic pelo nome
                    model_class = self._carregar_modelo_pydantic(config_tarefa['output_pydantic'])
                    output_config['output_pydantic'] = model_class
            if config_tarefa.get('output_file'):
                output_config['output_file'] = config_tarefa['output_file']
                output_config['create_directory'] = config_tarefa.get('create_directory', True)

            # Criação da tarefa
            tarefa = Task(
                description=config_tarefa['description'],
                expected_output=config_tarefa['expected_output'],
                agent=agente,
                tools=tools,
                async_execution=config_tarefa.get('async_execution', False),
                context=config_tarefa.get('context'),
                config=config_tarefa.get('config'),
                callback=config_tarefa.get('callback'),
                human_input=config_tarefa.get('human_input', False),
                name=config_tarefa.get('name'),
                **output_config
            )
            
            self.logger.info(f"Tarefa criada: {tarefa.name or tarefa.description[:50]}...")
            return tarefa
            
        except Exception as e:
            self.logger.error(f"Erro ao criar tarefa: {e}")
            raise

    def criar_tarefas(self, agentes: Optional[List[Agent]] = None) -> List[Task]:
        """Cria múltiplas tarefas a partir do arquivo de configuração."""
        try:
            if not self.configuracoes.get('tasks'):
                self.logger.error("Nenhuma tarefa encontrada nas configurações")
                return []

            self.tarefas = []
            agentes_dict = {a.role: a for a in (agentes or [])}
            self.logger.debug(f"Agentes disponíveis: {list(agentes_dict.keys())}")

            for config_tarefa in self.configuracoes['tasks']:
                try:
                    # Associa agente se especificado
                    agente_role = config_tarefa.get('agent_role')
                    agente = agentes_dict.get(agente_role)
                    
                    if agente_role and not agente:
                        self.logger.warning(f"Agente '{agente_role}' não encontrado para tarefa '{config_tarefa.get('name')}'")
                        continue
                    
                    # Cria a tarefa
                    tarefa = self.criar_tarefa(config_tarefa, agente)
                    self.tarefas.append(tarefa)
                    self.logger.info(f"Tarefa '{tarefa.name}' criada com agente '{agente.role if agente else 'None'}'")
                    
                except Exception as e:
                    self.logger.error(f"Erro ao processar tarefa individual: {e}")
                    continue

            if not self.tarefas:
                self.logger.warning("Nenhuma tarefa foi criada com sucesso")
            else:
                self.logger.info(f"Total de tarefas criadas: {len(self.tarefas)}")
                
            return self.tarefas

        except Exception as e:
            self.logger.error(f"Erro ao criar tarefas: {e}")
            self.logger.exception("Traceback completo:")
            return []

    def _carregar_configuracoes(self) -> None:
        """Carrega as configurações das tarefas do arquivo YAML."""
        try:
            with open(self.caminho_config, 'r', encoding='utf-8') as arquivo:
                self.configuracoes = yaml.safe_load(arquivo)
        except Exception as e:
            self.logger.error(f"Erro ao carregar arquivo de configuração: {e}")
            raise

    def _carregar_modelo_pydantic(self, nome_modelo: str) -> Type[BaseModel]:
        """
        Carrega uma classe Pydantic pelo nome, buscando automaticamente
        todas as classes que herdam de BaseModel no módulo pydantic_models.
        
        Args:
            nome_modelo: Nome do modelo Pydantic a ser carregado

        Returns:
            Type[BaseModel]: Classe do modelo Pydantic

        Raises:
            ValueError: Se o modelo não for encontrado
        """
        import inspect
        from src.modelos import pydantic_models
        
        # Obtém todas as classes do módulo que herdam de BaseModel
        modelos_disponiveis = {
            name: cls for name, cls in inspect.getmembers(pydantic_models, inspect.isclass)
            if issubclass(cls, BaseModel) and cls != BaseModel
        }
        
        if nome_modelo not in modelos_disponiveis:
            raise ValueError(
                f"Modelo Pydantic '{nome_modelo}' não encontrado. "
                f"Modelos disponíveis: {list(modelos_disponiveis.keys())}"
            )
        
        self.logger.debug(f"Carregando modelo Pydantic: {nome_modelo}")
        return modelos_disponiveis[nome_modelo]

    def obter_tarefas(self) -> List[Task]:
        """Retorna a lista de tarefas criadas."""
        return self.tarefas

    def _carregar_ferramentas(self, config_ferramentas: List[Union[str, Dict]]) -> List[Tool]:
        """
        Carrega ferramentas dinamicamente baseado na configuração.
        Suporta tanto ferramentas nativas do crewai quanto ferramentas customizadas.

        Args:
            config_ferramentas: Lista de strings (nomes das ferramentas) ou dicionários (configuração detalhada)

        Returns:
            List[Tool]: Lista de ferramentas instanciadas
        """
        import importlib
        import inspect
        from crewai.tools.base_tool import BaseTool
        
        
        ferramentas = []
        
        try:
            # Tenta importar ferramentas customizadas
            custom_tools = importlib.import_module('src.ferramentas')
        except ImportError:
            custom_tools = None
            self.logger.debug("Módulo de ferramentas customizadas não encontrado")

        for ferramenta_config in config_ferramentas:
            try:
                # Processa configuração da ferramenta
                if isinstance(ferramenta_config, str):
                    nome_ferramenta = ferramenta_config
                    params = {}
                else:
                    nome_ferramenta = ferramenta_config['name']
                    params = ferramenta_config.get('params', {})

                # Busca primeiro em ferramentas customizadas
                ferramenta_class = None
                if custom_tools:
                    ferramenta_class = getattr(custom_tools, nome_ferramenta, None)

                # Se não encontrar, busca nas ferramentas nativas do crewai
                if not ferramenta_class:
                    ferramenta_class = getattr(crewai_tools, nome_ferramenta, None)

                if not ferramenta_class:
                    self.logger.warning(f"Ferramenta '{nome_ferramenta}' não encontrada")
                    continue

                # Verifica se a classe é uma ferramenta válida
                if not (inspect.isclass(ferramenta_class) and issubclass(ferramenta_class, BaseTool)):
                    self.logger.warning(f"'{nome_ferramenta}' não é uma ferramenta válida")
                    continue

                # Instancia a ferramenta com os parâmetros fornecidos
                ferramenta = ferramenta_class(**params)
                ferramentas.append(ferramenta)
                self.logger.debug(f"Ferramenta carregada: {nome_ferramenta}")

            except Exception as e:
                self.logger.error(f"Erro ao carregar ferramenta '{nome_ferramenta}': {e}")
                continue

        return ferramentas

if __name__ == "__main__":
    from dotenv import load_dotenv
    import tempfile
    import os
    from src.agentes.agentes_genericos import GerenciadorAgentes
    
    # Carrega variáveis de ambiente
    load_dotenv()
    
    # Configura logging
    logging_config = LoggingConfig(
        log_level="DEBUG",
        console_format="%(asctime)s - %(levelname)s - %(message)s"
    )
    logger = logging_config.get_logger(__name__)
    
    # YAML de teste para agentes
    yaml_agentes = """
    agentes:
      - role: "Pesquisador"
        quantidade: 2
        goal: "Realizar pesquisas aprofundadas sobre mercados e tendências"
        backstory: "Analista experiente com histórico em pesquisa de mercado"
        verbose: true
        tools:
          - name: "SerperDevTool"
            params:
              country: "br"
              locale: "pt-br"
              n_results: 5
          - "FileReadTool"
        
      - role: "Analista"
        goal: "Analisar dados e gerar insights acionáveis"
        backstory: "Especialista em análise de dados com foco em mercados financeiros"
        verbose: true
        tools:
          - name: "JSONSearchTool"
          - name: "CSVSearchTool"
    """
    
    # YAML de teste para tarefas
    yaml_tarefas = """
    tasks:
      - name: "Pesquisa de Mercado"
        description: "Pesquisar as últimas tendências do mercado de criptomoedas"
        expected_output: "Lista com as 5 principais tendências identificadas"
        agent_role: "Pesquisador_1"
        tools:
          - name: "SerperDevTool"
            params:
              country: "br"
              locale: "pt-br"
              n_results: 5
          - "FileReadTool"
        output_pydantic: "MarketAnalysis"
        output_file: "outputs/market_research.json"
        config:
          search_query: "crypto market trends 2024"
        async_execution: false
        human_input: false
        
      - name: "Análise de Dados"
        description: "Analisar os dados coletados e identificar padrões relevantes"
        expected_output: "Relatório detalhado com análise e recomendações"
        agent_role: "Analista"
        tools:
          - name: "JSONSearchTool"
            params:
              json_path: "outputs/market_research.json"
              search_query: "principais tendências e padrões identificados"
        output_pydantic: "MarketAnalysis"
        output_file: "outputs/market_analysis.json"
        async_execution: false
        human_input: true
        context_tasks: ["Pesquisa de Mercado"]
    """
    
    def executar_teste():
        try:
            # Cria arquivos temporários
            with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False, encoding='utf-8') as temp_agentes:
                temp_agentes.write(yaml_agentes)
                agentes_path = temp_agentes.name
                
            with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False, encoding='utf-8') as temp_tarefas:
                temp_tarefas.write(yaml_tarefas)
                tarefas_path = temp_tarefas.name
            
            # Cria os agentes
            logger.info("Iniciando criação dos agentes...")
            gerenciador_agentes = GerenciadorAgentes(agentes_path)
            agentes = gerenciador_agentes.obter_agentes()
            
            # Cria as tarefas
            logger.info("Iniciando criação das tarefas...")
            gerenciador_tarefas = GerenciadorTarefas(tarefas_path)
            tarefas = gerenciador_tarefas.criar_tarefas(agentes)
            
            # Exibe informações das tarefas criadas
            print("\nTarefas criadas:")
            print("=" * 50)
            
            for tarefa in tarefas:
                print(f"\nNome: {tarefa.name}")
                print(f"Agente: {tarefa.agent.role if tarefa.agent else 'Nenhum'}")
                print(f"Ferramentas: {[tool.name for tool in tarefa.tools]}")
                
                if tarefa.context:
                    print(f"Contexto: {[ctx.name for ctx in tarefa.context]}")
                
                if tarefa.config:
                    print("Configurações:")
                    for key, value in tarefa.config.items():
                        print(f"  - {key}: {value}")
                
                print("-" * 30)
            
            print(f"\nTotal de tarefas criadas: {len(tarefas)}")
            return True
            
        except Exception as e:
            logger.error(f"Erro durante o teste: {e}")
            logger.exception("Traceback completo:")
            return False
            
        finally:
            # Limpa arquivos temporários
            try:
                os.unlink(agentes_path)
                os.unlink(tarefas_path)
                logger.debug("Arquivos temporários removidos com sucesso")
            except Exception as e:
                logger.error(f"Erro ao remover arquivos temporários: {e}")
    
    # Executa o teste
    sucesso = executar_teste()
    if sucesso:
        print("\nTeste concluído com sucesso!")
    else:
        print("\nTeste falhou!")

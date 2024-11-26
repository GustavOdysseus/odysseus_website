from typing import Dict, List, Optional, Any, Type, Callable, Union
import yaml
from pathlib import Path
from crewai import Agent, LLM
import os
from src.logging.logging_config import LoggingConfig


class GerenciadorAgentes:
    """
    Gerenciador para criação e administração de agentes baseados em configurações YAML.
    
    Esta classe é responsável por carregar configurações de um arquivo YAML e criar
    instâncias de agentes com base nessas configurações. Ela suporta todos os parâmetros
    disponíveis na biblioteca CrewAI para configuração de agentes.

    Atributos:
        caminho_config (Path): Caminho para o arquivo YAML de configuração
        agentes (List[Agent]): Lista de agentes criados
        configuracoes (Dict): Dicionário com as configurações carregadas do YAML

    Parâmetros dos Agentes:
        Obrigatórios:
            role (str): Define a função do agente dentro da equipe
            goal (str): Objetivo individual que o agente visa alcançar
            backstory (str): Contexto e história do agente que enriquece sua interação
        
        Opcionais:
            llm (str): Modelo de linguagem a ser usado (default: valor de OPENAI_MODEL_NAME ou 'gpt-4-mini')
            tools (List): Lista de ferramentas disponíveis para o agente (default: [])
            function_calling_llm: Modelo específico para chamada de funções (default: None)
            max_iter (int): Número máximo de iterações antes de forçar resposta (default: 25)
            max_rpm (int): Máximo de requisições por minuto (default: None)
            max_execution_time (int): Tempo máximo de execução em segundos (default: None)
            verbose (bool): Ativa logs detalhados (default: False)
            allow_delegation (bool): Permite delegação de tarefas (default: False)
            step_callback (Callable): Função chamada após cada etapa (default: None)
            cache (bool): Ativa cache para uso de ferramentas (default: True)
            system_template (str): Template personalizado do sistema (default: None)
            prompt_template (str): Template personalizado de prompt (default: None)
            response_template (str): Template personalizado de resposta (default: None)
            allow_code_execution (bool): Permite execução de código (default: False)
            max_retry_limit (int): Tentativas máximas em caso de erro (default: 2)
            use_system_prompt (bool): Usa prompt do sistema (default: True)
            respect_context_window (bool): Respeita limite da janela de contexto (default: True)
            code_execution_mode (str): Modo de execução de código ('safe'|'unsafe') (default: 'safe')

    Configuração de Múltiplos Agentes:
        quantidade (int): Número de instâncias do agente a serem criadas com a mesma configuração.
                         Útil para implementar técnicas de enxame. (default: 1)
                         
    Exemplo de YAML:
        agentes:
          - role: "Pesquisador"
            quantidade: 3
            goal: "Realizar pesquisas..."
            backstory: "Especialista em..."
            [... outras configurações ...]

    Configurações do LLM:
        model (str): Nome do modelo a ser usado (ex: "gpt-4o-mini", "gpt-3.5-turbo")
        timeout (Union[float, int]): Tempo máximo em segundos para aguardar resposta
        temperature (float): Controla aleatoriedade (0.0 a 1.0)
        top_p (float): Controla diversidade da saída (0.0 a 1.0)
        n (int): Número de completions a serem geradas
        stop (Union[str, List[str]]): Sequência(s) onde a geração deve parar
        max_tokens (int): Número máximo de tokens a serem gerados
        presence_penalty (float): Penaliza tokens baseado em presença
        frequency_penalty (float): Penaliza tokens baseado em frequência
        logit_bias (Dict[int, float]): Modifica probabilidade de tokens
        seed (int): Seed aleatória para resultados determinísticos
        logprobs (bool): Retorna log probabilities dos tokens
        top_logprobs (int): Número de tokens para retornar log probabilities
        api_key (str): Chave de API para autenticação
    """

    def __init__(self, caminho_config: str = "config/agentes.yaml"):
        """
        Inicializa o gerenciador de agentes.
        
        Args:
            caminho_config: Caminho para o arquivo YAML de configuração dos agentes
        """
        # Inicializa o logger
        logging_config = LoggingConfig()
        self.logger = logging_config.get_logger(__name__)
        
        self.caminho_config = Path(caminho_config)
        self.agentes: List[Agent] = []
        self.configuracoes: Dict = {}
        self._carregar_configuracoes()
        self._criar_agentes()
        
    def _carregar_configuracoes(self) -> None:
        """
        Carrega as configurações dos agentes do arquivo YAML.
        
        O arquivo YAML deve conter uma chave 'agentes' com uma lista de configurações,
        onde cada configuração representa um agente com seus respectivos parâmetros.
        
        Raises:
            FileNotFoundError: Se o arquivo não existir
            yaml.YAMLError: Se houver erro na sintaxe do YAML
            Exception: Para outros erros durante a leitura do arquivo
        """
        try:
            with open(self.caminho_config, 'r', encoding='utf-8') as arquivo:
                self.configuracoes = yaml.safe_load(arquivo)
        except FileNotFoundError:
            self.logger.error(f"Arquivo de configuração não encontrado: {self.caminho_config}")
            raise
        except yaml.YAMLError as e:
            self.logger.error(f"Erro na sintaxe do YAML: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Erro ao carregar arquivo de configuração: {e}")
            raise
            
    def _criar_configuracao_llm(self, config: Dict) -> LLM:
        """Cria uma configuração de LLM com base nas configurações do agente."""
        llm_config = config.get('llm', {})
        
        return LLM(
            model=llm_config.get('model', os.getenv('OPENAI_MODEL_NAME', 'gpt-4o-mini')),
            temperature=float(llm_config.get('temperature', os.getenv('OPENAI_TEMPERATURE', 1.0))),
            max_tokens=int(llm_config.get('max_tokens', os.getenv('OPENAI_MAX_TOKENS', 16000))),
            top_p=float(llm_config.get('top_p', os.getenv('OPENAI_TOP_P', 1.0))),
            presence_penalty=float(llm_config.get('presence_penalty', os.getenv('OPENAI_PRESENCE_PENALTY', 0.0))),
            frequency_penalty=float(llm_config.get('frequency_penalty', os.getenv('OPENAI_FREQUENCY_PENALTY', 0.0))),
            timeout=int(llm_config.get('timeout', os.getenv('OPENAI_TIMEOUT', 60))),
            api_key=os.getenv('OPENAI_API_KEY')
        )

    def _criar_agentes(self) -> None:
        """Cria os agentes com base nas configurações."""
        if not self.configuracoes.get('agentes'):
            self.logger.error("Nenhum agente encontrado nas configurações")
            return

        for config in self.configuracoes['agentes']:
            try:
                quantidade = config.get('quantidade', 1)
                
                for i in range(quantidade):
                    role_final = f"{config['role']}_{i+1}" if quantidade > 1 else config['role']
                    
                    try:
                        # Configuração do agente com atributos essenciais
                        agent_config = {
                            'role': role_final,
                            'goal': config['goal'],
                            'backstory': config['backstory'],
                            'llm': self._criar_configuracao_llm(config),
                            'verbose': config.get('verbose', False),
                            'allow_delegation': config.get('allow_delegation', False),
                            'max_iter': config.get('max_iter', 20),
                            'max_rpm': config.get('max_rpm'),
                            'max_execution_time': config.get('max_execution_time'),
                            'step_callback': config.get('step_callback'),
                            'use_system_prompt': config.get('use_system_prompt', True),
                            'respect_context_window': config.get('respect_context_window', True),
                            'max_retry_limit': config.get('max_retry_limit', 2),
                            'tools': []  # Será configurado posteriormente
                        }
                        
                        # Configurações opcionais
                        if config.get('allow_code_execution'):
                            agent_config.update({
                                'allow_code_execution': True,
                                'code_execution_mode': config.get('code_execution_mode', 'safe')
                            })
                        
                        # Templates personalizados
                        for template in ['system_template', 'prompt_template', 'response_template']:
                            if config.get(template):
                                agent_config[template] = config[template]
                        
                        # Criação do agente
                        agente = Agent(**agent_config)
                        self.agentes.append(agente)
                        self.logger.info(f"Agente criado com sucesso: {role_final}")
                        
                    except Exception as e:
                        self.logger.error(f"Erro ao criar agente {role_final}: {e}")
                        raise
                    
            except Exception as e:
                self.logger.error(f"Erro ao processar configuração do agente: {e}")
                raise

    def obter_agentes(self) -> List[Agent]:
        """
        Retorna a lista de agentes criados.
        
        Returns:
            List[Agent]: Lista contendo todos os agentes criados com sucesso
        """
        return self.agentes


if __name__ == "__main__":
    from dotenv import load_dotenv
    import tempfile
    from crewai_tools import SerperDevTool
    
    # Carrega as variáveis de ambiente
    load_dotenv()
    
    # Configura logging
    logging_config = LoggingConfig()
    logger = logging_config.get_logger(__name__)
    
    # Configura o LLM
    llm = LLM(
        model=os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini"),
        temperature=float(os.getenv("OPENAI_TEMPERATURE", 1.0)),
        max_tokens=int(os.getenv("OPENAI_MAX_TOKENS", 30000)),
        top_p=float(os.getenv("OPENAI_TOP_P", 1.0)),
        presence_penalty=float(os.getenv("OPENAI_PRESENCE_PENALTY", 0.0)),
        frequency_penalty=float(os.getenv("OPENAI_FREQUENCY_PENALTY", 0.0)),
        timeout=int(os.getenv("OPENAI_TIMEOUT", 60)),
        api_key=os.getenv("OPENAI_API_KEY")
    )
    logger.debug(f"LLM configurado: {llm}")
    
    # Inicializa a ferramenta de busca
    search_tool = SerperDevTool(
        country="br",
        locale="pt-br",
        n_results=5,
        save_file=True
    )
    logger.debug(f"Ferramenta de busca criada: {search_tool}")
    
    def testar_criacao_agentes():
        """Testa a criação básica de agentes"""
        yaml_teste = r"""
        agentes:
          - role: "Pesquisador"
            quantidade: 2
            goal: "Realizar pesquisas aprofundadas em artigos cientificos e repositorios de codigo"
            backstory: "PhD em Ciencia da Computacao com especializacao em IA e analise de dados"
            verbose: true
            allow_delegation: true
            max_iter: 25
            tools: []
            
          - role: "Analisador"
            goal: "Analisar e sintetizar informacoes coletadas, identificando padroes e insights"
            backstory: "Especialista em analise de dados com vasta experiencia em processamento de informacoes"
            verbose: true
            max_iter: 30
            allow_code_execution: true
            code_execution_mode: "safe"
            tools: []
        """
        
        # Cria arquivo temporário para teste
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', suffix='.yaml', delete=False) as temp_file:
            temp_file.write(yaml_teste)
            temp_path = temp_file.name
        
        try:
            # Testa criação do gerenciador
            logger.info("Teste 1: Criação básica de agentes")
            gerenciador = GerenciadorAgentes(temp_path)
            
            # Configura agentes
            for agente in gerenciador.agentes:
                agente.llm = llm
                agente.tools.append(search_tool)
            
            # Verifica número de agentes
            total_agentes = len(gerenciador.obter_agentes())
            esperado = 3  # 2 Pesquisadores + 1 Analisador
            assert total_agentes == esperado, f"Esperado {esperado} agentes, mas foram criados {total_agentes}"
            logger.info(f"✓ Número correto de agentes criados: {total_agentes}")
            
            # Verifica configurações dos agentes
            for agente in gerenciador.obter_agentes():
                assert agente.llm is not None, f"LLM não configurado para {agente.role}"
                assert len(agente.tools) > 0, f"Ferramentas não configuradas para {agente.role}"
                assert agente.verbose is True, "Verbose deveria ser True"
                logger.info(f"✓ Agente {agente.role} configurado corretamente")
                
                # Exibe configurações
                print(f"\nRole: {agente.role}")
                print(f"Goal: {agente.goal}")
                print(f"Backstory: {agente.backstory}")
                print("LLM Configurações:")
                llm_config = {
                    "model": agente.llm.model,
                    "temperature": agente.llm.temperature,
                    "max_tokens": agente.llm.max_tokens,
                    "top_p": agente.llm.top_p,
                    "presence_penalty": agente.llm.presence_penalty,
                    "frequency_penalty": agente.llm.frequency_penalty,
                    "timeout": agente.llm.timeout,
                }
                for key, value in llm_config.items():
                    if value is not None:
                        print(f"  - {key}: {value}")
                print(f"Verbose: {agente.verbose}")
                print(f"Tools: {[t.name for t in agente.tools]}")
                print("-" * 50)
            
            logger.info("✓ Todos os testes passaram com sucesso!")
            
        except AssertionError as e:
            logger.error(f"Falha no teste: {e}")
            raise
        except Exception as e:
            logger.error(f"Erro durante os testes: {e}")
            logger.exception("Traceback completo:")
            raise
        finally:
            try:
                os.unlink(temp_path)
                logger.debug("Arquivo temporário removido com sucesso")
            except Exception as e:
                logger.error(f"Erro ao remover arquivo temporário: {e}")
    
    # Executa os testes
    testar_criacao_agentes()

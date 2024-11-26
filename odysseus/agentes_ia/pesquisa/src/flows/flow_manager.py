from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any, Set, Callable
import asyncio
import logging
import yaml
import json
import uuid
from hashlib import md5
from pathlib import Path
from crewai import Crew
from crewai.flow.flow import Flow, start, listen
from src.logging.logging_config import LoggingConfig
from src.modelos.pydantic_models import (
    EventPriority, EventType, MetricType, Metric, Decision,
    FlowEvent, CrewState, AnalysisCache, ConditionType,
    ExecutionCondition, TimedEventType, TimedEvent,
    PropagationRule, FeedbackType, FeedbackStatus,
    Feedback, RollbackType, RollbackEvent, FlowState
)


class EventPropagation(BaseModel):
    """Sistema de propagação de eventos."""
    type: EventType
    source: str
    propagation_rules: List[Dict[str, Any]] = Field(default_factory=list)
    max_depth: int = 3
    current_depth: int = 0
    visited_crews: Set[str] = Field(default_factory=set)

    model_config = {
        "arbitrary_types_allowed": True
    }


class FlowManager(Flow[FlowState]):
    """
    Gerenciador avançado de flows com suporte a eventos e feedback loops.
    
    Este gerenciador implementa um sistema complexo para coordenação de equipes de IA,
    incluindo:
    
    Funcionalidades:
        - Gestão de estado distribuído
        - Sistema de eventos com prioridades
        - Feedback multi-direcional
        - Cache de análises
        - Checkpoints e rollbacks
        - Propagação de eventos
        - Execução condicional
        - Eventos temporizados
        
    Atributos:
        logger: Logger configurado para o flow
        config: Configurações carregadas do arquivo
        _state (FlowState): Estado global do flow
        event_handlers: Handlers para diferentes tipos de eventos
        event_queue: Fila assíncrona de eventos
        timed_event_task: Task para processamento de eventos temporizados
        
    O FlowManager é projetado para suportar operações complexas entre múltiplas
    equipes de IA, mantendo consistência, rastreabilidade e capacidade de
    recuperação de falhas.
    """
    
    def __init__(
            self,
            caminho_config: str,
            flow_name: str,
            event_handlers: Optional[Dict[EventType, Callable]] = None
        ):
        """Inicializa o FlowManager."""
        super().__init__()
        self.logger = LoggingConfig().get_logger(__name__)
        self.config = self._carregar_configuracao(caminho_config, flow_name)
        self._state = FlowState()
        self.event_handlers = event_handlers or {}
        self.event_queue = asyncio.Queue()
        self.timed_event_task = None
        
    @property
    def state(self) -> FlowState:
        """Obtém o estado atual do flow."""
        return self._state
        
    @state.setter
    def state(self, value: FlowState):
        """Define um novo estado para o flow."""
        self._state = value
        
    def _carregar_configuracao(self, caminho_config: str, flow_name: str) -> Dict:
        """
        Carrega a configuração do flow a partir do arquivo YAML.
        
        Args:
            caminho_config: Caminho para o diretório de configuração
            flow_name: Nome do flow a ser carregado
            
        Returns:
            Dict: Configuração carregada
        """
        try:
            # Primeiro carrega o arquivo de configuração principal
            config_path = Path(caminho_config) / "config.yaml"
            with open(config_path, 'r', encoding='utf-8') as f:
                system_config = yaml.safe_load(f)

            # Verifica se o flow existe na configuração
            if flow_name not in system_config.get('flows', {}):
                raise ValueError(f"Flow '{flow_name}' não encontrado na configuração do sistema")

            # Obtém a configuração específica do flow
            flow_config = system_config['flows'][flow_name]
            
            # Carrega o arquivo de configuração do flow
            flow_file = Path(caminho_config) / flow_config['flow_config']
            with open(flow_file, 'r', encoding='utf-8') as f:
                flows_config = yaml.safe_load(f)
                
            # Carrega o arquivo de dependências
            deps_file = Path(caminho_config) / flow_config['dependencies']
            with open(deps_file, 'r', encoding='utf-8') as f:
                deps_config = yaml.safe_load(f)
                
            # Verifica se o flow existe na configuração do flow
            if 'flows' not in flows_config or flow_name not in flows_config['flows']:
                raise ValueError(f"Flow '{flow_name}' não encontrado no arquivo {flow_file}")
                
            # Combina configurações
            config = {
                'flow': flows_config['flows'][flow_name],
                'dependencies': deps_config.get('dependencies', {}),
                'system': system_config.get('system', {})
            }
            
            return config
            
        except Exception as e:
            self.logger.error(f"Erro ao carregar configuração: {str(e)}")
            raise
            
    async def _processar_eventos(self):
        """
        Processa eventos na fila de forma assíncrona.
        
        Este método implementa um loop contínuo que:
        1. Monitora a fila de eventos
        2. Processa eventos por ordem de prioridade
        3. Gerencia propagação de eventos
        4. Lida com erros durante processamento
        
        O processamento é feito de forma assíncrona para não
        bloquear outras operações do sistema.
        """
        while True:
            try:
                event = await self.event_queue.get()
                
                # Processa evento com base em sua prioridade
                if event.priority == EventPriority.CRITICAL:
                    await self._handle_event(event)
                else:
                    asyncio.create_task(self._handle_event(event))
                    
                self.event_queue.task_done()
                
            except Exception as e:
                self.logger.error(f"Erro ao processar evento: {str(e)}")
                continue

    async def _handle_event(self, event: FlowEvent):
        """
        Processa um evento específico e inicia sua propagação.
        
        Args:
            event (FlowEvent): Evento a ser processado
            
        O método:
        1. Registra o evento no histórico
        2. Executa handler específico se existir
        3. Inicia propagação do evento
        4. Processa feedback se necessário
        """
        try:
            # Registra evento no histórico
            self.state.event_history.append(event)
            
            # Executa handler específico se existir
            if event.type in self.event_handlers:
                await self.event_handlers[event.type](event)
                
            # Processa feedback se for evento de feedback
            if event.type == EventType.FEEDBACK:
                await self._processar_feedback(event)
                
            # Inicia propagação do evento
            propagation = EventPropagation(
                type=event.type,
                source=event.source
            )
            await self._propagar_evento(event, propagation)
            
        except Exception as e:
            self.logger.error(f"Erro ao processar evento {event.type}: {str(e)}")
            
            # Gera evento de erro
            error_event = FlowEvent(
                type=EventType.ERROR,
                source=event.source,
                priority=EventPriority.HIGH,
                data={'error': str(e), 'original_event': event}
            )
            await self.event_queue.put(error_event)

    async def _processar_feedback(self, event: FlowEvent):
        """
        Processa feedback multi-direcional entre equipes.
        
        Este método implementa um sistema sofisticado de processamento de feedback que:
        - Converte eventos em objetos Feedback estruturados
        - Aplica regras de propagação de feedback
        - Gerencia transformações de conteúdo
        - Controla requisitos de resposta
        - Notifica equipes alvo
        
        Args:
            event (FlowEvent): Evento contendo informações do feedback
        
        O feedback é processado seguindo estas etapas:
        1. Criação do objeto Feedback com metadados
        2. Registro no histórico
        3. Aplicação de regras de transformação
        4. Propagação para equipes alvo
        5. Atualização de estados
        6. Notificação de eventos
        
        """
        try:
            # Cria objeto Feedback estruturado
            feedback = Feedback(
                type=event.data.get('feedback_type', FeedbackType.SUGGESTION),
                priority=event.priority,
                source_crew=event.source,
                target_crews=event.data.get('target_crews', []),
                content=event.data.get('content', {}),
                requires_response=event.data.get('requires_response', False),
                metrics=event.metrics
            )
            
            # Registra no histórico
            self.state.feedback_history.append(feedback)
            
            # Aplica regras de transformação
            crew_rules = self.state.feedback_rules.get(event.source, [])
            for rule in crew_rules:
                if rule.get('condition')(feedback):
                    feedback = rule.get('transform')(feedback)
                    
            # Propaga para equipes alvo
            for target_crew in feedback.target_crews:
                await self._notificar_crew_feedback(target_crew, feedback)
                
                # Atualiza estado da equipe
                if target_crew in self.state.crew_states:
                    self.state.crew_states[target_crew].update({
                        'last_feedback': feedback.dict(),
                        'feedback_status': feedback.status
                    })
                    
            # Gera evento de feedback processado
            processed_event = FlowEvent(
                type=EventType.STATE_CHANGE,
                source=event.source,
                data={
                    'feedback_id': feedback.id,
                    'status': feedback.status
                }
            )
            await self.event_queue.put(processed_event)
            
        except Exception as e:
            self.logger.error(f"Erro ao processar feedback: {str(e)}")
            # Gera evento de erro
            error_event = FlowEvent(
                type=EventType.ERROR,
                source=event.source,
                priority=EventPriority.HIGH,
                data={'error': str(e), 'original_event': event}
            )
            await self.event_queue.put(error_event)

    async def _notificar_crew_feedback(self, crew_id: str, feedback: Feedback):
        """
        Notifica uma equipe sobre novo feedback.
        
        Args:
            crew_id (str): ID da equipe a ser notificada
            feedback (Feedback): Objeto Feedback a ser entregue
        """
        try:
            # Gera evento de notificação
            notification_event = FlowEvent(
                type=EventType.STATE_CHANGE,
                source='system',
                target=crew_id,
                priority=feedback.priority,
                data={
                    'type': 'feedback_notification',
                    'feedback': feedback.dict()
                }
            )
            await self.event_queue.put(notification_event)
            
            # Atualiza status do feedback
            feedback.status = FeedbackStatus.ACKNOWLEDGED
            
        except Exception as e:
            self.logger.error(f"Erro ao notificar equipe {crew_id}: {str(e)}")

    async def _processar_eventos_temporizados(self):
        """
        Processa eventos temporizados no sistema.
        
        Implementa um loop contínuo que:
        - Monitora eventos agendados
        - Processa eventos no momento correto
        - Gerencia eventos recorrentes
        - Lida com deadlines e timeouts
        
        Comportamentos:
        - Eventos regulares são processados no tempo agendado
        - Eventos recorrentes são reagendados automaticamente
        - Eventos com deadline geram timeouts quando expiram
        - Eventos não recorrentes são removidos após execução
        
        O processador verifica eventos a cada segundo e mantém
        consistência mesmo com múltiplos eventos simultâneos.
        """
        while True:
            try:
                now = datetime.now()
                events_to_remove = []
                
                for timed_event in self.state.timed_events:
                    if now >= timed_event.scheduled_time:
                        # Processa evento
                        await self.event_queue.put(timed_event.event)
                        
                        # Gerencia eventos recorrentes
                        if (timed_event.type == TimedEventType.RECURRING and 
                            timed_event.recurring_interval):
                            # Reagenda próxima execução
                            timed_event.scheduled_time = now + timed_event.recurring_interval
                            timed_event.last_execution = now
                        else:
                            # Remove eventos não recorrentes após execução
                            events_to_remove.append(timed_event)
                            
                    # Verifica deadlines
                    elif (timed_event.type == TimedEventType.DEADLINE and 
                          now >= timed_event.event.deadline):
                        # Gera evento de timeout
                        timeout_event = FlowEvent(
                            type=EventType.TIMEOUT,
                            source=timed_event.event.source,
                            priority=EventPriority.HIGH,
                            data={
                                'original_event': timed_event.event.dict(),
                                'deadline': timed_event.event.deadline
                            }
                        )
                        await self.event_queue.put(timeout_event)
                        events_to_remove.append(timed_event)
                        
                    # Gerencia retries
                    elif (timed_event.type == TimedEventType.RETRY and 
                          timed_event.max_retries and 
                          timed_event.current_retries >= timed_event.max_retries):
                        # Gera evento de erro após máximo de tentativas
                        error_event = FlowEvent(
                            type=EventType.ERROR,
                            source=timed_event.event.source,
                            priority=EventPriority.HIGH,
                            data={
                                'error': 'Máximo de tentativas excedido',
                                'original_event': timed_event.event.dict(),
                                'retries': timed_event.current_retries
                            }
                        )
                        await self.event_queue.put(error_event)
                        events_to_remove.append(timed_event)
                        
                # Remove eventos processados
                for event in events_to_remove:
                    self.state.timed_events.remove(event)
                    
                # Aguarda 1 segundo antes da próxima verificação
                await asyncio.sleep(1)
                
            except Exception as e:
                self.logger.error(f"Erro ao processar eventos temporizados: {str(e)}")
                await asyncio.sleep(1)  # Aguarda antes de tentar novamente

    async def agendar_evento(
        self,
        event: FlowEvent,
        scheduled_time: datetime,
        event_type: TimedEventType = TimedEventType.SCHEDULED,
        recurring_interval: Optional[timedelta] = None,
        max_retries: Optional[int] = None
    ):
        """
        Agenda um evento para execução futura.
        
        Args:
            event (FlowEvent): Evento a ser agendado
            scheduled_time (datetime): Momento para execução
            event_type (TimedEventType): Tipo de evento temporizado
            recurring_interval (timedelta, opcional): Intervalo para eventos recorrentes
            max_retries (int, opcional): Número máximo de tentativas
        
        O método:
        1. Cria um TimedEvent com os parâmetros fornecidos
        2. Adiciona à lista de eventos temporizados
        3. Inicia o processador de eventos se necessário
        
        Tipos de eventos suportados:
        - SCHEDULED: Evento único agendado
        - RECURRING: Evento que se repete periodicamente
        - DEADLINE: Evento com prazo limite
        - TIMEOUT: Evento de timeout
        - RETRY: Evento com tentativas múltiplas
        """
        timed_event = TimedEvent(
            type=event_type,
            scheduled_time=scheduled_time,
            event=event,
            recurring_interval=recurring_interval,
            max_retries=max_retries
        )
        self.state.timed_events.append(timed_event)
        
        # Inicia processador de eventos temporizados se necessário
        if self.timed_event_task is None:
            self.timed_event_task = asyncio.create_task(
                self._processar_eventos_temporizados()
            )
        
    @start()
    async def inicializar_flow(self, crews: List[Crew], inputs: Dict[str, Any]):
        """Inicializa o flow com múltiplas equipes."""
        self.state.execution_context.update(inputs)
        
        # Inicia processador de eventos
        asyncio.create_task(self._processar_eventos())
        
        for crew in crews:
            crew_id = str(crew.id)
            self.state.active_crews.append(crew_id)
            self.state.crew_states[crew_id] = {
                'status': 'initialized',
                'last_execution': None,
                'results': None
            }
            
        return self.state
            
    async def _executar_crew(self, crew: Crew) -> Dict:
        """
        Executa uma equipe com gestão completa de estado e eventos.
        
        Args:
            crew (Crew): Equipe a ser executada
        
        Returns:
            Dict: Resultado da execução da equipe
        
        Este método implementa:
        1. Verificação de condições de execução
        2. Gestão de estado da equipe
        3. Preparação de contexto
        4. Execução segura com tratamento de erros
        5. Atualização de estados
        6. Notificação de eventos
        
        Estados possíveis:
        - initialized: Equipe inicializada
        - running: Em execução
        - completed: Execução concluída
        - error: Erro durante execução
        
        Raises:
            Exception: Propaga exceções após registro adequado
        """
        crew_id = str(crew.id)
        
        # Verifica condições de execução
        conditions = self.state.execution_conditions.get(crew_id, [])
        if conditions and not await self._verificar_condicoes(crew_id, conditions):
            self.logger.info(f"Condições não atendidas para execução da equipe {crew_id}")
            return None
            
        # Continua com a execução normal
        try:
            self.state.crew_states[crew_id]['status'] = 'running'
            
            # Prepara contexto de execução
            contexto = {
                'shared_state': self.state.shared_state,
                'crew_state': self.state.crew_states[crew_id],
                **self.state.execution_context
            }
            
            resultado = await crew.kickoff(inputs=contexto)
            
            # Atualiza estados
            self.state.crew_states[crew_id].update({
                'status': 'completed',
                'last_execution': datetime.now(),
                'results': resultado
            })
            
            # Gera evento de conclusão
            await self.event_queue.put(FlowEvent(
                type=EventType.TASK_COMPLETE,
                source=crew_id,
                data={'resultado': resultado}
            ))
            
            return resultado
            
        except Exception as e:
            self.state.crew_states[crew_id]['status'] = 'error'
            await self.event_queue.put(FlowEvent(
                type=EventType.ERROR,
                source=crew_id,
                data={'error': str(e)}
            ))
            raise

    async def _executar_analise_cached(
        self,
        crew_id: str,
        analysis_type: str,
        params: Dict,
        analysis_func: Callable,
        ttl: Optional[timedelta] = None
    ) -> Dict:
        """Executa análise com suporte a cache."""
        cached_result = self.state.analysis_cache.get(crew_id, analysis_type, params)
        
        if cached_result is not None:
            self.logger.info(f"Usando resultado em cache para {analysis_type}")
            return cached_result
        
        result = await analysis_func(params)
        self.state.analysis_cache.set(
            crew_id,
            analysis_type,
            params,
            result,
            ttl
        )
        
        return result

    async def criar_checkpoint(self, checkpoint_id: str):
        """
        Cria um checkpoint do estado atual do sistema.
        
        Este método:
        1. Copia o estado atual do sistema
        2. Armazena métricas e decisões
        3. Registra o timestamp do checkpoint
        
        Args:
            checkpoint_id (str): Identificador único para o checkpoint
            
        O checkpoint inclui:
        - Estado compartilhado
        - Estados individuais das equipes
        - Histórico de métricas
        - Histórico de decisões
        - Timestamp de criação
        
        Este checkpoint pode ser usado posteriormente para rollback
        parcial ou completo do sistema.
        """
        checkpoint = {
            'shared_state': self.state.shared_state.copy(),
            'crew_states': {
                crew_id: state.copy() 
                for crew_id, state in self.state.crew_states.items()
            },
            'metrics_history': self.state.metrics_history.copy(),
            'decisions_history': self.state.decisions_history.copy(),
            'timestamp': datetime.now()
        }
        self.state.checkpoints[checkpoint_id] = checkpoint
        
    async def executar_rollback(
        self,
        rollback_type: RollbackType,
        crew_id: Optional[str] = None,
        checkpoint_id: Optional[str] = None,
        state_key: Optional[str] = None,
        reason: str = "Rollback manual"
    ):
        """
        Executa operação de rollback no sistema.
        
        Args:
            rollback_type (RollbackType): Tipo de rollback a ser executado
            crew_id (str, opcional): ID da equipe para rollback específico
            checkpoint_id (str, opcional): ID do checkpoint para restauração
            state_key (str, opcional): Chave de estado específica
            reason (str): Motivo do rollback
            
        Tipos de Rollback:
        - FULL: Restaura todo o sistema ao estado mais antigo
        - CREW: Restaura apenas uma equipe específica
        - CHECKPOINT: Restaura até um checkpoint específico
        - STATE: Restaura apenas uma chave de estado específica
        
        O método:
        1. Cria evento de rollback
        2. Executa o tipo específico de rollback
        3. Notifica o sistema sobre a operação
        4. Registra no log em caso de erro
        
        Raises:
            ValueError: Se parâmetros necessários estiverem faltando
            Exception: Se ocorrer erro durante o rollback
        """
        rollback_event = RollbackEvent(
            type=rollback_type,
            crew_id=crew_id,
            checkpoint_id=checkpoint_id,
            state_key=state_key,
            reason=reason
        )
        
        try:
            if rollback_type == RollbackType.FULL:
                await self._rollback_completo()
            elif rollback_type == RollbackType.CREW:
                await self._rollback_crew(crew_id)
            elif rollback_type == RollbackType.CHECKPOINT:
                await self._rollback_checkpoint(checkpoint_id)
            elif rollback_type == RollbackType.STATE:
                await self._rollback_state(state_key)
                
            # Notifica sobre o rollback
            await self.event_queue.put(FlowEvent(
                type=EventType.ROLLBACK,
                source="system",
                priority=EventPriority.HIGH,
                data={'rollback': rollback_event.dict()}
            ))
            
        except Exception as e:
            self.logger.error(f"Erro durante rollback: {e}")
            raise
            
    async def _rollback_completo(self):
        """
        Executa rollback completo do flow.
        
        Este método:
        1. Restaura estado compartilhado ao inicial
        2. Limpa históricos
        3. Reinicializa estados das equipes
        4. Notifica sistema sobre rollback
        """
        try:
            # Salva estado atual como checkpoint antes do rollback
            checkpoint_id = f"pre_rollback_{datetime.now().isoformat()}"
            await self.criar_checkpoint(checkpoint_id)
            
            # Restaura estado inicial
            self.state.shared_state = {}
            self.state.metrics_history = []
            self.state.decisions_history = []
            self.state.event_history = []
            self.state.feedback_history = []
            
            # Reinicializa estados das equipes
            for crew_id in self.state.crew_states:
                self.state.crew_states[crew_id] = CrewState(
                    status='initialized'
                )
                
            # Notifica sobre rollback
            await self.event_queue.put(FlowEvent(
                type=EventType.STATE_CHANGE,
                source='system',
                priority=EventPriority.HIGH,
                data={
                    'type': 'rollback',
                    'rollback_type': RollbackType.FULL,
                    'checkpoint_id': checkpoint_id
                }
            ))
            
        except Exception as e:
            self.logger.error(f"Erro durante rollback completo: {str(e)}")
            raise
            
    async def _rollback_crew(self, crew_id: str):
        """
        Executa rollback de uma equipe específica.
        
        Args:
            crew_id (str): ID da equipe para rollback
            
        Este método:
        1. Restaura estado da equipe
        2. Remove eventos pendentes
        3. Limpa cache de análise
        4. Notifica sistema
        """
        try:
            if crew_id not in self.state.crew_states:
                raise ValueError(f"Equipe {crew_id} não encontrada")
                
            # Salva checkpoint antes do rollback
            checkpoint_id = f"pre_crew_rollback_{crew_id}_{datetime.now().isoformat()}"
            await self.criar_checkpoint(checkpoint_id)
            
            # Restaura estado da equipe
            self.state.crew_states[crew_id] = CrewState(
                status='initialized'
            )
            
            # Remove eventos pendentes da equipe
            self.state.timed_events = [
                event for event in self.state.timed_events
                if event.event.source != crew_id
            ]
            
            # Limpa cache de análise da equipe
            self.state.analysis_cache.invalidate(crew_id)
            
            # Notifica sobre rollback
            await self.event_queue.put(FlowEvent(
                type=EventType.STATE_CHANGE,
                source='system',
                target=crew_id,
                priority=EventPriority.HIGH,
                data={
                    'type': 'rollback',
                    'rollback_type': RollbackType.CREW,
                    'checkpoint_id': checkpoint_id
                }
            ))
            
        except Exception as e:
            self.logger.error(f"Erro durante rollback da equipe {crew_id}: {str(e)}")
            raise
            
    async def _rollback_checkpoint(self, checkpoint_id: str):
        """
        Executa rollback até um checkpoint específico.
        
        Args:
            checkpoint_id (str): ID do checkpoint para restauração
            
        Este método:
        1. Verifica existência do checkpoint
        2. Restaura estado do checkpoint
        3. Atualiza estados das equipes
        4. Notifica sistema
        """
        try:
            if checkpoint_id not in self.state.checkpoints:
                raise ValueError(f"Checkpoint {checkpoint_id} não encontrado")
                
            checkpoint = self.state.checkpoints[checkpoint_id]
            
            # Restaura estado do checkpoint
            self.state.shared_state = checkpoint['shared_state']
            self.state.metrics_history = checkpoint['metrics_history']
            self.state.decisions_history = checkpoint['decisions_history']
            
            # Restaura estados das equipes
            for crew_id, crew_state in checkpoint['crew_states'].items():
                if crew_id in self.state.crew_states:
                    self.state.crew_states[crew_id] = crew_state
                    
            # Notifica sobre rollback
            await self.event_queue.put(FlowEvent(
                type=EventType.STATE_CHANGE,
                source='system',
                priority=EventPriority.HIGH,
                data={
                    'type': 'rollback',
                    'rollback_type': RollbackType.CHECKPOINT,
                    'checkpoint_id': checkpoint_id
                }
            ))
            
        except Exception as e:
            self.logger.error(f"Erro durante rollback ao checkpoint {checkpoint_id}: {str(e)}")
            raise
            
    async def _rollback_state(self, state_key: str):
        """
        Executa rollback de um estado específico.
        
        Args:
            state_key (str): Chave do estado para rollback
            
        Este método:
        1. Verifica existência da chave
        2. Restaura valor anterior
        3. Notifica sistema
        """
        try:
            if state_key not in self.state.shared_state:
                raise ValueError(f"Chave de estado {state_key} não encontrada")
                
            # Salva checkpoint antes do rollback
            checkpoint_id = f"pre_state_rollback_{state_key}_{datetime.now().isoformat()}"
            await self.criar_checkpoint(checkpoint_id)
            
            # Remove a chave do estado
            del self.state.shared_state[state_key]
            
            # Notifica sobre rollback
            await self.event_queue.put(FlowEvent(
                type=EventType.STATE_CHANGE,
                source='system',
                priority=EventPriority.HIGH,
                data={
                    'type': 'rollback',
                    'rollback_type': RollbackType.STATE,
                    'state_key': state_key,
                    'checkpoint_id': checkpoint_id
                }
            ))
            
        except Exception as e:
            self.logger.error(f"Erro durante rollback do estado {state_key}: {str(e)}")
            raise
            
    async def _verificar_condicoes(
        self,
        crew_id: str,
        conditions: List[ExecutionCondition]
    ) -> bool:
        """
        Verifica todas as condições para execução.
        
        Args:
            crew_id (str): ID da equipe sendo avaliada
            conditions (List[ExecutionCondition]): Lista de condições
            
        Returns:
            bool: True se todas as condições forem atendidas
        """
        try:
            for condition in conditions:
                if not await self._avaliar_condicao_execucao(crew_id, condition):
                    return False
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao verificar condições para {crew_id}: {str(e)}")
            return False

    async def _avaliar_condicao_execucao(
        self,
        crew_id: str,
        condition: ExecutionCondition
    ) -> bool:
        """
        Avalia uma condição específica de execução.
        
        Args:
            crew_id (str): ID da equipe sendo avaliada
            condition (ExecutionCondition): Condição a ser verificada
            
        Returns:
            bool: True se a condição for atendida
        """
        try:
            result = False
            
            if condition.type == ConditionType.METRIC_THRESHOLD:
                result = await self._avaliar_metrica(crew_id, condition)
                
            elif condition.type == ConditionType.STATE_CHECK:
                result = await self._avaliar_estado(crew_id, condition)
                
            elif condition.type == ConditionType.DEPENDENCY:
                result = await self._avaliar_dependencia(crew_id, condition)
                
            elif condition.type == ConditionType.TIME_WINDOW:
                result = await self._avaliar_janela_tempo(condition)
                
            elif condition.type == ConditionType.RESOURCE:
                result = await self._avaliar_recursos(condition)
                
            await self.event_queue.put(FlowEvent(
                type=EventType.CONDITION_MET if result else EventType.STATE_CHANGE,
                source=crew_id,
                data={
                    'condition_type': condition.type,
                    'result': result,
                    'parameters': condition.parameters
                }
            ))
            
            return result
            
        except Exception as e:
            self.logger.error(f"Erro ao avaliar condição para {crew_id}: {str(e)}")
            return False

    async def _avaliar_metrica(self, crew_id: str, condition: ExecutionCondition) -> bool:
        """
        Avalia uma condição baseada em métricas.
        
        Args:
            crew_id (str): ID da equipe sendo avaliada
            condition (ExecutionCondition): Condição a ser verificada
            
        Returns:
            bool: True se a condição for atendida
        """
        try:
            metric_type = condition.parameters.get('metric_type')
            threshold = condition.parameters.get('threshold')
            operator = condition.parameters.get('operator', '>=')
            window = condition.parameters.get('window', 1)
            
            if not metric_type or threshold is None:
                return False
                
            crew_metrics = [
                m for m in self.state.metrics_history
                if m.type == metric_type
            ][-window:]
            
            if not crew_metrics:
                return False
                
            current_value = sum(m.value for m in crew_metrics) / len(crew_metrics)
            
            if operator == '>=':
                return current_value >= threshold
            elif operator == '>':
                return current_value > threshold
            elif operator == '<=':
                return current_value <= threshold
            elif operator == '<':
                return current_value < threshold
            elif operator == '==':
                return current_value == threshold
            else:
                return False
                
        except Exception as e:
            self.logger.error(f"Erro ao avaliar métrica para {crew_id}: {str(e)}")
            return False

    async def _avaliar_estado(self, crew_id: str, condition: ExecutionCondition) -> bool:
        """
        Avalia uma condição baseada no estado do sistema.
        
        Args:
            crew_id (str): ID da equipe sendo avaliada
            condition (ExecutionCondition): Condição a ser verificada
            
        Returns:
            bool: True se a condição for atendida
        """
        try:
            state_key = condition.parameters.get('state_key')
            expected_value = condition.parameters.get('expected_value')
            scope = condition.parameters.get('scope', 'shared')
            
            if not state_key or expected_value is None:
                return False
                
            if scope == 'shared':
                current_value = self.state.shared_state.get(state_key)
            else:
                crew_state = self.state.crew_states.get(crew_id, {})
                current_value = crew_state.get(state_key)
                
            return current_value == expected_value
            
        except Exception as e:
            self.logger.error(f"Erro ao avaliar estado para {crew_id}: {str(e)}")
            return False

    async def _avaliar_dependencia(self, crew_id: str, condition: ExecutionCondition) -> bool:
        """
        Avalia dependências entre equipes.
        
        Args:
            crew_id (str): ID da equipe sendo avaliada
            condition (ExecutionCondition): Condição a ser verificada
            
        Returns:
            bool: True se todas as dependências forem satisfeitas
        """
        try:
            required_crews = condition.parameters.get('required_crews', [])
            required_status = condition.parameters.get('required_status', 'completed')
            require_results = condition.parameters.get('require_results', False)
            
            if not required_crews:
                return True
                
            for dep_crew in required_crews:
                crew_state = self.state.crew_states.get(dep_crew)
                
                if not crew_state:
                    return False
                    
                if crew_state.status != required_status:
                    return False
                    
                if require_results and not crew_state.results:
                    return False
                    
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao avaliar dependências para {crew_id}: {str(e)}")
            return False

    async def _avaliar_janela_tempo(self, condition: ExecutionCondition) -> bool:
        """
        Avalia uma condição baseada em janelas de tempo.
        
        Args:
            condition (ExecutionCondition): Condição a ser verificada
            
        Returns:
            bool: True se a condição for atendida
        """
        try:
            start_time = condition.parameters.get('start_time')
            end_time = condition.parameters.get('end_time')
            duration = condition.parameters.get('duration')
            
            now = datetime.now()
            
            if start_time and end_time:
                return start_time <= now <= end_time
                
            elif duration:
                last_event = next(
                    (e for e in reversed(self.state.event_history)
                     if e.type == condition.parameters.get('event_type')),
                    None
                )
                
                if not last_event:
                    return True
                    
                time_since_last = now - last_event.timestamp
                return time_since_last >= duration
                
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao avaliar janela de tempo: {str(e)}")
            return False

    async def _avaliar_recursos(self, condition: ExecutionCondition) -> bool:
        """
        Avalia uma condição baseada em recursos disponíveis.
        
        Args:
            condition (ExecutionCondition): Condição a ser verificada
            
        Returns:
            bool: True se a condição for atendida
        """
        try:
            resource_type = condition.parameters.get('resource_type')
            required_amount = condition.parameters.get('required_amount')
            
            if not resource_type or required_amount is None:
                return False
                
            available_resources = self.state.shared_state.get('resources', {})
            available_amount = available_resources.get(resource_type, 0)
            
            return available_amount >= required_amount
            
        except Exception as e:
            self.logger.error(f"Erro ao avaliar recursos: {str(e)}")
            return False

    async def _propagar_evento(
        self,
        event: FlowEvent,
        propagation: EventPropagation
    ):
        """
        Propaga um evento para outras equipes baseado em regras.
        
        Args:
            event (FlowEvent): Evento a ser propagado
            propagation (EventPropagation): Estado atual da propagação
            
        O sistema de propagação:
        1. Verifica limites de profundidade
        2. Evita loops infinitos
        3. Aplica regras de propagação
        4. Transforma eventos quando necessário
        5. Propaga recursivamente
        
        Controles:
        - Profundidade máxima de propagação
        - Conjunto de equipes já visitadas
        - Prioridade dos eventos
        - Transformações de eventos
        
        A propagação para quando:
        - Atinge profundidade máxima
        - Visita equipe já processada
        - Não há mais regras aplicáveis
        """
        if (propagation.current_depth >= propagation.max_depth or 
            event.source in propagation.visited_crews):
            return
            
        propagation.visited_crews.add(event.source)
        rules = self.state.propagation_rules.get(event.type, [])
        
        for rule in rules:
            if await self._avaliar_condicao(rule.condition, event):
                for target_crew in rule.target_crews:
                    if target_crew not in propagation.visited_crews:
                        novo_evento = event.copy()
                        if rule.transform_event:
                            novo_evento = await rule.transform_event(event)
                            
                        novo_evento.source = event.source
                        novo_evento.target = target_crew
                        novo_evento.priority = rule.priority
                        
                        await self.event_queue.put(novo_evento)
                        
                        # Propaga recursivamente
                        nova_propagacao = propagation.copy()
                        nova_propagacao.current_depth += 1
                        await self._propagar_evento(novo_evento, nova_propagacao)
                        
    async def _avaliar_condicao(
        self,
        condition: str,
        event: FlowEvent
    ) -> bool:
        """
        Avalia uma condição de propagação de eventos.
        
        Args:
            condition (str): Expressão de condição a ser avaliada
            event (FlowEvent): Evento sendo processado
            
        Returns:
            bool: Resultado da avaliação da condição
            
        O método:
        1. Prepara contexto de avaliação com:
           - Evento atual
           - Estado global
           - Histórico de métricas
           - Estados das equipes
        2. Avalia a expressão de forma segura
        3. Registra erros se ocorrerem
        
        A avaliação é feita em um ambiente controlado para
        evitar execução de código malicioso.
        
        Raises:
            Exception: Capturada e registrada, retornando False
        """
        try:
            # Contexto para avaliação
            context = {
                'event': event,
                'state': self.state,
                'metrics': self.state.metrics_history,
                'crew_states': self.state.crew_states
            }
            return eval(condition, {}, context)
        except Exception as e:
            self.logger.error(f"Erro ao avaliar condição: {e}")
            return False

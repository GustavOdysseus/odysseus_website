import logging
import os
from datetime import datetime

class ConcursoErrorHandler:
    def __init__(self, log_dir='logs'):
        # Criar diretório de logs se não existir
        os.makedirs(log_dir, exist_ok=True)
        
        # Configurar logging
        log_file = os.path.join(log_dir, f'concurso_analyzer_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s: %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def log_error(self, error, context=None):
        """
        Registra um erro com contexto adicional
        
        Args:
            error (Exception): Erro capturado
            context (dict, optional): Contexto adicional sobre o erro
        """
        error_message = str(error)
        self.logger.error(f"Erro encontrado: {error_message}")
        
        if context:
            self.logger.info(f"Contexto do erro: {context}")
    
    def is_rate_limit_error(self, error):
        """
        Verifica se o erro é relacionado a limite de requisições
        
        Args:
            error (Exception): Erro a ser verificado
            
        Returns:
            bool: True se for um erro de limite de requisições, False caso contrário
        """
        rate_limit_keywords = [
            'rate limit exceeded', 
            'too many requests', 
            'quota', 
            'limit reached'
        ]
        
        error_message = str(error).lower()
        return any(keyword in error_message for keyword in rate_limit_keywords)
    
    def get_fallback_model(self):
        """
        Retorna um modelo de fallback quando o modelo principal falha
        
        Returns:
            str: Nome do modelo de fallback
        """
        fallback_models = [
            'gpt-3.5-turbo',
            'claude-2',  # Outros modelos podem ser adicionados
            'gpt-3.5-turbo-16k'
        ]
        
        self.logger.info(f"Usando modelo de fallback: {fallback_models[0]}")
        return fallback_models[0]
    
    def generate_error_report(self, error, context=None):
        """
        Gera um relatório detalhado de erro
        
        Args:
            error (Exception): Erro capturado
            context (dict, optional): Contexto adicional
            
        Returns:
            dict: Relatório de erro estruturado
        """
        return {
            'timestamp': datetime.now().isoformat(),
            'error_type': type(error).__name__,
            'error_message': str(error),
            'context': context or {},
            'suggested_action': 'Retry with fallback model or wait and retry'
        }

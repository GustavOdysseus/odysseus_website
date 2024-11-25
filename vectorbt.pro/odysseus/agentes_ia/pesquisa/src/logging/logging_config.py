import logging
import logging.handlers
import os
from pathlib import Path
from datetime import datetime
import json
from typing import Dict, Optional

class LoggingConfig:
    """
    Configuração centralizada de logging para o sistema Odysseus.
    """
    
    def __init__(
        self,
        log_dir: str = "logs",
        log_level: str = "INFO",
        max_bytes: int = 10 * 1024 * 1024,  # 10MB
        backup_count: int = 5,
        console_format: str = "%(asctime)s - %(levelname)s - %(message)s",
        file_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    ):
        """
        Inicializa a configuração de logging.
        """
        self.log_dir = Path(log_dir)
        self.log_level = getattr(logging, log_level.upper())
        self.max_bytes = max_bytes
        self.backup_count = backup_count
        self.console_format = console_format
        self.file_format = file_format
        
        # Garante que o diretório de logs existe
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Configura logging básico
        logging.basicConfig(level=self.log_level)
        
    def get_logger(self, name: str) -> logging.Logger:
        """
        Obtém um logger configurado com os handlers definidos.
        """
        logger = logging.getLogger(name)
        logger.setLevel(self.log_level)
        
        # Remove handlers existentes para evitar duplicação
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
            
        # Adiciona handlers
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(self.console_format))
        logger.addHandler(console_handler)
        
        # Handler de arquivo
        file_path = self.log_dir / f"{name}.log"
        file_handler = logging.handlers.RotatingFileHandler(
            file_path,
            maxBytes=self.max_bytes,
            backupCount=self.backup_count,
            encoding='utf-8'
        )
        file_handler.setFormatter(logging.Formatter(self.file_format))
        logger.addHandler(file_handler)
        
        return logger

# Exemplo de uso
if __name__ == "__main__":
    # Inicializa configuração de logging
    logging_config = LoggingConfig(
        log_dir="logs",
        log_level="DEBUG",
        max_bytes=5 * 1024 * 1024,  # 5MB
        backup_count=3
    )
    
    # Obtém um logger
    logger = logging_config.get_logger("teste")
    
    # Testa diferentes níveis de log
    logger.debug("Mensagem de debug")
    logger.info("Mensagem de informação")
    logger.warning("Mensagem de aviso")
    logger.error("Mensagem de erro")
    logger.critical("Mensagem crítica")

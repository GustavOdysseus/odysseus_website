"""
Main entry point for the Telegram Calendar Bot.
"""

import logging
import os
from dotenv import load_dotenv
from telegram.telegram_handler import TelegramHandler

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s][%(levelname)s] %(message)s'
)

def main():
    try:
        logging.info("Iniciando o bot do Telegram...")
        handler = TelegramHandler()
        logging.info("Bot iniciado com sucesso! Aguardando mensagens...")
        handler.start()
    except Exception as e:
        logging.error(f"Erro ao iniciar o bot: {str(e)}")
        raise

if __name__ == "__main__":
    load_dotenv()
    main()

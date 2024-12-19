"""
Main entry point for the Telegram Calendar Bot using crewai_tools.
This is an alternative implementation using crewai_tools.ComposioTool.
"""

import logging
import os
from dotenv import load_dotenv
import telebot
from threading import Timer
from collections import defaultdict
from calendar.calendar_crew_tools import CalendarCrewTools

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s][%(levelname)s] %(message)s'
)

class TelegramHandler:
    def __init__(self):
        self.bot = telebot.TeleBot(os.getenv('TELEGRAM_BOT_KEY'))
        self.message_queue = defaultdict(list)  # chat_id -> [messages]
        self.processing_timers = {}  # chat_id -> timer
        self.crew = CalendarCrewTools()
        logging.info(f"TelegramHandler iniciado com token: {os.getenv('TELEGRAM_BOT_KEY')[:5]}...")

    def process_messages(self, chat_id: int):
        """Process all queued messages for a chat after delay"""
        try:
            if chat_id in self.message_queue and self.message_queue[chat_id]:
                messages = self.message_queue[chat_id]
                combined_message = " ".join([msg.text for msg in messages])
                logging.info(f"Processando mensagens para chat {chat_id}: {combined_message}")
                
                result = self.crew.process_message(combined_message)
                
                # Send response back to the last message in queue
                last_message = messages[-1]
                self.bot.reply_to(last_message, result)
                self.message_queue[chat_id].clear()
                
        except Exception as e:
            error_msg = f"Erro ao processar mensagens: {str(e)}"
            logging.error(error_msg)
            self.bot.send_message(chat_id, f"Desculpe, ocorreu um erro: {error_msg}")
            
        finally:
            if chat_id in self.processing_timers:
                del self.processing_timers[chat_id]

    def handle_message(self, message):
        """Queue message and schedule processing"""
        chat_id = message.chat.id
        self.message_queue[chat_id].append(message)
        
        # Cancel existing timer if any
        if chat_id in self.processing_timers:
            self.processing_timers[chat_id].cancel()
        
        # Schedule processing after delay
        timer = Timer(15.0, self.process_messages, args=[chat_id])
        timer.start()
        self.processing_timers[chat_id] = timer
        
    def start(self):
        """Start the bot"""
        @self.bot.message_handler(func=lambda message: True)
        def echo_all(message):
            self.handle_message(message)
            
        self.bot.infinity_polling()


def main():
    try:
        logging.info("Iniciando o bot do Telegram (versão tools)...")
        handler = TelegramHandler()
        logging.info("Bot iniciado com sucesso! Aguardando mensagens...")
        handler.start()
    except Exception as e:
        logging.error(f"Erro ao iniciar o bot: {str(e)}")
        raise

if __name__ == "__main__":
    load_dotenv()
    main()

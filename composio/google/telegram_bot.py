from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from calendar_agent import CalendarAgent
from dotenv import load_dotenv
import os

load_dotenv()

# Inicializa o agente do calendário
calendar_agent = CalendarAgent()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Envia mensagem quando o comando /start é emitido."""
    await update.message.reply_text(
        "Olá! Eu sou seu assistente de calendário. 🗓\n\n"
        "Você pode me pedir coisas como:\n"
        "- Crie uma reunião amanhã às 14h\n"
        "- Quais eventos tenho hoje?\n"
        "- Mostre meus calendários\n\n"
        "Como posso ajudar?"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Envia mensagem quando o comando /help é emitido."""
    await update.message.reply_text(
        "Aqui está o que eu posso fazer:\n\n"
        "1. Criar eventos rapidamente\n"
        "   Exemplo: 'Crie uma reunião amanhã às 14h'\n\n"
        "2. Buscar eventos\n"
        "   Exemplo: 'Quais eventos tenho hoje?'\n\n"
        "3. Listar calendários\n"
        "   Exemplo: 'Mostre meus calendários'\n\n"
        "Basta me dizer o que você precisa em linguagem natural! 😊"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Processa mensagens normais do usuário."""
    try:
        # Mostra que está digitando
        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id,
            action="typing"
        )
        
        # Processa a mensagem usando o agente
        response = calendar_agent.process_request(update.message.text)
        
        # Envia a resposta
        await update.message.reply_text(response)
    except Exception as e:
        await update.message.reply_text(
            "Desculpe, ocorreu um erro ao processar sua solicitação. "
            "Por favor, tente novamente."
        )

def main():
    """Inicia o bot."""
    # Cria o aplicativo
    app = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()

    # Adiciona handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Inicia o bot
    print("Bot iniciado...")
    app.run_polling()

if __name__ == '__main__':
    main()

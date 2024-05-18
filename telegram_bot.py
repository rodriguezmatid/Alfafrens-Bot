"""
The main execution script for initializing and running the Telegram bot.

This script sets up the Telegram bot using the python-telegram-bot library.
It configures command handlers for specific bot commands and a message handler
for general text responses. The bot runs in polling mode, continuously checking
for new messages and commands.
"""
import functions_telegram
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import os

T_TOKEN = os.environ["TELEGRAM_TOKEN"]

if __name__ == '__main__':
    application = ApplicationBuilder().token(T_TOKEN).build()

    application.add_handler(CommandHandler('start', functions_telegram.start))
    application.add_handler(CommandHandler('eth_price', functions_telegram.search_degen_price))
    
    # Add a message handler for handling text messages that are not commands
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, functions_telegram.handle_text))

    # The 'polling mode' is a technique used for the bot to receive updates or messages from users. 
    # In this mode, the bot actively 'polls' or queries the Telegram server to fetch new messages
    application.run_polling()
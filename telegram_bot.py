"""
The main execution script for initializing and running the Telegram bot.

This script sets up the Telegram bot using the python-telegram-bot library.
It configures command handlers for specific bot commands and a message handler
for general text responses. The bot runs in polling mode, continuously checking
for new messages and commands.
"""
import functions_telegram
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import os, asyncio

T_TOKEN = os.environ["TELEGRAM_TOKEN"]

async def main():
    application = ApplicationBuilder().token(os.getenv('TELEGRAM_TOKEN')).build()

    application.add_handler(CommandHandler("start", functions_telegram.start))
    application.add_handler(CommandHandler("configuration", functions_telegram.configuration))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, functions_telegram.handle_text))

    await functions_telegram.set_bot_commands(application)

    application.run_polling()

if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()
    asyncio.run(main())
import functions_telegram
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import os
import asyncio

T_TOKEN = os.environ["TELEGRAM_TOKEN"]

async def main():
    application = ApplicationBuilder().token(T_TOKEN).build()

    application.add_handler(CommandHandler("start", functions_telegram.start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, functions_telegram.handle_text))

    await functions_telegram.set_bot_commands(application)

    application.run_polling()

if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()
    asyncio.run(main())

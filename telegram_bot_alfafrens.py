import functions_telegram, message_handlers
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import os, logging, asyncio

T_TOKEN = os.environ["TELEGRAM_TOKEN_TEST"]

async def main():
    application = ApplicationBuilder().token(T_TOKEN).build()
    bot = application.bot  # Obtener el objeto bot directamente de la instancia de la aplicación

    application.add_handler(CommandHandler("start", functions_telegram.start))
    application.add_handler(CommandHandler("info", message_handlers.send_info_message))  # Añadir manejador para /info
    application.add_handler(CommandHandler("price", functions_telegram.search_degen_price))  # Añadir manejador para /price
    application.add_handler(CommandHandler("gwei", functions_telegram.search_gas_price))  # Añadir manejador para /gwei
    application.add_handler(CommandHandler("configuration", functions_telegram.configuration))  # Añadir manejador para /configuration
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, functions_telegram.handle_text))

    await functions_telegram.set_bot_commands(application)

    # Iniciar el trabajo recurrente para verificar el precio del gas
    asyncio.create_task(functions_telegram.check_gas_price_periodically(bot))

    # Iniciar el trabajo recurrente para verificar desuscripciones
    asyncio.create_task(functions_telegram.check_unsubscribed_users_periodically(bot))

    application.run_polling()

if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()
    
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped.")
from telegram import Update
from telegram.ext import ContextTypes

# Function to send welcome message
async def send_welcome_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    print(f"Sending welcome message to {chat_id}")  # Mensaje de depuración
    welcome_message = (
        "Welcome to the AlfaFren Bot!\n\n"
        "Here are some of the features you can use:\n"
        "- /start: Start the bot and register your details.\n"
        "- /info: Get information about the bot and its features.\n"
        "- Price Alerts: Get notified when the price of Degen or gas changes.\n"
        "- User Information: View details about your channel and account.\n"
        "- Settings: Configure your alerts and preferences.\n"
        "- Unsubscribed Alerts: Get notified when someone unsubscribes from your channel.\n"
    )
    await update.message.reply_text(welcome_message)

# Function to return information about the bot
async def send_info_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    info_message = (
        "AlfaFren Bot Information:\n\n"
        "Features:\n"
        "- /start: Start the bot and register your details.\n"
        "- /info: Get information about the bot and its features.\n"
        "- Price Alerts: Get notified when the price of Degen or gas changes.\n"
        "- User Information: View details about your channel and account.\n"
        "- Settings: Configure your alerts and preferences.\n"
        "- Unsubscribed Alerts: Get notified when someone unsubscribes from your channel.\n"
    )
    await update.message.reply_text(info_message)

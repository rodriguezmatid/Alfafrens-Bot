from telegram import Update
from telegram.ext import ContextTypes

# Function to send welcome message
async def send_welcome_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    print(f"Sending welcome message to {chat_id}")  # Mensaje de depuración
    welcome_message = (
        "🌟 Welcome to the Bot! 🌟\n\n"
        "Here are some of the features you can use:\n\n"
        "🚀 /start: Start the bot and register your details.\n"
        "ℹ️ /info: Get information about the bot and its features.\n"
        "💸 Price Alerts: Get notified when the price of Degen or gas changes.\n"
        "👤 User Information: View details about your channel and account.\n"
        "⚙️ Settings: Configure your alerts and preferences.\n"
        "🔔 Unsubscribed Alerts: Get notified when someone unsubscribes from your channel.\n"
        "💰 Balance Alerts: Receive alerts if your DegenX balance falls below 250 tokens.\n"
        "📈 Claim Alerts: Be reminded every 22 hours to claim your rewards to ensure you don’t miss out.\n"
    )
    await update.message.reply_text(welcome_message)

# Function to return information about the bot
async def send_info_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    info_message = (
        "🌟 AlfaFren Bot Information 🌟\n\n"
        "Here are some of the features you can use:\n\n"
        "🚀 /start: Start the bot and register your details.\n"
        "ℹ️ /info: Get information about the bot and its features.\n"
        "💸 Price Alerts: Get notified when the price of Degen or gas changes.\n"
        "👤 User Information: View details about your channel and account.\n"
        "⚙️ Settings: Configure your alerts and preferences.\n"
        "🔔 Unsubscribed Alerts: Get notified when someone unsubscribes from your channel.\n"
        "💰 Balance Alerts: Receive alerts if your DegenX balance falls below 250 tokens, prompting you to recharge to avoid liquidation.\n"
        "📈 Claim Alerts: Be reminded every 22 hours to claim your rewards, helping you maximize your earnings and maintain your staking benefits.\n"
    )
    await update.message.reply_text(info_message)

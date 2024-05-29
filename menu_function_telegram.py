from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import ContextTypes
from global_vars import user_data, registered_status, price_alert_jobs


# Assuming user_data and registered_status are defined elsewhere
# Import them if they are not in this file

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id not in registered_status or not registered_status[chat_id]:
        await update.message.reply_text("Welcome! Please enter your channel ID:", reply_markup=ReplyKeyboardRemove())
        user_data[chat_id] = {'state': 'AWAITING_CHANNEL_ID'}
        registered_status[chat_id] = False
    else:
        await show_main_menu(update, context)

# Show main menu
async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_data[chat_id]['state'] = 'MAIN_MENU'
    reply_keyboard = [['User information', 'General information'],
                      ['Degen price', 'Gas price', 'Configuration']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    await update.message.reply_text(
        "What do you want to do?",
        reply_markup=markup
    )

# Show user info menu
async def show_user_info_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, show_channel=True):
    chat_id = update.effective_chat.id
    user_data[chat_id]['state'] = 'USER_INFO_MENU'
    reply_keyboard = [['Account'],
                      ['Back']]
    if show_channel:
        reply_keyboard.insert(0, ['Channel'])
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    await update.message.reply_text(
        "Select an option:",
        reply_markup=markup
    )

# Show general info menu
async def show_general_info_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_data[chat_id]['state'] = 'GENERAL_INFO_MENU'
    reply_keyboard = [['Channels', 'Unsubscribed'],
                      ['Back']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    await update.message.reply_text(
        "Select an option:",
        reply_markup=markup
    )

# Show channel subscription menu
async def show_channel_subscription_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_data[chat_id]['state'] = 'CHANNEL_SUBSCRIPTION_MENU'
    reply_keyboard = [['500', '1000', '1500'],
                      ['Back']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    await update.message.reply_text(
        "Select a subscription cost:",
        reply_markup=markup
    )

# Configuration menu
async def show_settings_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_data[chat_id]['state'] = 'SETTINGS_MENU'
    reply_keyboard = [['Price Alerts', 'Gas Alerts', 'Back']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    await update.message.reply_text(
        "Settings options:",
        reply_markup=markup
    )

# Price alerts menu
async def show_price_alerts_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_data[chat_id]['state'] = 'PRICE_ALERTS_MENU'
    reply_keyboard = [['ON', 'OFF', 'Back']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    await update.message.reply_text(
        "Price alerts:",
        reply_markup=markup
    )

# Frequency menu
async def show_frequency_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_data[chat_id]['state'] = 'FREQUENCY_MENU'
    reply_keyboard = [['2 hours', '6 hours', '24 hours', 'Back']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    await update.message.reply_text(
        "Select alert frequency:",
        reply_markup=markup
    )

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import ContextTypes
from global_vars import user_data, registered_status, price_alert_jobs
from message_handlers import send_welcome_message  # Importar desde el nuevo archivo

# Assuming user_data and registered_status are defined elsewhere
# Import them if they are not in this file
# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     chat_id = update.effective_chat.id
#     print(f"User {chat_id} started the bot")  # Mensaje de depuración
#     if chat_id not in registered_status or not registered_status[chat_id]:
#         await send_welcome_message(update, context)
#         reply_keyboard = [['FID', 'Address']]
#         markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
#         await update.message.reply_text("Please enter your FID or Address:", reply_markup=markup)
#         user_data[chat_id] = {'state': 'AWAITING_FID_OR_ADDRESS'}
#         # await update.message.reply_text("Please enter your FID:", reply_markup=ReplyKeyboardRemove())
#         # user_data[chat_id] = {'state': 'AWAITING_FID'}
#         registered_status[chat_id] = False
#     else:
#         await show_main_menu(update, context)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    print(f"User {chat_id} started the bot")
    if chat_id not in registered_status or not registered_status[chat_id]:
        await send_welcome_message(update, context)
        user_data[chat_id] = {'state': 'AWAITING_USERNAME'}
        await update.message.reply_text("Please enter your Farcaster username:", reply_markup=ReplyKeyboardRemove())
        registered_status[chat_id] = False
    else:
        await show_main_menu(update, context)

async def handle_fid_or_address(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
    chat_id = update.effective_chat.id
    user_data[chat_id]['state'] = 'AWAITING_FID_OR_ADDRESS_RESPONSE'
    if text.lower() == 'fid':
        await update.message.reply_text("Please enter your FID:")
    elif text.lower() == 'address':
        await update.message.reply_text("Please enter your address:")
    else:
        await update.message.reply_text("Invalid option. Please choose 'FID' or 'Address'.")
        return

# Show main menu
async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_data[chat_id]['state'] = 'MAIN_MENU'
    reply_keyboard = [['User information', 'General information'],
                      ['Degen price', 'Gas price', 'Alerts']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    await update.message.reply_text(
        "What do you want to do?",
        reply_markup=markup
    )

# Show user info menu
async def show_user_info_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_data[chat_id]['state'] = 'USER_INFO_MENU'
    reply_keyboard = [['Channel', 'Account'], ['Back']]
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
    reply_keyboard = [['Price', 'Unsubscribed', 'Claim', 'Balance', 'Back']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    await update.message.reply_text(
        "Alerts options:",
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

# Gas alerts menu
async def show_gas_alerts_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_data[chat_id]['state'] = 'GAS_ALERTS_MENU'
    reply_keyboard = [['ON', 'OFF', 'Back']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    await update.message.reply_text(
        "Gas alerts:",
        reply_markup=markup
    )

async def show_unsubscribed_alerts_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_data[chat_id]['state'] = 'UNSUBSCRIBED_ALERTS_MENU'
    reply_keyboard = [['ON', 'OFF', 'Back']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    await update.message.reply_text(
        "Unsubscribed alerts options:",
        reply_markup=markup
    )

async def show_claim_alerts_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_data[chat_id]['state'] = 'CLAIM_ALERTS_MENU'
    reply_keyboard = [['ON', 'OFF', 'Back']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    await update.message.reply_text(
        "Claim Alerts Options:",
        reply_markup=markup
    )

async def show_balance_alerts_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_data[chat_id]['state'] = 'BALANCE_ALERTS_MENU'
    reply_keyboard = [['ON', 'OFF', 'Back']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    await update.message.reply_text(
        "Balance alerts:",
        reply_markup=markup
    )
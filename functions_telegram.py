from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import os, dotenv, functions, requests, asyncio
from web3 import Web3

dotenv.load_dotenv()
rpc_url = os.environ['BASE']
w3 = Web3(Web3.HTTPProvider(rpc_url))

user_data = {}  # To store user data temporarily; use persistent storage for real applications
registered_status = {}  # To store registration status of users

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
                      ['Degen price', 'Gas price']]
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

# Handle text messages
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = update.message.text

    print(f"Received text: {text}")  # Debugging message

    if chat_id in user_data and 'state' in user_data[chat_id] and not registered_status.get(chat_id, False):
        print("1er menu")
        print(f"User state: {user_data[chat_id]['state']}")
        if user_data[chat_id]['state'] in ['AWAITING_CHANNEL_ID', 'AWAITING_ACCOUNT_ID']:
            if user_data[chat_id]['state'] == 'AWAITING_CHANNEL_ID':
                await handle_channel_id(update, context, text)
            elif user_data[chat_id]['state'] == 'AWAITING_ACCOUNT_ID':
                await handle_account_id(update, context, text)
        else:
            await show_main_menu(update, context)
    elif registered_status.get(chat_id, False):
        print("2do menu")
        if chat_id in user_data:
            print(f"User state: {user_data[chat_id]['state']}")
        if user_data[chat_id]['state'] == 'USER_INFO_MENU':
            await handle_user_info_menu(update, context, text)
        elif user_data[chat_id]['state'] == 'GENERAL_INFO_MENU':
            await handle_general_info_menu(update, context, text)
        elif user_data[chat_id]['state'] == 'CHANNEL_SUBSCRIPTION_MENU':
            await handle_channel_subscription_menu(update, context, text)
        else:
            if text == 'User information':
                await show_user_info_menu(update, context)
            elif text == 'General information':
                await show_general_info_menu(update, context)
            elif text == 'Degen price':
                await search_degen_price(update, context)
            elif text == 'Gas price':
                await search_gas_price(update, context)
            else:
                await show_main_menu(update, context)
    else:
        await start(update, context)

# Handle channel ID input
async def handle_channel_id(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
    chat_id = update.effective_chat.id
    if chat_id not in user_data:
        user_data[chat_id] = {}
    user_data[chat_id]['channel_id'] = text.lower()  # Convert to lowercase
    user_data[chat_id]['state'] = 'AWAITING_ACCOUNT_ID'
    print(f"User {chat_id} - channel_id set to: {text.lower()}")
    print(f"User state updated to: {user_data[chat_id]['state']}")
    await update.message.reply_text("Please enter your account ID:")

# Handle account ID input
async def handle_account_id(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
    chat_id = update.effective_chat.id
    if chat_id not in user_data:
        user_data[chat_id] = {}
    user_data[chat_id]['account_id'] = text.lower()  # Convert to lowercase
    registered_status[chat_id] = True
    print(f"User {chat_id} - account_id set to: {text.lower()}")
    print(f"User registration status updated to: {registered_status[chat_id]}")
    await update.message.reply_text("Thank you! You can now use the bot.")
    await show_main_menu(update, context)

# Handle user info menu options
async def handle_user_info_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
    chat_id = update.effective_chat.id
    if text == 'Channel':
        await handle_channel_option(update, context)
    elif text == 'Account':
        await handle_account_option(update, context)
    elif text == 'Back':
        await show_main_menu(update, context)
    else:
        await show_user_info_menu(update, context)

# Handle general info menu options
async def handle_general_info_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
    chat_id = update.effective_chat.id
    if text == 'Channels':
        await show_channel_subscription_menu(update, context)
    elif text == 'Unsubscribed':
        if 'channel_id' in user_data[chat_id]:
            channel_id = user_data[chat_id]['channel_id']
            await handle_unsubscribed_channels_with_matching_flow_operator(update, context, channel_id)
        else:
            await update.message.reply_text("Channel ID not set.")
            await show_general_info_menu(update, context)
    elif text == 'Back':
        await show_main_menu(update, context)
    else:
        await show_general_info_menu(update, context)

# Handle channel subscription menu options
async def handle_channel_subscription_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
    chat_id = update.effective_chat.id
    if text in ['500', '1000', '1500']:
        subscription_cost = int(text)
        if 'account_id' in user_data[chat_id]:
            account_id = user_data[chat_id]['account_id']
            await handle_unsubscribed_channels(update, context, account_id, subscription_cost)
        else:
            await update.message.reply_text("Account ID not set.")
            await show_user_info_menu(update, context)
    elif text == 'Back':
        await show_general_info_menu(update, context)
    else:
        await show_channel_subscription_menu(update, context)

# Handle unsubscribed channels
async def handle_unsubscribed_channels(update: Update, context: ContextTypes.DEFAULT_TYPE, account_id, subscription_cost):
    chat_id = update.effective_chat.id
    try:
        unsubscribed_channels = functions.get_unsubscribed_channels(account_id, subscription_cost)
        if isinstance(unsubscribed_channels, list):
            limited_channels = unsubscribed_channels[:5]
            message = f"Unsubscribed channels with subscription cost {subscription_cost}:\n"
            message += "\n".join([f"https://www.alfafrens.com/channel/{channel}" for channel in limited_channels])
            await update.message.reply_text(message)
        else:
            await update.message.reply_text(f"No unsubscribed channels found with subscription cost {subscription_cost}.")
    except Exception as e:
        await update.message.reply_text(f"Error fetching unsubscribed channels: {e}")
    await show_channel_subscription_menu(update, context)

# Handle unsubscribed channels with matching flow operator
async def handle_unsubscribed_channels_with_matching_flow_operator(update: Update, context: ContextTypes.DEFAULT_TYPE, channel_id):
    chat_id = update.effective_chat.id
    try:
        unsubscribed_channels = functions.get_unsubscribed_channels_with_matching_flow_operator(channel_id)
        if isinstance(unsubscribed_channels, list):
            limited_channels = unsubscribed_channels[:5]
            message = f"Unsubscribed channels:\n"
            message += "\n".join([f"https://www.alfafrens.com/profile/{channel}" for channel in limited_channels])
            await update.message.reply_text(message)
        else:
            await update.message.reply_text(f"No unsubscribed channels found with matching flow operator.")
    except Exception as e:
        await update.message.reply_text(f"Error fetching unsubscribed channels with matching flow operator: {e}")
    await show_general_info_menu(update, context)

# Handle channel option
async def handle_channel_option(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if 'channel_id' in user_data[chat_id]:
        channel_id = user_data[chat_id]['channel_id']
        result = functions.get_account_by_id(channel_id)
        number_of_subscribers = result[0]
        net_flow_rate = result[1]
        title = "Channel information"

        message = f"{title}\n"
        message += f"Number of subscribers: {number_of_subscribers}\n"
        message += f"Net flow rate: {net_flow_rate}\n"
        
        await update.message.reply_text(message)
        await show_user_info_menu(update, context, show_channel=False)
    else:
        await update.message.reply_text("Channel ID not set.")
        await show_user_info_menu(update, context)

# Handle account option
async def handle_account_option(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if 'account_id' in user_data[chat_id]:
        account_id = user_data[chat_id]['account_id']
        await account_information(update, context, account_id)
    else:
        await update.message.reply_text("Account ID not set.")
        await show_user_info_menu(update, context)

# Account information function
async def account_information(update: Update, context: ContextTypes.DEFAULT_TYPE, wallet):
    chat_id = update.effective_chat.id
    try:
        result = functions.get_channels_subscribed(wallet)
        number_of_channels_subscribed = len(result)

        message = f"Number of channels subscribed: {number_of_channels_subscribed}\n"
        
        await context.bot.send_message(chat_id=chat_id, text=message)
    except ValueError as ve:
        await context.bot.send_message(chat_id=chat_id, text=str(ve))
    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text="Error fetching account information, please try again.")

# Search degen price
async def search_degen_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        degen_price = await functions.obtain_degen_price() # Attempt to fetch the current price of Ethereum
        mensaje = f"Current Degen price: ${degen_price} USD"
        await update.message.reply_text(mensaje)
    except Exception as e:
        await update.message.reply_text(f"Error obtaining degen price: {e}")
    await show_main_menu(update, context)

# Search gas price
async def search_gas_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        gas_price = functions.obtain_gas_price(w3) / 10e8 # Attempt to fetch the current gas price
        message = f"Gas base fee: {gas_price} GWEI"
        await update.message.reply_text(message)
    except Exception as e:
        await update.message.reply_text(f"Error obtaining gas price: {e}")
    await show_main_menu(update, context)

# Configuration command handler
async def configuration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_data[chat_id] = {'state': 'AWAITING_CHANNEL_ID'}
    registered_status[chat_id] = False
    await update.message.reply_text("Please enter your channel ID to update:", reply_markup=ReplyKeyboardRemove())

# Set bot commands for the command list
async def set_bot_commands(application):
    commands = [
        BotCommand(command="/start", description="Start the bot"),
        BotCommand(command="/price", description="Returns the current Degen price"),
        BotCommand(command="/gwei", description="Returns the current base fee"),
        BotCommand(command="/configuration", description="Update your channel and account IDs")
    ]
    await application.bot.set_my_commands(commands)
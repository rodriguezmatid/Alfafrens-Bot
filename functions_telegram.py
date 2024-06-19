from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import os, dotenv, functions, requests, asyncio, json, time
from web3 import Web3
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from global_vars import user_data, registered_status, price_alert_jobs
from functions import obtain_gas_price, get_unsubscribed_channels_with_timestamp
from api_calls import user_information, channel_information

from menu_function_telegram import (
    start,
    show_main_menu,
    show_user_info_menu,
    show_general_info_menu,
    show_channel_subscription_menu,
    show_settings_menu,  # Actualizado
    show_price_alerts_menu,
    show_frequency_menu,
    show_gas_alerts_menu,
    show_unsubscribed_alerts_menu,
    show_claim_alerts_menu
)

dotenv.load_dotenv()
rpc_url = os.environ['BASE']
w3 = Web3(Web3.HTTPProvider(rpc_url))
scheduler = AsyncIOScheduler()
scheduler.start()

with open('./utils/cfa_contract.json', 'r') as f:
    abi_cfa_contract = json.load(f)
with open('./utils/gda_contract.json', 'r') as f:
    abi_gda_contract = json.load(f)
with open('./utils/super_degen.json', 'r') as f:
    abi_super_degen = json.load(f)

cfa_address = w3.to_checksum_address('0xcfA132E353cB4E398080B9700609bb008eceB125')
gda_address = w3.to_checksum_address('0x6DA13Bde224A05a288748d857b9e7DDEffd1dE08')
super_degen_address = w3.to_checksum_address('0x1eff3dd78f4a14abfa9fa66579bd3ce9e1b30529')

cfa_contract = w3.eth.contract(address = cfa_address, abi = abi_cfa_contract)
gda_contract = w3.eth.contract(address = gda_address, abi = abi_gda_contract)
sdegen_contract = w3.eth.contract(address = super_degen_address, abi = abi_super_degen)

# Handle text messages
# Handle text messages
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = update.message.text

    print(f"Received text: {text}")

    if chat_id in user_data and 'state' in user_data[chat_id] and not registered_status.get(chat_id, False):
        if user_data[chat_id]['state'] == 'AWAITING_FID':
            await handle_fid(update, context, text)
        elif user_data[chat_id]['state'] == 'AWAITING_GAS_PRICE':
            try:
                gas_price = float(text)
                user_data[chat_id]['gas_alert_price'] = gas_price
                user_data[chat_id]['last_gas_alert'] = 0  # Inicializar la última alerta de gas
                user_data[chat_id]['state'] = 'GAS_ALERT_ACTIVE'
                print(f"Set gas alert for user {chat_id} at price {gas_price} ETH")
                await update.message.reply_text(f"Gas alert set for {gas_price} ETH.")
                await show_settings_menu(update, context)
            except ValueError:
                print(f"Invalid gas price entered by user {chat_id}: {text}")
                await update.message.reply_text("Please enter a valid gas price.")
                await show_gas_alerts_menu(update, context)
        else:
            await show_main_menu(update, context)
    elif registered_status.get(chat_id, False):
        if user_data[chat_id]['state'] == 'USER_INFO_MENU':
            await handle_user_info_menu(update, context, text)
        elif user_data[chat_id]['state'] == 'GENERAL_INFO_MENU':
            await handle_general_info_menu(update, context, text)
        elif user_data[chat_id]['state'] == 'CHANNEL_SUBSCRIPTION_MENU':
            await handle_channel_subscription_menu(update, context, text)
        elif user_data[chat_id]['state'] == 'SETTINGS_MENU':
            await handle_settings_menu(update, context, text)
        elif user_data[chat_id]['state'] == 'PRICE_ALERTS_MENU':
            await handle_price_alerts_menu(update, context, text)
        elif user_data[chat_id]['state'] == 'GAS_ALERTS_MENU':
            await handle_gas_alerts_menu(update, context, text)
        elif user_data[chat_id]['state'] == 'FREQUENCY_MENU':
            await handle_frequency_menu(update, context, text)
        elif user_data[chat_id]['state'] == 'UNSUBSCRIBED_ALERTS_MENU':
            await handle_unsubscribed_alerts_menu(update, context, text)
        elif user_data[chat_id]['state'] == 'CLAIM_ALERTS_MENU':
            await handle_claim_alerts_menu(update, context, text)
        else:
            if text == 'User information':
                await handle_channel_option(update, context)  # Mostrar la información del canal
                await show_user_info_menu(update, context)  # Mostrar el menú con los botones adicionales
            elif text == 'General information':
                await show_general_info_menu(update, context)
            elif text == 'Degen price':
                await search_degen_price(update, context)
            elif text == 'Gas price':
                await search_gas_price(update, context)
            elif text == 'Alerts':
                await show_settings_menu(update, context)
            else:
                await show_main_menu(update, context)
    else:
        await start(update, context)

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

# # Function to return information about the bot
# async def send_info_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     info_message = (
#         "AlfaFren Bot Information:\n\n"
#         "Features:\n"
#         "- /start: Start the bot and register your details.\n"
#         "- /info: Get information about the bot and its features.\n"
#         "- Price Alerts: Get notified when the price of Degen or gas changes.\n"
#         "- User Information: View details about your channel and account.\n"
#         "- Settings: Configure your alerts and preferences.\n"
#         "- Unsubscribed Alerts: Get notified when someone unsubscribes from your channel.\n"
#     )
#     await update.message.reply_text(info_message)
    
async def handle_fid(update: Update, context: ContextTypes.DEFAULT_TYPE, fid: str):
    chat_id = update.effective_chat.id
    try:
        user_info = user_information(fid)
        if user_info:
            user_info_json = json.loads(user_info)  # Parse JSON response
            channel_id = user_info_json['channeladdress']
            account_id = user_info_json['userAddress']
            handle = user_info_json['handle']
            user_data[chat_id] = {
                'channel_id': channel_id,
                'account_id': account_id,
                'handle': handle,
                'fid': fid,
                'state': 'MAIN_MENU'
            }
            registered_status[chat_id] = True
            await update.message.reply_text(f"Welcome {handle}! Your FID has been registered.")
            await show_main_menu(update, context)
        else:
            await update.message.reply_text("No user information found for the provided FID.")
            user_data[chat_id]['state'] = 'AWAITING_FID'
    except Exception as e:
        await update.message.reply_text(f"Error retrieving user information: {e}")
        user_data[chat_id]['state'] = 'AWAITING_FID'

# Handle configuration menu options
async def handle_settings_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
    chat_id = update.effective_chat.id
    if text == 'Price':
        await show_price_alerts_menu(update, context)
    elif text == 'Gas Alerts':
        await show_gas_alerts_menu(update, context)
    elif text == 'Unsubscribed':
        await show_unsubscribed_alerts_menu(update, context)
    elif text == 'Claim':
        await show_claim_alerts_menu(update, context)  # Redirigir al menú de Claim Alerts
    elif text == 'Back':
        await show_main_menu(update, context)
    else:
        await show_settings_menu(update, context)

# Handle price alerts menu options
async def handle_price_alerts_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
    chat_id = update.effective_chat.id
    if text == 'ON':
        await show_frequency_menu(update, context)
    elif text == 'OFF':
        # Cancel existing job if it exists
        if chat_id in price_alert_jobs:
            price_alert_jobs[chat_id].remove()
            del price_alert_jobs[chat_id]
            await update.message.reply_text("Price alerts turned off.")
        await show_settings_menu(update, context)
    elif text == 'Back':
        await show_settings_menu(update, context)
    else:
        await show_price_alerts_menu(update, context)

# Handle frequency menu options
async def handle_frequency_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
    chat_id = update.effective_chat.id
    frequency_map = {
        '2 hours': 120,
        '6 hours': 360,
        '24 hours': 1440
    }
    if text in frequency_map:
        frequency = frequency_map[text]
        # Cancel existing job if it exists
        if chat_id in price_alert_jobs:
            price_alert_jobs[chat_id].remove()
        # Schedule new job
        job = scheduler.add_job(send_price_alert, 'interval', minutes=frequency, args=[update, context])
        price_alert_jobs[chat_id] = job
        await update.message.reply_text(f"Price alerts set to every {text}.")
        await show_settings_menu(update, context)
    elif text == 'Back':
        await show_price_alerts_menu(update, context)
    else:
        await show_frequency_menu(update, context)

async def handle_unsubscribed_alerts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if 'unsubscribed_alert' not in user_data[chat_id]:
        user_data[chat_id]['unsubscribed_alert'] = True
        await update.message.reply_text("Unsubscribed alerts have been turned ON.")
    else:
        user_data[chat_id]['unsubscribed_alert'] = not user_data[chat_id]['unsubscribed_alert']
        status = "ON" if user_data[chat_id]['unsubscribed_alert'] else "OFF"
        await update.message.reply_text(f"Unsubscribed alerts have been turned {status}.")
    await show_settings_menu(update, context)

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
# Handle user info menu options
async def handle_user_info_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
    chat_id = update.effective_chat.id
    if text == 'Channel':
        await handle_channel_address(update, context)
    elif text == 'Account':
        await handle_account_address(update, context)
    elif text == 'Back':
        await show_main_menu(update, context)
    else:
        await show_user_info_menu(update, context)

# Handle channel address option
async def handle_channel_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if 'channel_id' in user_data[chat_id]:
        channel_id = user_data[chat_id]['channel_id']
        await update.message.reply_text(f"Your channel address is: {channel_id}")
        await show_user_info_menu(update, context)
    else:
        await update.message.reply_text("Channel ID not set.")
        await show_user_info_menu(update, context)

# Handle Claim Alerts menu options
async def handle_claim_alerts_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
    chat_id = update.effective_chat.id

    if text == 'ON':
        user_data[chat_id]['claim_alerts_active'] = True
        response = "Claim Alerts have been turned ON. You will be notified to claim your rewards every 22 hours if needed."
        # Inicia la tarea si aún no está activa
        if 'claim_alert_task' not in user_data[chat_id]:
            user_data[chat_id]['claim_alert_task'] = asyncio.create_task(check_and_alert_claim_time_periodically(update, context, chat_id))
    elif text == 'OFF':
        user_data[chat_id]['claim_alerts_active'] = False
        response = "Claim Alerts have been turned OFF."
        # Cancela la tarea si está activa
        if 'claim_alert_task' in user_data[chat_id]:
            user_data[chat_id]['claim_alert_task'].cancel()
            del user_data[chat_id]['claim_alert_task']
    else:
        response = "Invalid option."

    await update.message.reply_text(response)
    await show_settings_menu(update, context)

async def check_and_alert_claim_time_periodically(update, context, chat_id):
    while user_data[chat_id]['claim_alerts_active']:
        try:
            account_id = user_data[chat_id]['account_id']
            last_claimed_timestamp = functions.get_last_claim_info(account_id)
            current_time = int(time.time())
            if (current_time - int(last_claimed_timestamp)) > 79200:#79200:  # 22 hours in seconds
                await update.message.reply_text("It's time to claim your rewards!")
        except Exception as e:
            await update.message.reply_text(f"Error processing claim information: {str(e)}")
        await asyncio.sleep(79200)  # Espera 22 horas antes de comprobar de nuevo

async def check_and_alert_claim_time(update, context, account_id):
    try:
        # La función get_last_claim_info ahora devuelve directamente el último timestamp de reclamación
        last_claimed_timestamp = functions.get_last_claim_info(account_id)
        
        # Verificar que last_claimed_timestamp no sea un mensaje de error
        if last_claimed_timestamp and last_claimed_timestamp.isdigit():
            last_claimed_timestamp = int(last_claimed_timestamp)
            current_time = int(time.time())
            if (current_time - last_claimed_timestamp) > 79200:  # 22 hours in seconds
                await update.message.reply_text("It's time to claim your rewards!")
            else:
                await update.message.reply_text("No need to claim yet.")
        else:
            await update.message.reply_text(last_claimed_timestamp)  # Muestra el mensaje de error de la función
    except Exception as e:
        await update.message.reply_text(f"Error processing claim information: {str(e)}")

# Handle account address option
async def handle_account_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if 'account_id' in user_data[chat_id]:
        account_id = user_data[chat_id]['account_id']
        await update.message.reply_text(f"Your account address is: {account_id}")
        await show_user_info_menu(update, context)
    else:
        await update.message.reply_text("Account ID not set.")
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
from api_calls import channel_information
import json

# Handle channel option
async def handle_channel_option(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if 'channel_id' in user_data[chat_id]:
        channel_id = user_data[chat_id]['channel_id']
        user_address = user_data[chat_id]['account_id']
        try:
            channel_info = channel_information(channel_id)
            
            if channel_info:
                channel_info_json = json.loads(channel_info)

                title = channel_info_json['title']
                number_of_subscribers = channel_info_json['numberOfSubscribers']
                number_of_stakers = channel_info_json['numberOfStakers']

                subscription_cost_input = int(channel_info_json['totalSubscriptionFlowRate'])/number_of_subscribers
                if subscription_cost_input == 190258751902587:
                    subscription_cost = 500
                elif subscription_cost_input == 380517503805175:
                    subscription_cost = 1000
                else:
                    subscription_cost = 1500
                subscribers_income = number_of_subscribers * 0.25 * subscription_cost
                # stake_to_income_ratio = (float(channel_info_json['stakeToIncomeRatio'])/1e11)*60*60*24*365/12
                subscribers_income = round(subscribers_income)
                total_subscription_inflow_amount = round(float(channel_info_json['totalSubscriptionInflowAmount'])/1e18)
                total_claimed = round(float(channel_info_json['totalClaimed'])/1e14)
                current_staked = round(float(channel_info_json['currentStaked'])/1e14)

                flow_rate = cfa_contract.functions.getAccountFlowrate(super_degen_address, user_address).call()
                net_flow = gda_contract.functions.getNetFlow(super_degen_address, user_address).call()
                degenx_balance = sdegen_contract.functions.balanceOf(user_address).call()

                flow_rate_month = flow_rate/1e18*60*60*24*365/12
                net_flow_month = round(net_flow/1e18*60*60*24*365/12)
                degenx_balance = round(degenx_balance/1e18)
                total_result = round(net_flow_month + flow_rate_month)
                
                message = (
                    f"📢 Channel Information for {title} 📢\n\n"
                    f"👥 Number of subscribers: {number_of_subscribers}\n"
                    f"🔒 Number of stakers: {number_of_stakers}\n"
                    f"💰 Subscribers income: {subscribers_income} DEGENx\n"
                    f"💰 Total income: {net_flow_month} DEGENx\n"
                    f"💰 Total netflow: {total_result} DEGENx\n"
                    f"📊 Volume: {total_subscription_inflow_amount} DEGENx\n"
                    f"🤑 Total claimed: {total_claimed} ALFA\n"
                    f"🔗 Current staked: {current_staked} ALFA\n"
                    f"👛 Your DEGENx Balance: {degenx_balance} tokens\n"
                )

                await update.message.reply_text(message)
    
            else:
                await update.message.reply_text("No channel information found.")
                await show_user_info_menu(update, context)
        except Exception as e:
            await update.message.reply_text(f"Error retrieving channel information: {e}")
            await show_user_info_menu(update, context)
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
        mensaje = f"Current Degen price: ${degen_price:.3f} USD"
        await update.message.reply_text(mensaje)
    except Exception as e:
        await update.message.reply_text(f"Error obtaining degen price: {e}")
    await show_main_menu(update, context)

# Search gas price
async def search_gas_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        gas_price = functions.obtain_gas_price(w3) / 10e8 # Attempt to fetch the current gas price
        message = f"Gas base fee: {gas_price:.3f} GWEI"
        await update.message.reply_text(message)
    except Exception as e:
        await update.message.reply_text(f"Error obtaining gas price: {e}")
    await show_main_menu(update, context)

# Send price alert
async def send_price_alert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    try:
        degen_price = await functions.obtain_degen_price() # Attempt to fetch the current price of Degen (ETH)
        mensaje = f"Current Degen price: ${degen_price:.3f} USD"
        await context.bot.send_message(chat_id=chat_id, text=mensaje)
    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"Error obtaining degen price: {e}")

async def handle_gas_alerts_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
    chat_id = update.effective_chat.id
    if text == 'ON':
        user_data[chat_id]['state'] = 'AWAITING_GAS_PRICE'
        await update.message.reply_text("Please enter the gas price for your alert:")
    elif text == 'OFF':
        if chat_id in user_data and 'gas_alert_price' in user_data[chat_id]:
            del user_data[chat_id]['gas_alert_price']
            del user_data[chat_id]['last_gas_alert']
        await update.message.reply_text("Gas alerts have been turned OFF.")
        await show_settings_menu(update, context)
    elif text == 'Back':
        await show_settings_menu(update, context)
    else:
        await show_gas_alerts_menu(update, context)

async def check_gas_price(bot):
    try:
        current_gas_price = obtain_gas_price(w3) / 10e8  # Obtener el precio del gas
        # print(f"Current gas price: {current_gas_price} ETH")
    except Exception as e:
        print(f"Error obtaining gas price: {e}")
        return

    for chat_id, data in user_data.items():
        if 'gas_alert_price' in data and 'last_gas_alert' in data:
            gas_alert_price = data['gas_alert_price']
            last_alert_time = data['last_gas_alert']
            current_time = int(asyncio.get_event_loop().time())  # Obtener el tiempo actual
            print(f"Checking alerts for user {chat_id}: gas_alert_price={gas_alert_price}, last_alert_time={last_alert_time}")

            if current_gas_price < gas_alert_price and (current_time - last_alert_time) >= 60:
                try:
                    await bot.send_message(chat_id=chat_id, text=f"Gas price is below {gas_alert_price} ETH: {current_gas_price} ETH")
                    user_data[chat_id]['last_gas_alert'] = current_time  # Actualizar el tiempo de la última alerta
                    print(f"Alert sent to user {chat_id}")
                except Exception as e:
                    print(f"Error sending message to user {chat_id}: {e}")
            else:
                print(f"No alert sent for user {chat_id}: current_gas_price={current_gas_price}, gas_alert_price={gas_alert_price}, time_since_last_alert={current_time - last_alert_time}")

async def check_gas_price_periodically(bot):
    while True:
        await check_gas_price(bot)
        await asyncio.sleep(60)  # Check every 5 minutes

async def check_unsubscribed_users_periodically(bot):
    while True:
        await check_unsubscribed_users(bot)
        await asyncio.sleep(300)  # Check every 5 minutes

async def check_unsubscribed_users(bot):
    for chat_id, data in user_data.items():
        if 'unsubscribed_alert' in data and data['unsubscribed_alert']:
            if 'channel_id' in data:
                channel_id = data['channel_id']
                unsubscribed_users = get_unsubscribed_channels_with_timestamp(channel_id)
                for user in unsubscribed_users:
                    user_id = user['id']
                    unsubscribed_time = int(user['timestamp'])
                    if 'last_unsubscribed_alert' not in data or unsubscribed_time > data['last_unsubscribed_alert']:
                        try:
                            await bot.send_message(chat_id=chat_id, text=f"User {user_id} has unsubscribed from your channel.")
                            user_data[chat_id]['last_unsubscribed_alert'] = unsubscribed_time
                        except Exception as e:
                            print(f"Error sending unsubscribed alert to {chat_id}: {e}")

async def handle_unsubscribed_alerts_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
    chat_id = update.effective_chat.id
    if text == 'ON':
        user_data[chat_id]['unsubscribed_alert'] = True
        await update.message.reply_text("Unsubscribed alerts have been turned ON.")
        user_data[chat_id]['state'] = 'SETTINGS_MENU'  # Actualizar estado
        await show_settings_menu(update, context)
    elif text == 'OFF':
        user_data[chat_id]['unsubscribed_alert'] = False
        await update.message.reply_text("Unsubscribed alerts have been turned OFF.")
        user_data[chat_id]['state'] = 'SETTINGS_MENU'  # Actualizar estado
        await show_settings_menu(update, context)
    elif text == 'Back':
        user_data[chat_id]['state'] = 'SETTINGS_MENU'  # Actualizar estado
        await show_settings_menu(update, context)
    else:
        await show_unsubscribed_alerts_menu(update, context)

# Configuration command handler
async def configuration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_data[chat_id] = {'state': 'AWAITING_CHANNEL_ID'}
    registered_status[chat_id] = False
    await update.message.reply_text("Please enter your channel ID to update:", reply_markup=ReplyKeyboardRemove())

async def set_bot_commands(application):
    commands = [
        BotCommand(command="/start", description="Start the bot and register your details"),
        BotCommand(command="/info", description="Get information about the bot and its features"),
        BotCommand(command="/price", description="Returns the current Degen price"),
        BotCommand(command="/gwei", description="Returns the current base fee"),
        BotCommand(command="/configuration", description="Update your channel and account IDs")
    ]
    await application.bot.set_my_commands(commands)
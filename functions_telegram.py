from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import requests, os, dotenv
import functions
from web3 import Web3
rpc_url = os.environ['BASE']
w3 = Web3(Web3.HTTPProvider(rpc_url))
dotenv.load_dotenv()

user_states = {}
user_wallets = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Asynchronously initiates the interaction with the user in a Telegram chat.

    This function is triggered when a user starts a conversation with the bot or
    requests to go back to the main menu. It displays a custom keyboard with
    various options for the user to choose from, guiding them through the
    bot's functionalities.
    """
    # Create a markup for the keyboard layout to be used as a reply
    reply_keyboard = [['User information', 'General information'],
                      ['Degen price', 'Gas price']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    # Send a greeting message with the custom reply keyboard
    await update.message.reply_text(
        "Hey! Welcome to the best alfafrens bot ¿What do you want to do?",
        reply_markup = markup
    )

async def obtain_degen_price():
    """
    Asynchronously fetches the current price of degen (ETH) in USD.

    This function makes an HTTP GET request to the CoinGecko API to retrieve
    the latest price of degen in US dollars. It parses the JSON response
    to extract the price and then returns it.
    """
    url = "https://api.coingecko.com/api/v3/simple/price?ids=degen-base&vs_currencies=usd"

    try:
        response = requests.get(url) # Making an HTTP GET request to the CoinGecko API
        data = response.json()
        degen_price = data["degen-base"]["usd"]
        return degen_price
    except Exception as e:
        # Raising an exception if the HTTP request fails or the response cannot be parsed
        raise Exception(f"Error fetching Degen price: {e}")

async def search_degen_price(update: Update, context: ContextTypes.DEFAULT_TYPE):

    """
    Asynchronously retrieves and sends the current price of Degen to the user.

    This function is triggered when a user requests the current price of Degen.
    It fetches the latest price through the 'obtain_degen_price' function and
    sends it to the user. If there is an error during the fetching process, the
    function handles it and informs the user.

    The function attempts to:
    - Fetch the current price of Degen.
    - Format and send the price to the user.
    - Handle any exceptions that occur during the process.
    """

    try:
        degen_price = await obtain_degen_price() # Attempt to fetch the current price of Ethereum
        mensaje = f"Actual Degen price: ${degen_price} USD"
        await update.message.reply_text(mensaje)
    except Exception as e:
        await update.message.reply_text(f"Error obtaining degen price: {e}")

async def search_gas_price(update: Update, context: ContextTypes.DEFAULT_TYPE):

    """
    Asynchronously retrieves and sends the current price of Degen to the user.

    This function is triggered when a user requests the current price of Degen.
    It fetches the latest price through the 'obtain_degen_price' function and
    sends it to the user. If there is an error during the fetching process, the
    function handles it and informs the user.

    The function attempts to:
    - Fetch the current price of Degen.
    - Format and send the price to the user.
    - Handle any exceptions that occur during the process.
    """

    try:
        gas_price = functions.obtain_gas_price(w3)/10e8 # Attempt to fetch the current price of Ethereum
        message = f"Gas base fee: {gas_price} GWEI"
        await update.message.reply_text(message)
    except Exception as e:
        await update.message.reply_text(f"Error obtaining degen price: {e}")

async def handle_menu_response(update: Update, context: ContextTypes.DEFAULT_TYPE):

    """
    Asynchronously handles the user's response to the custom reply keyboard menu in a Telegram chat.

    This function is triggered when a user selects an option from the custom reply keyboard. 
    It identifies the user's choice based on the text of the message and executes the corresponding action, 
    such as initiating wallet analysis, fetching the current price of ETH, showing copy trade wallets, 
    or responding to unhandled options.
    """

    text = update.message.text
    chat_id = update.effective_chat.id

    # Handle the 'Analizar Wallet' option
    if text == 'User information':
        user_states[chat_id] = 'AWAITING_WALLET'
        await update.message.reply_text("Please, send my your channel", reply_markup=ReplyKeyboardRemove())
    
   # Handle the 'Degen price' option
    elif text == 'Degen price':
        await search_degen_price(update, context)
        user_states[chat_id] = None

    elif text == 'Gas price':
        await search_gas_price(update, context)
        user_states[chat_id] = None

    elif text == 'General information':
        reply_keyboard = [['Channels', 'Others']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        await update.message.reply_text("Please choose an option:", reply_markup=markup)
        user_states[chat_id] = 'GENERAL_INFO'
    elif text == 'Channels' and user_states.get(chat_id) == 'GENERAL_INFO':
        reply_keyboard = [['500', '1000', '1500']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        await update.message.reply_text("Please choose monthly subscription cost channel:", reply_markup=markup)
        user_states[chat_id] = 'CHANNELS'
    elif text in ['500', '1000', '1500'] and user_states.get(chat_id) == 'CHANNELS':
        # Call the function to get channels subscription cost
        try:
            channel_ids = functions.get_channels_subscription_cost(text)
            if isinstance(channel_ids, list):
                await send_long_message(update, context, channel_ids, text)
            else:
                await update.message.reply_text(channel_ids)
        except Exception as e:
            await update.message.reply_text(f"Error: {e}")
        user_states[chat_id] = None
    elif text == 'Others' and user_states.get(chat_id) == 'GENERAL_INFO':
        await update.message.reply_text("Other information here...")
        user_states[chat_id] = None

    # Default response for unhandled options
    else:
        await update.message.reply_text("Funcion disponible para usuarios premium, se necesita comprar 500 dolares en matiteach coin para acceder")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Asynchronously handles text input based on the current state of the user in a chat.

    This function is designed to work within a chatbot framework, handling user input
    based on the state of the user's interaction. It manages two primary states: 
    when the user is expected to provide a wallet address, and all other cases.

    Args:
    update (Update): An object representing an incoming update. Contains information 
                     about the chat, the user, and the message.
    context (ContextTypes.DEFAULT_TYPE): An object that holds context-specific information
                                         and states relevant to this interaction.

    """

    chat_id = update.effective_chat.id
    text = update.message.text

    # Caso para manejar el botón 'Precio ETH'
    if text == 'Degen price':
        await search_degen_price(update, context)

    elif text == 'Gas price':
        await search_gas_price(update, context)

    elif user_states.get(chat_id) == 'AWAITING_WALLET':
        # Manejar la entrada de la dirección de la wallet
        user_wallets[chat_id] = text
        wallet = user_wallets.get(chat_id)
        if wallet:
            await channel_information(update, context, wallet)
            user_states[chat_id] = None
            del user_wallets[chat_id]
    else:
        # Manejar otros casos (o un menú general si lo tienes)
        await handle_menu_response(update, context)

async def channel_information(update: Update, context: ContextTypes.DEFAULT_TYPE, wallet):
    chat_id = update.effective_chat.id
    try:
        result = functions.get_account_by_id(wallet)
        number_of_suscribers = result[0]
        net_flow_rate = result[1]
        title = "Channel information"

        message = f"{title}\n"
        message += f"Number of suscribers: {number_of_suscribers}\n"
        message += f"Net flow rate: {net_flow_rate}\n"
        
        await context.bot.send_message(chat_id=chat_id, text=message)
        user_states[chat_id] = None

    except ValueError as ve:
        await context.bot.send_message(chat_id=chat_id, text=str(ve))
    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text="Error buscando movimientos, vuelve a ingresar una wallet")

async def send_long_message(update: Update, context: ContextTypes.DEFAULT_TYPE, channel_ids, cost):
    """
    Helper function to send long messages in chunks to avoid exceeding Telegram's message length limit.
    """
    message_chunk_size = 4000  # Telegram message limit is 4096 characters
    message = f"Channel IDs with subscription cost {cost}:\n"
    message += "\n".join(channel_ids)
    
    for start in range(0, len(message), message_chunk_size):
        await update.message.reply_text(message[start:start+message_chunk_size])
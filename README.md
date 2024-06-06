# AlfaFren Bot
The AlfaFren Bot is a Telegram bot designed to interact with the Alfafrens platform, providing various functionalities such as monitoring price alerts, gas alerts, user information, and unsubscribed alerts.

## Table of Contents

- [Overview](#overview)
- [Scripts](#scripts)
  - [telegram_bot_alfafrens](#telegram_bot_alfafrens)
  - [functions_telegram](#functions_telegram)
  - [functions](#functions)
  - [menu_functions_telegram](#menu_functions_telegram)
  - [api_calls](#api_calls)
  - [message_handlers](#message_handlers)
  - [queries](#queries)
- [Usage](#usage)
- [Commands](#commands)

## Overview

The AlfaFren Bot is designed to automate interactions with the Alfafrens platform. It allows users to receive notifications for price and gas alerts, view user and channel information, and be notified when someone unsubscribes from their channel.

## Scripts

### functions_telegram.py
- Purpose: This script contains the main logic for handling user interactions and bot commands.
- Usage: Handles user state, processes messages, and manages alerts.

### menu_function_telegram.py
- Purpose: Contains functions related to displaying menus and handling menu selections.
- Usage: Displays various menus and handles user inputs for navigating the bot's features.

### api_calls.py
- Purpose: Contains functions to interact with the Alfafrens API.
- Usage: Fetches user and channel information from the Alfafrens platform.

## Usage

1. Ensure you have Python installed on your system.
2. Install the required dependencies using pip install -r requirements.txt.
3. Set up the environment variables for the Telegram bot token and other required configurations.

## Commands
To run the AlfaFren Test Bot in the background, you can use the following commands:

```shell
nohup python3 -u telegram_bot_alfafrens.py > /dev/null 2>&1 &
ps aux | grep 'telegram_bot_alfafrens.py' # Search the process

# Wallet Watchers

The Wallet Watchers project is a collection of scripts designed to monitor, analyze, copy trade wallets and potentially buy shitcoins. The main scripts are: `copy-trading`, `token-sells`, and ``.

## Table of Contents

- [Overview](#overview)
- [Scripts](#scripts)
  - [copy_trading](#copy_trading)
  - [token_sells](#token_sells)
- [Usage](#usage)
- [To do](#todo)
- [Commands](#commands)

## Overview

The Liquidation Bot is designed to automate the process of monitoring and potentially liquidating wallets on the Exactly platform. It leverages blockchain data, calculates wallet health factors, and identifies wallets that are eligible for liquidation based on specific criteria.

## Scripts

### copy-trading

- Purpose: This script retrieves events from the Exactly platform and stores them in a database for further analysis.
- Usage: Run this script to collect event data.
- Database: Stores events data.

### token-sells

- Purpose: Monitors Ethereum blocks for transactions related to the configured wallet address and processes incoming and outgoing token transfers.
- Usage: It fetches the transaction history for the wallet, analyzes each transaction, and identifies token purchases. For each detected token purchase, it spawns a new thread to handle the purchase process.

## Usage

To use the Wallet Watchers project, follow these steps:
1. Run the `copy-trading` script to copy trade wallets in ethereum mainnet on demand.
2. Run the `token-sells` script to sell the tokens that the copy trade bought automatically when the profit of the bought is 1.5x.

## To do
1. Estudiar como funcionan los builders en MEV y agregarlo para operar (pagarle)
2. Agregar que si compra de token tiene limite no nos rebote la tx y compré lo máximo
3. Agregar como se divide la entrada entre MEV builder y la salida de eth real (Compra)
4. División en la tx de cuanto fue gas

## Commands
To run the Wallet Watchers project in the background, you can use the following commands:


## Alchemy mail
madero.copytrading@gmail.com
potbyr-Tiqwi5-nymhix


```shell
nohup python3 -u telegram_bot_alfafrens.py > /dev/null 2>&1 &


ps aux | grep 'telegram_bot_HIB.py' # Search the process
ps aux | grep 'token_sells.py' # Search the process
ps aux | grep 'wallet_analyzer.py' # Search the process
ps aux | grep 'wallet_analyzer_sheet.py' # Search the process

nohup python3 -u wallet_analyzer.py > ./logs/bot_telegram-01-23.log 2>&1 &

tokensells@gmail.com
maderocopytraiding@gmail.com
maderowalletwatcherbalance@gmail.com# Alfafrens-Bot

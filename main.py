from functions import get_account_by_id, get_all_accounts, get_channels_subscription_cost, get_channels_subscribed, get_unsubscribed_channels
import pandas as pd

def main():
    # Ejemplo: Obtener una cuenta por ID
    # account_id = "0xfe5b79144afeb94912d149c192b162530de5561d"
    # result = get_account_by_id(account_id)
    # print(result)

    # df = get_all_accounts()
    # if df is not None:
    #     print(df)

    channel = 500
    # result = get_channels_subscription_cost(channel)
    # print(result)
    # # print("Data saved to 'tokens_ohcl.csv'")
    account_id = "0x292f9892a9bc702dd3ca785e7287718da4479865"  # Replace with the actual account ID
    # result = get_channels_subscribed(account_id)
    # print(len(result))
    # print(result)

    unsubscribed_channels = get_unsubscribed_channels(account_id, channel)
    print(unsubscribed_channels)

if __name__ == '__main__':
    main()
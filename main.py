from functions import get_account_by_id, get_all_accounts, get_channels_subscription_cost, get_channels_subscribed, get_unsubscribed_channels, get_unsubscribed_channels_with_matching_flow_operator, get_better_channels_to_follow, get_last_claim_info
import pandas as pd, time

def check_and_alert_claim_time(account_id):
        # Suponiendo que get_last_claim_info es la función correcta que devuelve los timestamps de los eventos de reclamación
        pool_info = get_last_claim_info(account_id)
        if pool_info and all('distributionClaimedEvents' in member for member in pool_info):
            max_timestamp = max(
                int(event['timestamp']) 
                for member in pool_info 
                for event in member['distributionClaimedEvents']
            )
            current_time = int(time.time())
            print(max_timestamp)
            print(current_time)
            if (current_time - max_timestamp) > 79200:  # 22 hours in seconds
                
                print("entro")
        else:
            print("hola")

def main():
    # Ejemplo: Obtener una cuenta por ID
    # account_id = "0xfe5b79144afeb94912d149c192b162530de5561d"
    # result = get_account_by_id(account_id)
    # print(result)

    # df = get_all_accounts()
    # if df is not None:
    #     print(df)
    # result = get_channels_subscription_cost(channel)
    # print(result)
    # # print("Data saved to 'tokens_ohcl.csv'")
    account_id = "0x4af3d323fc28a8d72cbeb3bdcba44644d5aab2cb"  # Replace with the actual account ID
    result = get_last_claim_info(account_id)
    print(result)

    result_2 = check_and_alert_claim_time(account_id)
    print(result_2)


    # result = get_channels_subscribed(account_id)
    # print(len(result))
    # print(result)

    # unsubscribed_channels = get_unsubscribed_channels(account_id, channel)
    
    
    # unsubscribed_channels = get_unsubscribed_channels_with_matching_flow_operator(account_id)
    # print(unsubscribed_channels)
    # print(len(unsubscribed_channels))

    # channels = get_better_channels_to_follow(1000)
    # print("channels")
    # print(channels)

if __name__ == '__main__':
    main()
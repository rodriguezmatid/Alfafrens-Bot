import requests, pandas as pd, os, dotenv
from queries import query_account_by_id, query_all_accounts, query_channels_subscription_cost
from web3 import Web3
dotenv.load_dotenv()

rpc_url = os.environ['BASE']
w3 = Web3(Web3.HTTPProvider(rpc_url))
url = 'https://base-mainnet.subgraph.x.superfluid.dev/'

def obtain_gas_price(web3):
    return web3.eth.gas_price

# def search_gas_price():
#     gas_price(w3)

def run_query(query):
    response = requests.post(url, json={'query': query})
    if response.status_code == 200:
        data = response.json()
        if 'errors' in data:
            print(f'Errores en la respuesta: {data["errors"]}')
            return None
        elif 'data' in data:
            return data['data']
        else:
            print(f'La respuesta no contiene la estructura esperada: {data}')
            return None
    else:
        print(f'Error {response.status_code}: {response.text}')
        return None

def get_account_by_id(account_id):
    query = query_account_by_id(account_id)
    data = run_query(query)
    if data and 'accounts' in data and data['accounts']:
        account = data['accounts'][0]
        if 'accountTokenSnapshots' in account and account['accountTokenSnapshots']:
            snapshots = account['accountTokenSnapshots'][0]
            total_streams = snapshots.get('totalNumberOfActiveStreams', 'N/A')
            net_flow_rate = snapshots.get('totalNetFlowRate', 'N/A')
            return total_streams, net_flow_rate
        else:
            return 'No se encontraron snapshots de tokens para esta cuenta.', None
    else:
        return 'No se encontró la cuenta con el ID proporcionado.', None

# Function to get channels subscription cost
def get_channels_subscription_cost(subscription_cost_input):
    if subscription_cost_input == '500':
        subscription_cost = '190258751902587'
    elif subscription_cost_input == '1000':
        subscription_cost = '380517503805175'
    else:
        subscription_cost = '570776255707762'

    query = query_channels_subscription_cost(subscription_cost)
    data = run_query(query)
    
    if data and 'accounts' in data:
        accounts = data['accounts']
        ids = [account['id'] for account in accounts]
        return ids
    else:
        return 'No accounts found with the given subscription cost.'

def get_all_accounts():
    query = query_all_accounts()
    data = run_query(query)
    if data is None:
        return None

    # Extraer los 'id' de las 'accounts'
    accounts = [item['id'] for item in data['accounts']]

    # Crear un DataFrame y contar las ocurrencias de los 'id'
    df = pd.DataFrame(accounts, columns=['sender_id'])
    count_series = df['sender_id'].value_counts().reset_index()
    count_series.columns = ['sender_id', 'count']

    return count_series
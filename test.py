import requests
import os
from string import Template
import dotenv

dotenv.load_dotenv()

url = 'https://base-mainnet.subgraph.x.superfluid.dev/'

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

def query_channels_subscribed(account_id):
    print(account_id)
    return Template('''
    {
      accounts(
          where: {
            inflows_: {
              sender: "0x292f9892A9Bc702dd3cA785E7287718dA4479865", 
              token: "0x1eff3dd78f4a14abfa9fa66579bd3ce9e1b30529"
            }
          }
        ) {
          id
      }
    }''').substitute(account_id=account_id)

def get_channels_subscribed(account_id):
    query = query_channels_subscribed(account_id)
    print(query)
    data = run_query(query)
    
    if data and 'accounts' in data:
        accounts = data['accounts']
        ids = [account['id'] for account in accounts]
        return ids
    else:
        return 'No channels found for the given account.'

# Ejemplo de uso
account_id = "0x292f9892A9Bc702dd3cA785E7287718dA4479865"
channels = get_channels_subscribed(account_id)
print(f"Channels subscribed by account {account_id}: {channels}")
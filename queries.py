# import requests

# # Define la URL del endpoint del subgrafo
# url = 'https://base-mainnet.subgraph.x.superfluid.dev'

# # Define la consulta GraphQL sin filtro
# query = '''
# {
#   accounts {
#     id
#     isSuperApp
#     inflows {
#       currentFlowRate
#       token {
#         symbol
#       }
#       sender {
#         id
#       }
#     }
#     outflows {
#       currentFlowRate
#       token {
#         symbol
#       }
#       receiver {
#         id
#       }
#     }
#     accountTokenSnapshots {
#       token {
#         id
#       }
#       totalNumberOfActiveStreams
#       totalNetFlowRate
#     }
#   }
# }
# '''

# # Realiza la solicitud POST al endpoint del subgrafo
# response = requests.post(url, json={'query': query})

# # Verifica si la solicitud fue exitosa
# if response.status_code == 200:
#     # Procesa la respuesta JSON
#     data = response.json()
#     if 'errors' in data:
#         print('Errores en la respuesta:', data['errors'])
#     elif 'data' in data and 'accounts' in data['data']:
#         accounts = data['data']['accounts']
#         if accounts:
#             print('Datos de las cuentas:', accounts)
#         else:
#             print('No se encontraron cuentas.')
#     else:
#         print('La respuesta no contiene la estructura esperada:', data)
# else:
#     print(f'Error {response.status_code}: {response.text}')

# queries.py

from string import Template

def query_account_by_id(account_id):
    return Template('''
    {
      accounts(where: { id: "$account_id" }) {
        id
        isSuperApp
        inflows {
          currentFlowRate
          token {
            symbol
          }
          sender {
            id
          }
        }
        outflows {
          currentFlowRate
          token {
            symbol
          }
          receiver {
            id
          }
        }
        accountTokenSnapshots {
          token {
            id
          }
          totalNumberOfActiveStreams
          totalNetFlowRate
        }
      }
    }
    ''').substitute(account_id=account_id)

def query_all_accounts():
    return '''
    {
      accounts {
        id
        isSuperApp
      }
    }    '''

def query_channels_subscription_cost(subscription_cost):
    return Template('''
    {
      accounts(
        skip: 0
        orderBy: createdAtBlockNumber
        orderDirection: asc
        where: {
          isSuperApp: true, 
          inflows_: {currentFlowRate: "$subscription_cost"}}
      ) {
        id
        pools {
          perUnitFlowRate
        }
      }
    }
    ''').substitute(subscription_cost=subscription_cost)

# Agrega más consultas según sea necesario

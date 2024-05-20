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

def query_channels_subscribed(account_id):
    return f'''
    {{
      accounts(
          where: {{
            inflows_: {{
              sender: "{account_id}", 
              token: "0x1eff3dd78f4a14abfa9fa66579bd3ce9e1b30529"
            }}
          }}
        ) {{
          id
      }}
    }}'''

def query_channels_subscribed_new():
    return '''
    {
      accounts(
          where: {
            inflows_: {
              sender: "0x292f9892a9bc702dd3ca785e7287718da4479865", 
              token: "0x1eff3dd78f4a14abfa9fa66579bd3ce9e1b30529"
            }
          }
        ) {
          id
      }
    }'''
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
    return Template('''
    {
      accounts(
          where: {
            inflows_: {
              sender: "$account_id", 
              token: "0x1eff3dd78f4a14abfa9fa66579bd3ce9e1b30529"
            }
          }
        ) {
          id
      }
    }''').substitute(account_id=account_id)

def query_last_claimed_timestamp(account_id):
    # Usa la interpolación directa con `safe_substitute` para manejar de forma segura las variables
    query_template = Template('''
    query MyQuery {
      user(id: "$id") {
        lastClaimedTimestamp
      }
    }
    ''')
    query = query_template.safe_substitute(id=account_id)
    return query

def query_better_channels_to_follow_order_by_pay():
    return '''
    {
      pools(orderBy: perUnitFlowRate, orderDirection: desc, where: {}) {
          perUnitFlowRate
          admin {
            id
            inflows(first: 1, orderBy: currentFlowRate, orderDirection: desc) {
              currentFlowRate
            }
          }
      }
    }'''

def query_unsubscribed_channels(channel_id):
    return Template('''
    {
      streams(
        where: {receiver: "$channel_id", currentFlowRate: "0"}
        orderBy: updatedAtBlockNumber
        orderDirection: desc
      ) {
        sender {
          id
        }
        flowUpdatedEvents {
          flowOperator
          totalAmountStreamedUntilTimestamp
        }
        updatedAtTimestamp
      }
    }''').substitute(channel_id=channel_id)

def query_max_timestamp_claim(account_id):
    return Template('''
    {
      poolMembers(where: {account: "$account_id"}) {
        distributionClaimedEvents {
          timestamp
        }
        account {
          id
        }
      }
    }
    ''').substitute(account_id=account_id)
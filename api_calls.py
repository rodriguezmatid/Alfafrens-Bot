import requests

# Gives a boolean indicating if the profile is subscribed to your channel
def is_user_subscribed(channel_address, user_address):
    url = f"https://alfafrens.com/api/v0/isUserSubscribedToChannel?channelAddress={channel_address}&userAddress={user_address}"

    payload = {}
    headers = {
        'Accept': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.text

# Gives information about the user by FID:
# user_address
# handle
# channel_address
def user_information(fid):

    url = f"https://alfafrens.com/api/v0/getUserByFid?fid={fid}"

    payload={}
    headers = {
        'Accept': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"API request failed with status code {response.status_code}")
    
# Gives information about the user by address:
def user_information_by_address(address):

    url = f"https://alfafrens.com/api/v0/getUserByAddress?userAddress={address}"
    
    payload = {}
    headers = {'Accept': 'application/json'}
    response = requests.request("GET", url, headers=headers, data=payload)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"API request failed with status code {response.status_code}")

# Gives you information about the channels that the input FID is subscribed
def subscribed_channels_information(fid):

    url = f"https://alfafrens.com/api/v0/getUserSubscribedChannels?fid={fid}"

    payload={}
    headers = {
    'Accept': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)

# Gives information about the input channel:
# Number of subscribers
# Number of stakers
# Total subscription flow rate
# Total subscription inflow amount
# Total claimed
# Current staked
# Estimated earnings per second
# Income to stake ratio
# totalSubscriptionCashbackFlowRate
# totalSubscriptionCashbackFlowAmount
# Title
def channel_information(channel_address):
    url = f"https://alfafrens.com/api/v0/getChannel?channelAddress={channel_address}"

    payload = {}
    headers = {
        'Accept': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"API request failed with status code {response.status_code}")


# Gives detailed channel information such as subscribers and stakes
def detailed_channel_information(channel_address):
    url = f"https://alfafrens.com/api/v0/getChannelSubscribersAndStakes?channelAddress={channel_address}"

    payload={}
    headers = {
    'Accept': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)



# user_information_by_address("0x292f9892A9Bc702dd3cA785E7287718dA4479865")
# result = channel_information("0xfe5b79144afeb94912d149c192b162530de5561d")
# print(result)
# result = detailed_channel_information("0xfe5b79144afeb94912d149c192b162530de5561d")
# print(result)
# result = user_information(354894)

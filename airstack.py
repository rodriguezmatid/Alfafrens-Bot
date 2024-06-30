import os
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

AIRSTACK_API_URL = "https://api.airstack.xyz/graphql"
AIRSTACK_API_KEY = os.environ["AIRSTACK_API_KEY"]

if not AIRSTACK_API_KEY:
    raise ValueError("AIRSTACK_API_KEY not set")

transport = RequestsHTTPTransport(
    url=AIRSTACK_API_URL,
    headers={
        "Authorization": AIRSTACK_API_KEY,  # Add API key to Authorization header
    },
    use_json=True,
)

client = Client(
    transport=transport,
    fetch_schema_from_transport=True,
)

def fetch_user_id(username):
    query = gql(f"""
    query GetFarcasterUserFID {{
      Socials(input: {{filter: {{profileName: {{_eq: "{username}"}}}}, blockchain: ethereum}}) {{
        Social {{
          dappName
          profileName
          userId
        }}
      }}
    }}
    """)
    try:
        response = client.execute(query)
        socials = response.get('Socials', {}).get('Social', [])
        if socials:
            return socials[0].get('userId')
        else:
            return None
    except Exception as e:
        raise ValueError(f"Error: {str(e)}")
    
if __name__ == "__main__":
    user_id = fetch_user_id()
    if user_id:
        print(f"userId: {user_id}")
    else:
        print("No userId found")
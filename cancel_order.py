import requests
import json

# Alpaca API credentials
key_id = "PKP2V124H0HKOWUB4PJP"
secret_key = "fS9uDM3vugecsTweCgvuTVGJnXonFMOLmdwIFf7d"
  

def get_most_recent_order_id(api_key, api_secret):
    url = "https://paper-api.alpaca.markets/v2/orders?status=open&limit=1"

    headers = {
        "accept": "application/json",
        "APCA-API-KEY-ID": api_key,
        "APCA-API-SECRET-KEY": api_secret
    }

    response = requests.get(url, headers=headers)

    # Check if the response is successful
    if response.status_code == 200:
        # Parse the JSON response
        orders = json.loads(response.text)
        
        # Check if there's at least one order in the response
        if orders:
            # Return the ID of the first (most recent) order
            return orders[0]['id']
        else:
            # No open orders found
            return None
    else:
        # Handle errors (e.g., bad request, authentication error)
        print(f"Failed to fetch orders: {response.text}")
        return None


# Function to delete the most recent order
def delete_most_recent_order():

    # Alpaca API credentials
    api_key= "PKP2V124H0HKOWUB4PJP"
    api_secret = "fS9uDM3vugecsTweCgvuTVGJnXonFMOLmdwIFf7d"
  
    # Fetch the most recent order ID (implement this function based on your earlier code)
    order_id = get_most_recent_order_id(api_key, api_secret)

    if order_id:
        url = f"https://paper-api.alpaca.markets/v2/orders/{order_id}"

        headers = {
            "APCA-API-KEY-ID": api_key,
            "APCA-API-SECRET-KEY": api_secret
        }

        response = requests.delete(url, headers=headers)

        if response.status_code == 200:
            print("Order successfully deleted.")
        else:
            print(f"Failed to delete order: {response.text}")
    else:
        print("No recent order to delete.")


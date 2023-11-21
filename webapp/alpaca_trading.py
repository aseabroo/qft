import requests

# Alpaca API credentials
key_id = "PKP2V124H0HKOWUB4PJP"
secret_key = "fS9uDM3vugecsTweCgvuTVGJnXonFMOLmdwIFf7d"
  
def get_alpaca_account():
    """
    Fetches account information from Alpaca API.
    Returns the JSON response containing account details.
    """
    url = "https://paper-api.alpaca.markets/v2/account"
    headers = {
        "accept": "application/json",
        "APCA-API-KEY-ID": key_id,
        "APCA-API-SECRET-KEY": secret_key
    }

    response = requests.get(url, headers=headers)
    return response.json()

def get_account_portfolio_history():
    """
    Retrieves the account's portfolio history for a specified period and timeframe.
    Returns the parsed JSON data.
    """
    url = "https://paper-api.alpaca.markets/v2/account/portfolio/history"
    params = {
        "period": "1M",
        "timeframe": "1D",
        "date_end": "2023-11-19"
    }
    headers = {
        "accept": "application/json",
        "APCA-API-KEY-ID": key_id,
        "APCA-API-SECRET-KEY": secret_key
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()  # Parse the response JSON data
    return data

# Alpaca API endpoint for placing orders
ORDER_ENDPOINT = "https://paper-api.alpaca.markets/v2/orders"

def create_order(data):
    """
    Creates an order with the given data using the Alpaca API.
    The data parameter should contain details like symbol, qty, side, etc.
    Returns the response from the API call.
    """
    # Define the order parameters
    order_data = {
        "symbol": data["symbol"],
        "qty": data["qty"],
        "side": data["side"],
        "type": data["type"],
        "time_in_force": data["time_in_force"],
        "client_order_id": data.get("client_order_id", None),
        "order_class": data.get("order_class", "")
    }

    # Additional order parameters, added if present in data
    optional_params = ["notional", "limit_price", "stop_price", "trail_price", "trail_percent", "extended_hours"]
    for param in optional_params:
        if param in data:
            order_data[param] = data[param]

    # Set up headers with API key and secret
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "APCA-API-KEY-ID": key_id,
        "APCA-API-SECRET-KEY": secret_key
    }

    # Send the POST request to Alpaca API to create the order
    response = requests.post(ORDER_ENDPOINT, json=order_data, headers=headers)
    return response

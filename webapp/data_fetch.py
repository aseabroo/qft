import requests
import logging

from webapp.url_builder import build_daily_url, build_intraday_url

def get_json_data(symbol, outputsize, apikey, function_interval, intraday_interval=None):
    """
    Fetches JSON data for a given stock symbol based on the specified parameters.
    :param symbol: The stock symbol to fetch data for.
    :param outputsize: Specifies the amount of data to return.
    :param apikey: The API key for authentication.
    :param function_interval: The function interval, either 'intraday' or 'daily'.
    :param intraday_interval: The interval for intraday data (required if function_interval is 'intraday').
    :return: JSON data from the API or None in case of an error or invalid parameters.
    """
    
    # Validate required parameters
    if not symbol or not apikey:
        logging.error("Invalid symbol or API key provided.")
        return None

    try:
        # Build the appropriate URL based on the function interval
        if function_interval == 'intraday':
            # Ensure intraday_interval is provided for intraday data
            if not intraday_interval:
                logging.error("Intraday interval is required for intraday data.")
                return None
            url = build_intraday_url(symbol, apikey, outputsize=outputsize, intraday_interval=intraday_interval, datatype='json')
        elif function_interval == 'daily':
            url = build_daily_url(symbol, apikey, outputsize=outputsize, datatype='json')
        else:
            logging.error("Invalid function_interval specified.")
            return None

        # Make the API request
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            # Log warning if API request is unsuccessful
            logging.warning(f"API request failed with status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        # Log error if there's an exception during the request
        logging.error(f"Error during API request: {e}")
        return None

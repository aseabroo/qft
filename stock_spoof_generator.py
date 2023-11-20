import random
from datetime import datetime, timedelta
import requests
from faker import Faker

# Function to generate random stock data with API parameters
def generate_stock_data(function, symbol, interval=None, adjusted=True, extended_hours=True, month=None, outputsize='compact', datatype='json', apikey=None):
    data = {}

    if function == 'TIME_SERIES_INTRADAY':
        if interval not in ['1min', '5min', '15min', '30min', '60min']:
            return {
                'Error': 'Invalid interval for TIME_SERIES_INTRADAY. Choose from 1min, 5min, 15min, 30min, 60min.'
            }

        data['Meta Data'] = {
            '1. Information': 'Intraday (' + interval + ') open, high, low, close prices and volume',
            '2. Symbol': symbol,
            '3. Last Refreshed': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            '4. Interval': interval,
            '5. Output Size': outputsize,
            '6. Time Zone': 'US/Eastern'
        }
        data['Time Series (1min)'] = {}

        current_time = datetime.now()
        if month:
            current_time = datetime.strptime(month, '%Y-%m') + timedelta(days=1)  # Start from the first day of the specified month

        while True:
            open_price = round(random.uniform(152.0, 154.0), 4)
            high_price = round(open_price + random.uniform(0.1, 1.0), 4)
            low_price = round(open_price - random.uniform(0.1, 1.0), 4)
            close_price = round(random.uniform(low_price, high_price), 4)
            volume = random.randint(1, 100)
            # Define the time series key based on the selected interval
            time_series_key = f'Time Series ({interval})'
            data[time_series_key][current_time.strftime('%Y-%m-%d %H:%M:%S')] = {
                '1. open': str(open_price),
                '2. high': str(high_price),
                '3. low': str(low_price),
                '4. close': str(close_price),
                '5. volume': str(volume)
            }

            current_time -= timedelta(minutes=5)
            if month:
                if current_time.strftime('%Y-%m') != month:
                    break

    elif function == 'TIME_SERIES_DAILY':
        if outputsize not in ['Compact', 'Full']:
            return {
                'Error': 'Invalid outputsize for TIME_SERIES_DAILY. Choose from compact or full.'
            }

        if apikey is None:
            return {
                'Error': 'API key is required for TIME_SERIES_DAILY function.'
            }

        data['Meta Data'] = {
            '1. Information': 'Daily Prices (open, high, low, close) and Volumes',
            '2. Symbol': symbol,
            '3. Last Refreshed': datetime.now().strftime('%Y-%m-%d'),
            '4. Output Size': outputsize
        }
        data['Time Series (Daily)'] = {}

         # Calculate the start date (1 year ago from today)
        current_date = datetime.now() - timedelta(days=30)
        
        # Generate daily data for a random 20+ years period
        # current_date = datetime.now() - timedelta(days=random.randint(20 * 365, 30 * 365))
        while current_date <= datetime.now():
            open_price = round(random.uniform(152.0, 154.0), 4)
            high_price = round(open_price + random.uniform(0.1, 1.0), 4)
            low_price = round(open_price - random.uniform(0.1, 1.0), 4)
            close_price = round(random.uniform(low_price, high_price), 4)
            volume = random.randint(10000, 1000000)

            data['Time Series (Daily)'][current_date.strftime('%Y-%m-%d')] = {
                '1. open': str(open_price),
                '2. high': str(high_price),
                '3. low': str(low_price),
                '4. close': str(close_price),
                '5. volume': str(volume)
            }

            current_date += timedelta(days=1)

    return data

# Example usage for TIME_SERIES_DAILY
function = 'TIME_SERIES_DAILY'
symbol = 'IBM'
outputsize = 'Compact'
datatype = 'json'
apikey = 'L2ASITPZD0FAQIDB'  # Replace with your actual API key

spoofed_data = generate_stock_data(function, symbol, outputsize=outputsize, datatype=datatype, apikey=apikey)

# Print the generated data or handle the error
import json
with open('stock_spoof_data.json', 'w') as json_file:
    json.dump(spoofed_data, json_file, indent=4)

if 'Error' in spoofed_data:
    print(spoofed_data['Error'])
else:
    print(json.dumps(spoofed_data, indent=2))


def build_intraday_url(symbol, apikey, intraday_interval, adjusted=True, extended_hours=True, month=None, outputsize='compact', datatype='json'):
    """
    Constructs a URL for fetching intraday stock data.

    :param symbol: Stock symbol for which the data is requested.
    :param apikey: API key for the data provider.
    :param intraday_interval: Time interval between data points (e.g., '1min').
    :param adjusted: Boolean indicating if adjusted data is required.
    :param extended_hours: Boolean to include extended hours data.
    :param month: Optional month parameter for the query.
    :param outputsize: Determines the number of data points ('compact' or 'full').
    :param datatype: Format of the returned data ('json' or 'csv').
    :return: Constructed URL string for the API request.
    """
    # Base URL for the API
    base_url = 'https://www.alphavantage.co/query'

    # Initial URL with mandatory parameters
    url = f'{base_url}?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={intraday_interval}&apikey={apikey}'

    # Append additional parameters to the URL
    if not adjusted:
        url += '&adjusted=false'
    if not extended_hours:
        url += '&extended_hours=false'
    if month:
        url += f'&month={month}'
    if outputsize:
        url += f'&outputsize={outputsize}'
    if datatype:
        url += f'&datatype={datatype}'

    return url

def build_daily_url(symbol, apikey, outputsize='compact', datatype='json'):
    """
    Constructs a URL for fetching daily stock data.

    :param symbol: Stock symbol for which the data is requested.
    :param apikey: API key for the data provider.
    :param outputsize: Determines the number of data points ('compact' or 'full').
    :param datatype: Format of the returned data ('json' or 'csv').
    :return: Constructed URL string for the API request.
    """
    # Base URL for the API
    base_url = 'https://www.alphavantage.co/query'

    # Initial URL with mandatory parameters
    url = f'{base_url}?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={apikey}'

    # Append optional parameters to the URL
    if outputsize:
        url += f'&outputsize={outputsize}'
    if datatype:
        url += f'&datatype={datatype}'

    return url

# Example usage
# build_daily_url('AAPL', apikey='5CZCCX7WZESVENBF')

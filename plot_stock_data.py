import plotly.graph_objects as go
import pandas as pd
import json
import pytz
from datetime import datetime

def create_interactive_candlestick_with_timezone(json_data, user_timezone):
    """
    Creates an interactive candlestick chart in a specified timezone using data from JSON.
    :param json_data: The JSON data containing stock market information.
    :param user_timezone: The timezone for displaying dates in the chart.
    :return: HTML representation of the candlestick chart.
    """

    # Check for empty or None JSON data
    if json_data is None:
        return "No data available"

    # Extract Meta Data from JSON
    meta_data = json_data.get("Meta Data", {})
    information = meta_data.get("1. Information", "")

    # Determine the appropriate time series key and interval
    if "Daily Prices" in information:
        time_series_key = "Time Series (Daily)"
        interval = "daily"
    elif "Intraday" in information:
        interval = meta_data.get("4. Interval", "1min")
        time_series_key = f"Time Series ({interval})"
    else:
        return "Invalid data format"

    # Extract time series data
    time_series = json_data.get(time_series_key, {})

    # Convert time series data to pandas DataFrame
    df = pd.DataFrame.from_dict(time_series, orient='index')
    df = df.rename(columns={
        "1. open": "Open",
        "2. high": "High",
        "3. low": "Low",
        "4. close": "Close",
        "5. volume": "Volume"
    })
    df.index = pd.to_datetime(df.index)

    # Convert index to the specified timezone
    df.index = df.index.tz_localize('UTC').tz_convert(user_timezone)

    # Create candlestick chart
    fig = go.Figure(data=[go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close']
    )])

    # Formatting and adding metadata for display
    symbol = meta_data.get("2. Symbol", "Unknown Symbol")
    last_refreshed_str = meta_data.get("3. Last Refreshed", "")
    title_text = f"Stock Data for {symbol} (Last Refreshed: {last_refreshed_str})"

    # Update layout with titles and labels
    fig.update_layout(
        title=title_text,
        xaxis_title='Date',
        yaxis_title='Price',
        xaxis_rangeslider_visible=False
    )

    # Format x-axis to display date and time in 12-hour format
    fig.update_xaxes(
        tickformat='%Y-%m-%d %I:%M%p'  # 'YYYY-MM-DD HH:MM AM/PM'
    )

    return fig.to_html(full_html=False)

# Example usage (replace json_data with actual JSON data)
# candlestick_html = create_interactive_candlestick_with_timezone(json_data, 'America/New_York')

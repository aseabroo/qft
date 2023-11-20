from flask import Flask, flash, render_template, request, redirect, url_for
import requests
import json
import time
from data_fetch import get_json_data
from plot_stock_data import create_interactive_candlestick_with_timezone
from url_builder import build_daily_url
import alpaca_trading

app = Flask(__name__)

# API key for stock data
API_KEY = '5CZCCX7WZESVENBF'
CACHE_TIME = 300  # Cache duration of 5 minutes in seconds
cached_data = None
last_fetch_time = 0
symbol = 'IBM'

# Secret key for Flask application
app.secret_key = 'password'

# Route for the home page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Retrieve symbol, output size, and function interval from the form
        symbol = request.form['symbol']
        outputsize = request.form['outputsize']
        function_interval = request.form['function_interval']

        # Optional intraday_interval parameter
        intraday_interval = request.form.get('intraday_interval')

        # Fetch data and generate candlestick chart
        data = get_json_data(symbol, outputsize, API_KEY, function_interval, intraday_interval)
        if data:
            candlestick_html = create_interactive_candlestick_with_timezone(data, 'America/New_York')
            return render_template('index.html', candlestick_html=candlestick_html)

    # Default data for initial page load
    initial_data = get_json_data('IBM', 'compact', API_KEY, 'daily')
    initial_candlestick_html = create_interactive_candlestick_with_timezone(initial_data, 'America/New_York')
    return render_template('index.html', candlestick_html=initial_candlestick_html)

# Route for the trading page
@app.route('/trading', methods=['GET', 'POST'])
def trading():
    if request.method == 'POST':
        # Create an order based on request data
        order_data = {
            "symbol": request.form["symbol"],
            "qty": request.form["qty"],
            "side": request.form["side"],
            "type": request.form["type"],
            "time_in_force": request.form["time_in_force"],
            # Additional order data can be added here
        }

        # Send the order request to Alpaca Trading
        response = alpaca_trading.create_order(order_data)

        # Handle response status codes
        if response.status_code == 200:
            flash("Order created successfully", "success")
        elif response.status_code == 403:
            flash("Forbidden - Buying power or shares are not sufficient", "danger")
        elif response.status_code == 422:
            flash("Unprocessable - Input parameters are not recognized", "danger")
        else:
            flash("An error occurred while creating the order", "danger")
        return redirect(url_for('trading'))

    # Fetch account and portfolio data
    account_data = alpaca_trading.get_alpaca_account()
    portfolio_data = alpaca_trading.get_account_portfolio_history()

    return render_template('trading.html', account_data=account_data, portfolio_data=portfolio_data)

# Main entry point for the application
if __name__ == '__main__':
    app.run(debug=True, port=8000)

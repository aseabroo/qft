# Quantum Flux Trading Documentation

## Introduction
This Flask application provides real-time stock data visualization using candlestick charts. Users can input stock symbols, data types, and time intervals to view interactive candlestick charts.

## API Endpoints

### GET / (Home Page)
- Method: GET
- Description: Display the home page with the default candlestick chart.
- Input Parameters: None
- Output: HTML page with candlestick chart.

### POST / (Update Candlestick Chart)
- Method: POST
- Description: Update the candlestick chart based on user inputs.
- Input Parameters:
  - symbol (string): Stock symbol
  - outputsize (string): Output size (compact or full)
  - datatype (string): Data type (json or csv)
  - function_interval (string, optional): Intraday interval (1min, 5min, 15min, 30min, 60min)
- Output: HTML page with updated candlestick chart.

## Request and Response Examples

### POST / (Update Candlestick Chart)
**Request:**
```json
{
  "symbol": "AAPL",
  "outputsize": "compact",
  "datatype": "json",
  "function_interval": "15min"
}

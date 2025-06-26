import requests
import os
from dotenv import load_dotenv

load_dotenv()
BASE_URL = "https://www.alphavantage.co/query"
API_KEY = os.getenv('AV_KEY')
if not API_KEY:
    raise ValueError("API key for Alpha Vantage is not set. Please set the AV_KEY environment variable.")

def _make_request(params):
    params['apikey'] = API_KEY
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    return response.json()

def get_intraday_data(symbol:str, interval:str="1min", output_size:str="compact"):
    """
    Fetch intraday stock data.
    :param symbol: Stock symbol (e.g., 'AAPL').
    :param interval: Time interval between data points (e.g., '1min', '5min').
    :param output_size: 'compact' or 'full'.
    :return: JSON response.
    """
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": symbol,
        "interval": interval,
        "outputsize": output_size
    }
    return _make_request(params)

def get_daily_data(symbol:str, output_size:str="compact"):
    """
    Fetch daily stock data.
    :param symbol: Stock symbol (e.g., 'AAPL').
    :param output_size: 'compact' or 'full'.
    :return: JSON response.
    """
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "outputsize": output_size
    }
    return _make_request(params)

def get_weekly_data(symbol:str):
    """
    Fetch weekly stock data.
    :param symbol: Stock symbol (e.g., 'AAPL').
    :return: JSON response.
    """
    params = {
        "function": "TIME_SERIES_WEEKLY",
        "symbol": symbol
    }
    return _make_request(params)

def get_monthly_data(symbol:str):
    """
    Fetch monthly stock data.
    :param symbol: Stock symbol (e.g., 'AAPL').
    :return: JSON response.
    """
    params = {
        "function": "TIME_SERIES_MONTHLY",
        "symbol": symbol
    }
    return _make_request(params)

def get_quote(symbol:str):
    """
    Fetch real-time stock quote.
    :param symbol: Stock symbol (e.g., 'AAPL').
    :return: JSON response.
    """
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": symbol
    }
    return _make_request(params)

def search_symbol(keywords:str):
    """
    Search for stock symbols based on keywords.
    :param keywords: Search keywords (e.g., 'Microsoft').
    :return: JSON response.
    """
    params = {
        "function": "SYMBOL_SEARCH",
        "keywords": keywords
    }
    return _make_request(params)
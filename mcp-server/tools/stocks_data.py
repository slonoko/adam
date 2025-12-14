import requests
import os
import csv
import io
from fastmcp import FastMCP
from dotenv import load_dotenv
from typing import Optional
import requests

load_dotenv()
BASE_URL = "https://www.alphavantage.co/query"
API_KEY = os.getenv("ALPHAVANTAGE_KEY")
if not API_KEY:
    raise ValueError(
        "API key for Alpha Vantage is not set. Please set the ALPHAVANTAGE_KEY environment variable."
    )


def _make_request(params):
    params["apikey"] = API_KEY
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    return response.json()

mcp = FastMCP("stockwhisperer")   

@mcp.tool()
def get_all_tickers_in_exchange(exchanges: set[str])-> list[str]:
    """
    Get a list with all the symbols filtered by a given exchange.
    
    Valid exchanges: {'AMEX', 'OTC', 'NYSE', 'NASDAQ'}
    
    :param exchanges: a set which contains the exchanges you want to keep (all the rest will be ignored)
    :return: list of symbols
    """

    exchanges = {x.upper() for x in exchanges}
    r = requests.get('https://scanner.tradingview.com/america/scan')
    data = r.json()['data']  # [{'s': 'NYSE:HKD', 'd': []}, {'s': 'NASDAQ:ALTY', 'd': []}...]
    
    symbols = []
    for dct in data:
        exchange, symbol = dct['s'].split(':')
        if exchange in exchanges:
            symbols.append(symbol)
    return symbols

@mcp.tool()
def get_intraday_data(
    symbol: str, interval: str = "1min", output_size: str = "compact"
):
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
        "outputsize": output_size,
    }
    return _make_request(params)

@mcp.tool()
def get_all_daily_historical_data(symbol: str, output_size: str = "compact"):
    """
    Returns raw (as-traded) daily time series (date, daily open, daily high, daily low, daily close, daily volume) of the global equity specified, covering 20+ years of historical data. The OHLCV data is sometimes called "candles" in finance literature.
    :param symbol: Stock symbol (e.g., 'AAPL').
    :param output_size: 'compact' or 'full'.
    :return: JSON response.
    """
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "outputsize": output_size,
    }
    return _make_request(params)

@mcp.tool()
def get_specific_date_historical_data(symbol: str, date: str):
    """
    Returns raw (as-traded) daily time series (date, daily open, daily high, daily low, daily close, daily volume) of the global equity specified, for a specific date.
    :param symbol: Stock symbol (e.g., 'AAPL').
    :param date: Date in YYYY-MM-DD format. example: 2025-10-31
    :return: JSON response.
    """
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "outputsize": "full",
    }
    data = _make_request(params)

    time_series = data.get("Time Series (Daily)", {})
    historical_data = time_series.get(date, {})

    return {date: historical_data} if historical_data else {date: {}}


@mcp.tool()
def get_weekly_data(symbol: str):
    """
    Fetch weekly stock data.
    :param symbol: Stock symbol (e.g., 'AAPL').
    :return: JSON response.
    """
    params = {"function": "TIME_SERIES_WEEKLY", "symbol": symbol}
    return _make_request(params)

@mcp.tool()
def get_monthly_data(symbol: str):
    """
    Fetch monthly stock data.
    :param symbol: Stock symbol (e.g., 'AAPL').
    :return: JSON response.
    """
    params = {"function": "TIME_SERIES_MONTHLY", "symbol": symbol}
    return _make_request(params)

@mcp.tool()
def get_quote(symbol: str):
    """
    Fetch real-time stock quote.
    :param symbol: Stock symbol (e.g., 'AAPL').
    :return: JSON response.
    """
    params = {"function": "GLOBAL_QUOTE", "symbol": symbol}
    return _make_request(params)

@mcp.tool()
def search_symbol(keywords: str):
    """
    Search for stock symbols based on keywords.
    :param keywords: Search keywords (e.g., 'Microsoft').
    :return: JSON response.
    """
    params = {"function": "SYMBOL_SEARCH", "keywords": keywords}
    return _make_request(params)

@mcp.tool()
def symbol_search(keywords: str):
    """
    Search for best-matching symbols and market information based on keywords.
    :param keywords: Search keywords (e.g., 'Microsoft').
    :return: JSON response.
    """
    params = {
        "function": "SYMBOL_SEARCH",
        "keywords": keywords,
        "datatype": "json"
    }
    return _make_request(params)

@mcp.tool()
def market_status():
    """
    Global Market Open & Close Status Utility

    This endpoint returns the current market status (open vs. closed) of major trading venues for equities, forex, and cryptocurrencies around the world.
    :return: JSON response.
    """
    params = {
        "function": "MARKET_STATUS"
    }
    return _make_request(params)

@mcp.tool()
def earning_call_transcript(symbol: str, quarter: str):
    """
    Earnings Call Transcript Trending

    This API returns the earnings call transcript for a given company in a specific quarter, covering over 15 years of history and enriched with LLM-based sentiment signals.
    :param symbol: The ticker symbol (e.g., 'IBM').
    :param quarter: Fiscal quarter in YYYYQM format (e.g., '2024Q1').
    :return: JSON response.
    """
    params = {
        "function": "EARNINGS_CALL_TRANSCRIPT",
        "symbol": symbol,
        "quarter": quarter
    }
    return _make_request(params)

@mcp.tool()
def top_gainers_losers():
    """
    Top Gainers, Losers, and Most Actively Traded Tickers (US Market)

    This endpoint returns the top 20 gainers, losers, and the most active traded tickers in the US market.
    :return: JSON response.
    """
    params = {
        "function": "TOP_GAINERS_LOSERS"
    }
    return _make_request(params)

@mcp.tool()
def analytics_fixed_window(
    symbols: str,
    interval: str,
    calculations: str,
    range1: str,
    range2: Optional[str] = None,
    ohlc: str = "close"
):
    """
    Advanced Analytics (Fixed Window)

    This endpoint returns a rich set of advanced analytics metrics (e.g., total return, variance, auto-correlation, etc.) for a given time series over a fixed temporal window.
    :param symbols: Comma separated list of symbols (e.g., 'AAPL,MSFT,IBM').
    :param interval: Time interval between data points (e.g., 'DAILY', '1min').
    :param calculations: Comma separated list of analytics metrics (e.g., 'MEAN,STDDEV,CORRELATION').
    :param range1: Start date or range (e.g., '2023-07-01').
    :param range2: End date or range (optional, e.g., '2023-08-31').
    :param ohlc: OHLC field to use (default 'close').
    :return: JSON response.
    """
    params = {
        "function": "ANALYTICS_FIXED_WINDOW",
        "SYMBOLS": symbols,
        "INTERVAL": interval,
        "CALCULATIONS": calculations,
        "OHLC": ohlc
    }
    # Add RANGE parameters as separate entries if range2 is provided
    if range2:
        # requests will encode multiple identical keys as needed
        params_list = [
            ("function", "ANALYTICS_FIXED_WINDOW"),
            ("SYMBOLS", symbols),
            ("INTERVAL", interval),
            ("CALCULATIONS", calculations),
            ("OHLC", ohlc),
            ("RANGE", range1),
            ("RANGE", range2)
        ]
        return _make_request(dict(params_list))
    else:
        params["RANGE"] = range1
        return _make_request(params)

@mcp.tool()
def company_overview(symbol: str):
    """
    Company Overview

    This API returns the company information, financial ratios, and other key metrics for the equity specified.
    :param symbol: The ticker symbol (e.g., 'IBM').
    :return: JSON response.
    """
    params = {
        "function": "OVERVIEW",
        "symbol": symbol
    }
    return _make_request(params)

@mcp.tool()
def etf_profile(symbol: str):
    """
    ETF Profile & Holdings

    This API returns key ETF metrics (e.g., net assets, expense ratio, and turnover), along with the corresponding ETF holdings / constituents with allocation by asset types and sectors.
    :param symbol: The ticker symbol (e.g., 'QQQ').
    :return: JSON response.
    """
    params = {
        "function": "ETF_PROFILE",
        "symbol": symbol
    }
    return _make_request(params)

@mcp.tool()
def dividends(symbol: str):
    """
    Corporate Action - Dividends Trending

    This API returns historical and future (declared) dividend distributions.
    :param symbol: The ticker symbol (e.g., 'IBM').
    :return: JSON response.
    """
    params = {
        "function": "DIVIDENDS",
        "symbol": symbol
    }
    return _make_request(params)

@mcp.tool()
def splits(symbol: str):
    """
    Corporate Action - Splits

    This API returns historical split events.
    :param symbol: The ticker symbol (e.g., 'IBM').
    :return: JSON response.
    """
    params = {
        "function": "SPLITS",
        "symbol": symbol
    }
    return _make_request(params)

@mcp.tool()
def income_statement(symbol: str):
    """
    Income Statement

    This API returns the annual and quarterly income statements for the company of interest, with normalized fields mapped to GAAP and IFRS taxonomies of the SEC.
    :param symbol: The ticker symbol (e.g., 'IBM').
    :return: JSON response.
    """
    params = {
        "function": "INCOME_STATEMENT",
        "symbol": symbol
    }
    return _make_request(params)

@mcp.tool()
def balance_sheet(symbol: str):
    """
    Balance Sheet

    This API returns the annual and quarterly balance sheets for the company of interest, with normalized fields mapped to GAAP and IFRS taxonomies of the SEC.
    :param symbol: The ticker symbol (e.g., 'IBM').
    :return: JSON response.
    """
    params = {
        "function": "BALANCE_SHEET",
        "symbol": symbol
    }
    return _make_request(params)

@mcp.tool()
def cash_flow(symbol: str):
    """
    Cash Flow

    This API returns the annual and quarterly cash flow for the company of interest, with normalized fields mapped to GAAP and IFRS taxonomies of the SEC.
    :param symbol: The ticker symbol (e.g., 'IBM').
    :return: JSON response.
    """
    params = {
        "function": "CASH_FLOW",
        "symbol": symbol
    }
    return _make_request(params)

@mcp.tool()
def earnings(symbol: str):
    """
    Earnings

    This API returns the annual and quarterly earnings (EPS) for the company of interest. Quarterly data also includes analyst estimates and surprise metrics.
    :param symbol: The ticker symbol (e.g., 'IBM').
    :return: JSON response.
    """
    params = {
        "function": "EARNINGS",
        "symbol": symbol
    }
    return _make_request(params)

@mcp.tool()
def earnings_calendar(symbol: Optional[str] = None, horizon: str = "3month"):
    """
    Earnings Calendar

    This API returns a list of company earnings expected in the next 3, 6, or 12 months.
    :param symbol: The ticker symbol (optional, e.g., 'IBM'). If not provided, returns all scheduled earnings.
    :param horizon: Time horizon ('3month', '6month', or '12month'). Defaults to '3month'.
    :return: JSON response with earnings calendar data.
    """
    if not API_KEY:
        raise ValueError("API key for Alpha Vantage is not set.")
        
    params = {
        "function": "EARNINGS_CALENDAR",
        "horizon": horizon,
        "datatype": "csv",  # Request CSV format to get the structured data
        "apikey": API_KEY
    }
    if symbol:
        params["symbol"] = symbol
    
    # Make request and handle CSV response
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    
    # Parse CSV data and convert to JSON
    csv_data = response.text
    csv_reader = csv.DictReader(io.StringIO(csv_data))
    
    # Convert CSV rows to list of dictionaries
    earnings_data = []
    for row in csv_reader:
        earnings_data.append(dict(row))
    
    return {
        "earnings_calendar": earnings_data,
        "total_count": len(earnings_data)
    }

@mcp.tool()
def ipo_calendar():
    """
    IPO Calendar

    This API returns a list of IPOs expected in the next 3 months.
    :return: JSON response.
    """
    params = {
        "function": "IPO_CALENDAR"
    }
    return _make_request(params)

# Technical Indicators - Moving Averages
@mcp.tool()
def sma(symbol: str, interval: str, time_period: int, series_type: str, month: Optional[str] = None):
    """
    Simple Moving Average (SMA)
    
    This API returns the simple moving average (SMA) values.
    :param symbol: The ticker symbol (e.g., 'IBM').
    :param interval: Time interval ('1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly').
    :param time_period: Number of data points used to calculate each moving average value.
    :param series_type: The desired price type ('close', 'open', 'high', 'low').
    :param month: Optional month in YYYY-MM format for intraday intervals.
    :return: JSON response.
    """
    params = {
        "function": "SMA",
        "symbol": symbol,
        "interval": interval,
        "time_period": time_period,
        "series_type": series_type
    }
    if month:
        params["month"] = month
    return _make_request(params)

@mcp.tool()
def ema(symbol: str, interval: str, time_period: int, series_type: str, month: Optional[str] = None):
    """
    Exponential Moving Average (EMA)
    
    This API returns the exponential moving average (EMA) values.
    :param symbol: The ticker symbol (e.g., 'IBM').
    :param interval: Time interval ('1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly').
    :param time_period: Number of data points used to calculate each moving average value.
    :param series_type: The desired price type ('close', 'open', 'high', 'low').
    :param month: Optional month in YYYY-MM format for intraday intervals.
    :return: JSON response.
    """
    params = {
        "function": "EMA",
        "symbol": symbol,
        "interval": interval,
        "time_period": time_period,
        "series_type": series_type
    }
    if month:
        params["month"] = month
    return _make_request(params)

@mcp.tool()
def wma(symbol: str, interval: str, time_period: int, series_type: str, month: Optional[str] = None):
    """
    Weighted Moving Average (WMA)
    
    This API returns the weighted moving average (WMA) values.
    :param symbol: The ticker symbol (e.g., 'IBM').
    :param interval: Time interval ('1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly').
    :param time_period: Number of data points used to calculate each moving average value.
    :param series_type: The desired price type ('close', 'open', 'high', 'low').
    :param month: Optional month in YYYY-MM format for intraday intervals.
    :return: JSON response.
    """
    params = {
        "function": "WMA",
        "symbol": symbol,
        "interval": interval,
        "time_period": time_period,
        "series_type": series_type
    }
    if month:
        params["month"] = month
    return _make_request(params)

@mcp.tool()
def dema(symbol: str, interval: str, time_period: int, series_type: str, month: Optional[str] = None):
    """
    Double Exponential Moving Average (DEMA)
    
    This API returns the double exponential moving average (DEMA) values.
    :param symbol: The ticker symbol (e.g., 'IBM').
    :param interval: Time interval ('1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly').
    :param time_period: Number of data points used to calculate each moving average value.
    :param series_type: The desired price type ('close', 'open', 'high', 'low').
    :param month: Optional month in YYYY-MM format for intraday intervals.
    :return: JSON response.
    """
    params = {
        "function": "DEMA",
        "symbol": symbol,
        "interval": interval,
        "time_period": time_period,
        "series_type": series_type
    }
    if month:
        params["month"] = month
    return _make_request(params)

@mcp.tool()
def tema(symbol: str, interval: str, time_period: int, series_type: str, month: Optional[str] = None):
    """
    Triple Exponential Moving Average (TEMA)
    
    This API returns the triple exponential moving average (TEMA) values.
    :param symbol: The ticker symbol (e.g., 'IBM').
    :param interval: Time interval ('1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly').
    :param time_period: Number of data points used to calculate each moving average value.
    :param series_type: The desired price type ('close', 'open', 'high', 'low').
    :param month: Optional month in YYYY-MM format for intraday intervals.
    :return: JSON response.
    """
    params = {
        "function": "TEMA",
        "symbol": symbol,
        "interval": interval,
        "time_period": time_period,
        "series_type": series_type
    }
    if month:
        params["month"] = month
    return _make_request(params)

@mcp.tool()
def trima(symbol: str, interval: str, time_period: int, series_type: str, month: Optional[str] = None):
    """
    Triangular Moving Average (TRIMA)
    
    This API returns the triangular moving average (TRIMA) values.
    :param symbol: The ticker symbol (e.g., 'IBM').
    :param interval: Time interval ('1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly').
    :param time_period: Number of data points used to calculate each moving average value.
    :param series_type: The desired price type ('close', 'open', 'high', 'low').
    :param month: Optional month in YYYY-MM format for intraday intervals.
    :return: JSON response.
    """
    params = {
        "function": "TRIMA",
        "symbol": symbol,
        "interval": interval,
        "time_period": time_period,
        "series_type": series_type
    }
    if month:
        params["month"] = month
    return _make_request(params)

@mcp.tool()
def kama(symbol: str, interval: str, time_period: int, series_type: str, month: Optional[str] = None):
    """
    Kaufman Adaptive Moving Average (KAMA)
    
    This API returns the Kaufman adaptive moving average (KAMA) values.
    :param symbol: The ticker symbol (e.g., 'IBM').
    :param interval: Time interval ('1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly').
    :param time_period: Number of data points used to calculate each moving average value.
    :param series_type: The desired price type ('close', 'open', 'high', 'low').
    :param month: Optional month in YYYY-MM format for intraday intervals.
    :return: JSON response.
    """
    params = {
        "function": "KAMA",
        "symbol": symbol,
        "interval": interval,
        "time_period": time_period,
        "series_type": series_type
    }
    if month:
        params["month"] = month
    return _make_request(params)

@mcp.tool()
def mama(symbol: str, interval: str, series_type: str, fastlimit: float = 0.01, slowlimit: float = 0.01, month: Optional[str] = None):
    """
    MESA Adaptive Moving Average (MAMA)
    
    This API returns the MESA adaptive moving average (MAMA) values.
    :param symbol: The ticker symbol (e.g., 'IBM').
    :param interval: Time interval ('1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly').
    :param series_type: The desired price type ('close', 'open', 'high', 'low').
    :param month: Optional month in YYYY-MM format for intraday intervals.
    :param fastlimit: Fast limit parameter. Default is 0.01.
    :param slowlimit: Slow limit parameter. Default is 0.01.
    :return: JSON response.
    """
    params = {
        "function": "MAMA",
        "symbol": symbol,
        "interval": interval,
        "series_type": series_type,
        "fastlimit": fastlimit,
        "slowlimit": slowlimit
    }
    if month:
        params["month"] = month
    return _make_request(params)

@mcp.tool()
def vwap(symbol: str, interval: str, month: Optional[str] = None):
    """
    Volume Weighted Average Price (VWAP) - Premium

    This API returns the volume weighted average price (VWAP) for intraday time series.
    :param symbol: The ticker symbol (e.g., 'IBM').
    :param interval: Intraday interval ('1min', '5min', '15min', '30min', '60min').
    :param month: Optional month in YYYY-MM format for specific month.
    :return: JSON response.
    """
    params = {
        "function": "VWAP",
        "symbol": symbol,
        "interval": interval
    }
    if month:
        params["month"] = month
    return _make_request(params)

@mcp.tool()
def t3(symbol: str, interval: str, time_period: int, series_type: str, month: Optional[str] = None):
    """
    Triple Exponential Moving Average (T3)

    This API returns the triple exponential moving average (T3) values.
    :param symbol: The ticker symbol (e.g., 'IBM').
    :param interval: Time interval ('1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly').
    :param time_period: Number of data points used to calculate each moving average value.
    :param series_type: The desired price type ('close', 'open', 'high', 'low').
    :param month: Optional month in YYYY-MM format for intraday intervals.
    :return: JSON response.
    """
    params = {
        "function": "T3",
        "symbol": symbol,
        "interval": interval,
        "time_period": time_period,
        "series_type": series_type
    }
    if month:
        params["month"] = month
    return _make_request(params)

# Technical Indicators - Momentum & Oscillators
@mcp.tool()
def macd(symbol: str, interval: str, series_type: str, fastperiod: int = 12, slowperiod: int = 26, signalperiod: int = 9, month: Optional[str] = None):
    """
    Moving Average Convergence / Divergence (MACD)
    
    This API returns the moving average convergence / divergence (MACD) values.
    :param symbol: The ticker symbol (e.g., 'IBM').
    :param interval: Time interval ('1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly').
    :param series_type: The desired price type ('close', 'open', 'high', 'low').
    :param fastperiod: Fast period (default 12).
    :param slowperiod: Slow period (default 26).
    :param signalperiod: Signal period (default 9).
    :param month: Optional month in YYYY-MM format for intraday intervals.
    :return: JSON response.
    """
    params = {
        "function": "MACD",
        "symbol": symbol,
        "interval": interval,
        "series_type": series_type,
        "fastperiod": fastperiod,
        "slowperiod": slowperiod,
        "signalperiod": signalperiod
    }
    if month:
        params["month"] = month
    return _make_request(params)

@mcp.tool()
def macdext(symbol: str, interval: str, series_type: str, fastperiod: int = 12, slowperiod: int = 26, signalperiod: int = 9, fastmatype: int = 0, slowmatype: int = 0, signalmatype: int = 0, month: Optional[str] = None):
    """
    MACD with Controllable MA Type (MACDEXT)

    This API returns the MACD values with controllable moving average type.
    :param symbol: The ticker symbol (e.g., 'IBM').
    :param interval: Time interval ('1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly').
    :param series_type: The desired price type ('close', 'open', 'high', 'low').
    :param month: Optional month in YYYY-MM format for intraday intervals.
    :param fastperiod: Fast period parameter. Default is 12.
    :param slowperiod: Slow period parameter. Default is 26.
    :param signalperiod: Signal period parameter. Default is 9.
    :param fastmatype: Fast MA type (0=SMA, 1=EMA, 2=WMA, 3=DEMA, 4=TEMA, 5=TRIMA, 6=KAMA, 7=MAMA, 8=T3). Default is 0.
    :param slowmatype: Slow MA type. Default is 0.
    :param signalmatype: Signal MA type. Default is 0.
    :return: JSON response.
    """
    params = {
        "function": "MACDEXT",
        "symbol": symbol,
        "interval": interval,
        "series_type": series_type,
        "fastperiod": fastperiod,
        "slowperiod": slowperiod,
        "signalperiod": signalperiod,
        "fastmatype": fastmatype,
        "slowmatype": slowmatype,
        "signalmatype": signalmatype
    }
    if month:
        params["month"] = month
    return _make_request(params)

@mcp.tool()
def stoch(symbol: str, interval: str, month: Optional[str] = None, fastkperiod: int = 5, slowkperiod: int = 3, slowdperiod: int = 3, slowkmatype: int = 0, slowdmatype: int = 0):
    """
    Stochastic Oscillator (STOCH)

    This API returns the stochastic oscillator values.
    :param symbol: The ticker symbol (e.g., 'IBM').
    :param interval: Time interval ('1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly').
    :param month: Optional month in YYYY-MM format for intraday intervals.
    :param fastkperiod: Fast K period. Default is 5.
    :param slowkperiod: Slow K period. Default is 3.
    :param slowdperiod: Slow D period. Default is 3.
    :param slowkmatype: Slow K MA type (0=SMA, 1=EMA, 2=WMA, etc.). Default is 0.
    :param slowdmatype: Slow D MA type. Default is 0.
    :return: JSON response.
    """
    params = {
        "function": "STOCH",
        "symbol": symbol,
        "interval": interval,
        "fastkperiod": fastkperiod,
        "slowkperiod": slowkperiod,
        "slowdperiod": slowdperiod,
        "slowkmatype": slowkmatype,
        "slowdmatype": slowdmatype
    }
    if month:
        params["month"] = month
    return _make_request(params)

@mcp.tool()
def stochf(symbol: str, interval: str, month: Optional[str] = None, fastkperiod: int = 5, fastdperiod: int = 3, fastdmatype: int = 0):
    """
    Stochastic Fast (STOCHF)

    This API returns the stochastic fast values.
    :param symbol: The ticker symbol (e.g., 'IBM').
    :param interval: Time interval ('1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly').
    :param month: Optional month in YYYY-MM format for intraday intervals.
    :param fastkperiod: Fast K period. Default is 5.
    :param fastdperiod: Fast D period. Default is 3.
    :param fastdmatype: Fast D MA type (0=SMA, 1=EMA, 2=WMA, etc.). Default is 0.
    :return: JSON response.
    """
    params = {
        "function": "STOCHF",
        "symbol": symbol,
        "interval": interval,
        "fastkperiod": fastkperiod,
        "fastdperiod": fastdperiod,
        "fastdmatype": fastdmatype
    }
    if month:
        params["month"] = month
    return _make_request(params)

@mcp.tool()
def rsi(symbol: str, interval: str, time_period: int, series_type: str, month: Optional[str] = None):
    """
    Relative Strength Index (RSI)
    
    This API returns the relative strength index (RSI) values.
    :param symbol: The ticker symbol (e.g., 'IBM').
    :param interval: Time interval ('1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly').
    :param time_period: Number of data points used to calculate each RSI value.
    :param series_type: The desired price type ('close', 'open', 'high', 'low').
    :param month: Optional month in YYYY-MM format for intraday intervals.
    :return: JSON response.
    """
    params = {
        "function": "RSI",
        "symbol": symbol,
        "interval": interval,
        "time_period": time_period,
        "series_type": series_type
    }
    if month:
        params["month"] = month
    return _make_request(params)

@mcp.tool()
def stochrsi(symbol: str, interval: str, time_period: int, series_type: str, month: Optional[str] = None, fastkperiod: int = 5, fastdperiod: int = 3, fastdmatype: int = 0):
    """
    Stochastic Relative Strength Index (STOCHRSI)

    This API returns the stochastic relative strength index (STOCHRSI) values.
    :param symbol: The ticker symbol (e.g., 'IBM').
    :param interval: Time interval ('1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly').
    :param time_period: Number of data points used to calculate each STOCHRSI value.
    :param series_type: The desired price type ('close', 'open', 'high', 'low').
    :param month: Optional month in YYYY-MM format for intraday intervals.
    :param fastkperiod: Fast K period. Default is 5.
    :param fastdperiod: Fast D period. Default is 3.
    :param fastdmatype: Fast D MA type (0=SMA, 1=EMA, 2=WMA, etc.). Default is 0.
    :return: JSON response.
    """
    params = {
        "function": "STOCHRSI",
        "symbol": symbol,
        "interval": interval,
        "time_period": time_period,
        "series_type": series_type,
        "fastkperiod": fastkperiod,
        "fastdperiod": fastdperiod,
        "fastdmatype": fastdmatype
    }
    if month:
        params["month"] = month
    return _make_request(params)

@mcp.tool()
def get_sma(
    symbol: str,
    interval: str,
    time_period: int,
    series_type: str,
    month: Optional[str] = None,
    datatype: str = "json"
):
    """
    Simple Moving Average (SMA)

    This API returns the simple moving average (SMA) values.
    :param symbol: The ticker symbol (e.g., 'IBM').
    :param interval: Time interval ('1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly').
    :param time_period: Number of data points used to calculate each moving average value.
    :param series_type: The desired price type ('close', 'open', 'high', 'low').
    :param month: Optional month in YYYY-MM format for intraday intervals.
    :param datatype: Output format ('json' or 'csv'). Default is 'json'.
    :return: JSON response.
    """
    params = {
        "function": "SMA",
        "symbol": symbol,
        "interval": interval,
        "time_period": time_period,
        "series_type": series_type,
        "datatype": datatype
    }
    if month:
        params["month"] = month
    return _make_request(params)

@mcp.tool()
def get_ema(
    symbol: str,
    interval: str,
    time_period: int,
    series_type: str,
    month: Optional[str] = None,
    datatype: str = "json"
):
    """
    Exponential Moving Average (EMA)

    This API returns the exponential moving average (EMA) values.
    :param symbol: The ticker symbol (e.g., 'IBM').
    :param interval: Time interval ('1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly').
    :param time_period: Number of data points used to calculate each moving average value.
    :param series_type: The desired price type ('close', 'open', 'high', 'low').
    :param month: Optional month in YYYY-MM format for intraday intervals.
    :param datatype: Output format ('json' or 'csv'). Default is 'json'.
    :return: JSON response.
    """
    params = {
        "function": "EMA",
        "symbol": symbol,
        "interval": interval,
        "time_period": time_period,
        "series_type": series_type,
        "datatype": datatype
    }
    if month:
        params["month"] = month
    return _make_request(params)

@mcp.tool()
def get_wma(
    symbol: str,
    interval: str,
    time_period: int,
    series_type: str,
    month: Optional[str] = None,
    datatype: str = "json"
):
    """
    Weighted Moving Average (WMA)

    This API returns the weighted moving average (WMA) values.
    :param symbol: The ticker symbol (e.g., 'IBM').
    :param interval: Time interval ('1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly').
    :param time_period: Number of data points used to calculate each moving average value.
    :param series_type: The desired price type ('close', 'open', 'high', 'low').
    :param month: Optional month in YYYY-MM format for intraday intervals.
    :param datatype: Output format ('json' or 'csv'). Default is 'json'.
    :return: JSON response.
    """
    params = {
        "function": "WMA",
        "symbol": symbol,
        "interval": interval,
        "time_period": time_period,
        "series_type": series_type,
        "datatype": datatype
    }
    if month:
        params["month"] = month
    return _make_request(params)

@mcp.tool()
def get_dema(
    symbol: str,
    interval: str,
    time_period: int,
    series_type: str,
    month: Optional[str] = None,
    datatype: str = "json"
):
    """
    Double Exponential Moving Average (DEMA)

    This API returns the double exponential moving average (DEMA) values.
    :param symbol: The ticker symbol (e.g., 'IBM').
    :param interval: Time interval ('1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly').
    :param time_period: Number of data points used to calculate each moving average value.
    :param series_type: The desired price type ('close', 'open', 'high', 'low').
    :param month: Optional month in YYYY-MM format for intraday intervals.
    :param datatype: Output format ('json' or 'csv'). Default is 'json'.
    :return: JSON response.
    """
    params = {
        "function": "DEMA",
        "symbol": symbol,
        "interval": interval,
        "time_period": time_period,
        "series_type": series_type,
        "datatype": datatype
    }
    if month:
        params["month"] = month
    return _make_request(params)

@mcp.tool()
def get_tema(
    symbol: str,
    interval: str,
    time_period: int,
    series_type: str,
    month: Optional[str] = None,
    datatype: str = "json"
):
    """
    Triple Exponential Moving Average (TEMA)

    This API returns the triple exponential moving average (TEMA) values.
    :param symbol: The ticker symbol (e.g., 'IBM').
    :param interval: Time interval ('1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly').
    :param time_period: Number of data points used to calculate each moving average value.
    :param series_type: The desired price type ('close', 'open', 'high', 'low').
    :param month: Optional month in YYYY-MM format for intraday intervals.
    :param datatype: Output format ('json' or 'csv'). Default is 'json'.
    :return: JSON response.
    """
    params = {
        "function": "TEMA",
        "symbol": symbol,
        "interval": interval,
        "time_period": time_period,
        "series_type": series_type,
        "datatype": datatype
    }
    if month:
        params["month"] = month
    return _make_request(params)

@mcp.tool()
def get_trima(
    symbol: str,
    interval: str,
    time_period: int,
    series_type: str,
    month: Optional[str] = None,
    datatype: str = "json"
):
    """
    Triangular Moving Average (TRIMA)

    This API returns the triangular moving average (TRIMA) values.
    :param symbol: The ticker symbol (e.g., 'IBM').
    :param interval: Time interval ('1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly').
    :param time_period: Number of data points used to calculate each moving average value.
    :param series_type: The desired price type ('close', 'open', 'high', 'low').
    :param month: Optional month in YYYY-MM format for intraday intervals.
    :param datatype: Output format ('json' or 'csv'). Default is 'json'.
    :return: JSON response.
    """
    params = {
        "function": "TRIMA",
        "symbol": symbol,
        "interval": interval,
        "time_period": time_period,
        "series_type": series_type,
        "datatype": datatype
    }
    if month:
        params["month"] = month
    return _make_request(params)

@mcp.tool()
def get_kama(
    symbol: str,
    interval: str,
    time_period: int,
    series_type: str,
    month: Optional[str] = None,
    datatype: str = "json"
):
    """
    Kaufman Adaptive Moving Average (KAMA)

    This API returns the Kaufman adaptive moving average (KAMA) values.
    :param symbol: The ticker symbol (e.g., 'IBM').
    :param interval: Time interval ('1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly').
    :param time_period: Number of data points used to calculate each moving average value.
    :param series_type: The desired price type ('close', 'open', 'high', 'low').
    :param month: Optional month in YYYY-MM format for intraday intervals.
    :param datatype: Output format ('json' or 'csv'). Default is 'json'.
    :return: JSON response.
    """
    params = {
        "function": "KAMA",
        "symbol": symbol,
        "interval": interval,
        "time_period": time_period,
        "series_type": series_type,
        "datatype": datatype
    }
    if month:
        params["month"] = month
    return _make_request(params)

@mcp.tool()
def get_mama(
    symbol: str,
    interval: str,
    series_type: str,
    month: Optional[str] = None,
    fastlimit: float = 0.01,
    slowlimit: float = 0.01,
    datatype: str = "json"
):
    """
    MESA Adaptive Moving Average (MAMA)

    This API returns the MESA adaptive moving average (MAMA) values.
    :param symbol: The ticker symbol (e.g., 'IBM').
    :param interval: Time interval ('1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly').
    :param series_type: The desired price type ('close', 'open', 'high', 'low').
    :param month: Optional month in YYYY-MM format for intraday intervals.
    :param fastlimit: Fast limit parameter. Default is 0.01.
    :param slowlimit: Slow limit parameter. Default is 0.01.
    :param datatype: Output format ('json' or 'csv'). Default is 'json'.
    :return: JSON response.
    """
    params = {
        "function": "MAMA",
        "symbol": symbol,
        "interval": interval,
        "series_type": series_type,
        "fastlimit": fastlimit,
        "slowlimit": slowlimit,
        "datatype": datatype
    }
    if month:
        params["month"] = month
    return _make_request(params)

@mcp.tool()
def get_vwap(
    symbol: str,
    interval: str,
    month: Optional[str] = None,
    datatype: str = "json"
):
    """
    Volume Weighted Average Price (VWAP) - Premium

    This API returns the volume weighted average price (VWAP) for intraday time series.
    :param symbol: The ticker symbol (e.g., 'IBM').
    :param interval: Intraday interval ('1min', '5min', '15min', '30min', '60min').
    :param month: Optional month in YYYY-MM format for specific month.
    :param datatype: Output format ('json' or 'csv'). Default is 'json'.
    :return: JSON response.
    """
    params = {
        "function": "VWAP",
        "symbol": symbol,
        "interval": interval,
        "datatype": datatype
    }
    if month:
        params["month"] = month
    return _make_request(params)

@mcp.tool()
def get_t3(
    symbol: str,
    interval: str,
    time_period: int,
    series_type: str,
    month: Optional[str] = None,
    datatype: str = "json"
):
    """
    Triple Exponential Moving Average (T3)

    This API returns the triple exponential moving average (T3) values.
    :param symbol: The ticker symbol (e.g., 'IBM').
    :param interval: Time interval ('1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly').
    :param time_period: Number of data points used to calculate each moving average value.
    :param series_type: The desired price type ('close', 'open', 'high', 'low').
    :param month: Optional month in YYYY-MM format for intraday intervals.
    :param datatype: Output format ('json' or 'csv'). Default is 'json'.
    :return: JSON response.
    """
    params = {
        "function": "T3",
        "symbol": symbol,
        "interval": interval,
        "time_period": time_period,
        "series_type": series_type,
        "datatype": datatype
    }
    if month:
        params["month"] = month
    return _make_request(params)

# Technical Indicators - Momentum & Oscillators
@mcp.tool()
def get_macd(
    symbol: str,
    interval: str,
    series_type: str,
    month: Optional[str] = None,
    fastperiod: int = 12,
    slowperiod: int = 26,
    signalperiod: int = 9,
    datatype: str = "json"
):
    """
    Moving Average Convergence / Divergence (MACD)
    
    This API returns the moving average convergence / divergence (MACD) values.
    :param symbol: The ticker symbol (e.g., 'IBM').
    :param interval: Time interval ('1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly').
    :param series_type: The desired price type ('close', 'open', 'high', 'low').
    :param fastperiod: Fast period (default 12).
    :param slowperiod: Slow period (default 26).
    :param signalperiod: Signal period (default 9).
    :param month: Optional month in YYYY-MM format for intraday intervals.
    :param datatype: Output format ('json' or 'csv'). Default is 'json'.
    :return: JSON response.
    """
    params = {
        "function": "MACD",
        "symbol": symbol,
        "interval": interval,
        "series_type": series_type,
        "fastperiod": fastperiod,
        "slowperiod": slowperiod,
        "signalperiod": signalperiod,
        "datatype": datatype
    }
    if month:
        params["month"] = month
    return _make_request(params)

@mcp.tool()
def get_macdext(
    symbol: str,
    interval: str,
    series_type: str,
    month: Optional[str] = None,
    fastperiod: int = 12,
    slowperiod: int = 26,
    signalperiod: int = 9,
    fastmatype: int = 0,
    slowmatype: int = 0,
    signalmatype: int = 0,
    datatype: str = "json"
):
    """
    MACD with Controllable MA Type (MACDEXT)

    This API returns the MACD values with controllable moving average type.
    :param symbol: The ticker symbol (e.g., 'IBM').
    :param interval: Time interval ('1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly').
    :param series_type: The desired price type ('close', 'open', 'high', 'low').
    :param month: Optional month in YYYY-MM format for intraday intervals.
    :param fastperiod: Fast period parameter. Default is 12.
    :param slowperiod: Slow period parameter. Default is 26.
    :param signalperiod: Signal period parameter. Default is 9.
    :param fastmatype: Fast MA type (0=SMA, 1=EMA, 2=WMA, 3=DEMA, 4=TEMA, 5=TRIMA, 6=KAMA, 7=MAMA, 8=T3). Default is 0.
    :param slowmatype: Slow MA type. Default is 0.
    :param signalmatype: Signal MA type. Default is 0.
    :param datatype: Output format ('json' or 'csv'). Default is 'json'.
    :return: JSON response.
    """
    params = {
        "function": "MACDEXT",
        "symbol": symbol,
        "interval": interval,
        "series_type": series_type,
        "fastperiod": fastperiod,
        "slowperiod": slowperiod,
        "signalperiod": signalperiod,
        "fastmatype": fastmatype,
        "slowmatype": slowmatype,
        "signalmatype": signalmatype,
        "datatype": datatype
    }
    if month:
        params["month"] = month
    return _make_request(params)

@mcp.tool()
def get_stoch(
    symbol: str,
    interval: str,
    month: Optional[str] = None,
    fastkperiod: int = 5,
    slowkperiod: int = 3,
    slowdperiod: int = 3,
    slowkmatype: int = 0,
    slowdmatype: int = 0,
    datatype: str = "json"
):
    """
    Stochastic Oscillator (STOCH)

    This API returns the stochastic oscillator values.
    :param symbol: The ticker symbol (e.g., 'IBM').
    :param interval: Time interval ('1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly').
    :param month: Optional month in YYYY-MM format for intraday intervals.
    :param fastkperiod: Fast K period. Default is 5.
    :param slowkperiod: Slow K period. Default is 3.
    :param slowdperiod: Slow D period. Default is 3.
    :param slowkmatype: Slow K MA type (0=SMA, 1=EMA, 2=WMA, etc.). Default is 0.
    :param slowdmatype: Slow D MA type. Default is 0.
    :param datatype: Output format ('json' or 'csv'). Default is 'json'.
    :return: JSON response.
    """
    params = {
        "function": "STOCH",
        "symbol": symbol,
        "interval": interval,
        "fastkperiod": fastkperiod,
        "slowkperiod": slowkperiod,
        "slowdperiod": slowdperiod,
        "slowkmatype": slowkmatype,
        "slowdmatype": slowdmatype,
        "datatype": datatype
    }
    if month:
        params["month"] = month
    return _make_request(params)

@mcp.tool()
def get_stochf(
    symbol: str,
    interval: str,
    month: Optional[str] = None,
    fastkperiod: int = 5,
    fastdperiod: int = 3,
    fastdmatype: int = 0,
    datatype: str = "json"
):
    """
    Stochastic Fast (STOCHF)

    This API returns the stochastic fast values.
    :param symbol: The ticker symbol (e.g., 'IBM').
    :param interval: Time interval ('1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly').
    :param month: Optional month in YYYY-MM format for intraday intervals.
    :param fastkperiod: Fast K period. Default is 5.
    :param fastdperiod: Fast D period. Default is 3.
    :param fastdmatype: Fast D MA type (0=SMA, 1=EMA, 2=WMA, etc.). Default is 0.
    :param datatype: Output format ('json' or 'csv'). Default is 'json'.
    :return: JSON response.
    """
    params = {
        "function": "STOCHF",
        "symbol": symbol,
        "interval": interval,
        "fastkperiod": fastkperiod,
        "fastdperiod": fastdperiod,
        "fastdmatype": fastdmatype,
        "datatype": datatype
    }
    if month:
        params["month"] = month
    return _make_request(params)

@mcp.tool()
def get_rsi(
    symbol: str,
    interval: str,
    time_period: int,
    series_type: str,
    month: Optional[str] = None,
    datatype: str = "json"
):
    """
    Relative Strength Index (RSI)
    
    This API returns the relative strength index (RSI) values.
    :param symbol: The ticker symbol (e.g., 'IBM').
    :param interval: Time interval ('1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly').
    :param time_period: Number of data points used to calculate each RSI value.
    :param series_type: The desired price type ('close', 'open', 'high', 'low').
    :param month: Optional month in YYYY-MM format for intraday intervals.
    :param datatype: Output format ('json' or 'csv'). Default is 'json'.
    :return: JSON response.
    """
    params = {
        "function": "RSI",
        "symbol": symbol,
        "interval": interval,
        "time_period": time_period,
        "series_type": series_type,
        "datatype": datatype
    }
    if month:
        params["month"] = month
    return _make_request(params)

@mcp.tool()
def get_stochrsi(
    symbol: str,
    interval: str,
    time_period: int,
    series_type: str,
    month: Optional[str] = None,
    fastkperiod: int = 5,
    fastdperiod: int = 3,
    fastdmatype: int = 0,
    datatype: str = "json"
):
    """
    Stochastic Relative Strength Index (STOCHRSI)

    This API returns the stochastic relative strength index (STOCHRSI) values.
    :param symbol: The ticker symbol (e.g., 'IBM').
    :param interval: Time interval ('1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly').
    :param time_period: Number of data points used to calculate each STOCHRSI value.
    :param series_type: The desired price type ('close', 'open', 'high', 'low').
    :param month: Optional month in YYYY-MM format for intraday intervals.
    :param fastkperiod: Fast K period. Default is 5.
    :param fastdperiod: Fast D period. Default is 3.
    :param fastdmatype: Fast D MA type (0=SMA, 1=EMA, 2=WMA, etc.). Default is 0.
    :param datatype: Output format ('json' or 'csv'). Default is 'json'.
    :return: JSON response.
    """
    params = {
        "function": "STOCHRSI",
        "symbol": symbol,
        "interval": interval,
        "time_period": time_period,
        "series_type": series_type,
        "fastkperiod": fastkperiod,
        "fastdperiod": fastdperiod,
        "fastdmatype": fastdmatype,
        "datatype": datatype
    }
    if month:
        params["month"] = month
    return _make_request(params)

@mcp.tool()
def get_trange(
    symbol: str,
    interval: str,
    month: Optional[str] = None,
    datatype: str = "json"
):
    """
    True Range (TRANGE)

    This API returns the true range values.
    :param symbol: The ticker symbol (e.g., 'IBM').
    :param interval: Time interval ('1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly').
    :param month: Optional month in YYYY-MM format for intraday intervals.
    :param datatype: Output format ('json' or 'csv'). Default is 'json'.
    :return: JSON response.
    """
    params = {
        "function": "TRANGE",
        "symbol": symbol,
        "interval": interval,
        "datatype": datatype
    }
    if month:
        params["month"] = month
    return _make_request(params)

@mcp.tool()
def get_atr(
    symbol: str,
    interval: str,
    time_period: int,
    month: Optional[str] = None,
    datatype: str = "json"
):
    """
    Average True Range (ATR)

    This API returns the average true range (ATR) values.
    :param symbol: The ticker symbol (e.g., 'IBM').
    :param interval: Time interval ('1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly').
    :param time_period: Number of data points used to calculate each ATR value.
    :param month: Optional month in YYYY-MM format for intraday intervals.
    :param datatype: Output format ('json' or 'csv'). Default is 'json'.
    :return: JSON response.
    """
    params = {
        "function": "ATR",
        "symbol": symbol,
        "interval": interval,
        "time_period": time_period,
        "datatype": datatype
    }
    if month:
        params["month"] = month
    return _make_request(params)

@mcp.tool()
def get_natr(
    symbol: str,
    interval: str,
    time_period: int,
    month: Optional[str] = None,
    datatype: str = "json"
):
    """
    Normalized Average True Range (NATR)

    This API returns the normalized average true range (NATR) values.
    :param symbol: The ticker symbol (e.g., 'IBM').
    :param interval: Time interval ('1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly').
    :param time_period: Number of data points used to calculate each NATR value.
    :param month: Optional month in YYYY-MM format for intraday intervals.
    :param datatype: Output format ('json' or 'csv'). Default is 'json'.
    :return: JSON response.
    """
    params = {
        "function": "NATR",
        "symbol": symbol,
        "interval": interval,
        "time_period": time_period,
        "datatype": datatype
    }
    if month:
        params["month"] = month
    return _make_request(params)

@mcp.tool()
def get_ad(
    symbol: str,
    interval: str,
    month: Optional[str] = None,
    datatype: str = "json"
):
    """
    Chaikin A/D Line (AD)

    This API returns the Chaikin A/D line values.
    :param symbol: The ticker symbol (e.g., 'IBM').
    :param interval: Time interval ('1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly').
    :param month: Optional month in YYYY-MM format for intraday intervals.
    :param datatype: Output format ('json' or 'csv'). Default is 'json'.
    :return: JSON response.
    """
    params = {
        "function": "AD",
        "symbol": symbol,
        "interval": interval,
        "datatype": datatype
    }
    if month:
        params["month"] = month
    return _make_request(params)

@mcp.tool()
def get_adosc(
    symbol: str,
    interval: str,
    month: Optional[str] = None,
    fastperiod: int = 3,
    slowperiod: int = 10,
    datatype: str = "json"
):
    """
    Chaikin A/D Oscillator (ADOSC)

    This API returns the Chaikin A/D oscillator values.
    :param symbol: The ticker symbol (e.g., 'IBM').
    :param interval: Time interval ('1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly').
    :param month: Optional month in YYYY-MM format for intraday intervals.
    :param fastperiod: Fast period parameter. Default is 3.
    :param slowperiod: Slow period parameter. Default is 10.
    :param datatype: Output format ('json' or 'csv'). Default is 'json'.
    :return: JSON response.
    """
    params = {
        "function": "ADOSC",
        "symbol": symbol,
        "interval": interval,
        "fastperiod": fastperiod,
        "slowperiod": slowperiod,
        "datatype": datatype
    }
    if month:
        params["month"] = month
    return _make_request(params)

@mcp.tool()
def get_obv(
    symbol: str,
    interval: str,
    month: Optional[str] = None,
    datatype: str = "json"
):
    """
    On Balance Volume (OBV)

    This API returns the on balance volume (OBV) values.
    :param symbol: The ticker symbol (e.g., 'IBM').
    :param interval: Time interval ('1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly').
    :param month: Optional month in YYYY-MM format for intraday intervals.
    :param datatype: Output format ('json' or 'csv'). Default is 'json'.
    :return: JSON response.
    """
    params = {
        "function": "OBV",
        "symbol": symbol,
        "interval": interval,
        "datatype": datatype
    }
    if month:
        params["month"] = month
    return _make_request(params)

@mcp.tool()
def get_ht_trendline(
    symbol: str,
    interval: str,
    series_type: str,
    month: Optional[str] = None,
    datatype: str = "json"
):
    """
    Hilbert Transform - Instantaneous Trendline (HT_TRENDLINE)

    This API returns the Hilbert Transform instantaneous trendline values.
    :param symbol: The ticker symbol (e.g., 'IBM').
    :param interval: Time interval ('1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly').
    :param series_type: The desired price type ('close', 'open', 'high', 'low').
    :param month: Optional month in YYYY-MM format for intraday intervals.
    :param datatype: Output format ('json' or 'csv'). Default is 'json'.
    :return: JSON response.
    """
    params = {
        "function": "HT_TRENDLINE",
        "symbol": symbol,
        "interval": interval,
        "series_type": series_type,
        "datatype": datatype
    }
    if month:
        params["month"] = month
    return _make_request(params)

@mcp.tool()
def get_ht_sine(
    symbol: str,
    interval: str,
    series_type: str,
    month: Optional[str] = None,
    datatype: str = "json"
):
    """
    Hilbert Transform - SineWave (HT_SINE)

    This API returns the Hilbert Transform sine wave values.
    :param symbol: The ticker symbol (e.g., 'IBM').
    :param interval: Time interval ('1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly').
    :param series_type: The desired price type ('close', 'open', 'high', 'low').
    :param month: Optional month in YYYY-MM format for intraday intervals.
    :param datatype: Output format ('json' or 'csv'). Default is 'json'.
    :return: JSON response.
    """
    params = {
        "function": "HT_SINE",
        "symbol": symbol,
        "interval": interval,
        "series_type": series_type,
        "datatype": datatype
    }
    if month:
        params["month"] = month
    return _make_request(params)

@mcp.tool()
def get_ht_trendmode(
    symbol: str,
    interval: str,
    series_type: str,
    month: Optional[str] = None,
    datatype: str = "json"
):
    """
    Hilbert Transform - Trend vs Cycle Mode (HT_TRENDMODE)

    This API returns the Hilbert Transform trend vs cycle mode values.
    :param symbol: The ticker symbol (e.g., 'IBM').
    :param interval: Time interval ('1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly').
    :param series_type: The desired price type ('close', 'open', 'high', 'low').
    :param month: Optional month in YYYY-MM format for intraday intervals.
    :param datatype: Output format ('json' or 'csv'). Default is 'json'.
    :return: JSON response.
    """
    params = {
        "function": "HT_TRENDMODE",
        "symbol": symbol,
        "interval": interval,
        "series_type": series_type,
        "datatype": datatype
    }
    if month:
        params["month"] = month
    return _make_request(params)

@mcp.tool()
def get_ht_dcperiod(
    symbol: str,
    interval: str,
    series_type: str,
    month: Optional[str] = None,
    datatype: str = "json"
):
    """
    Hilbert Transform - Dominant Cycle Period (HT_DCPERIOD)

    This API returns the Hilbert Transform dominant cycle period values.
    :param symbol: The ticker symbol (e.g., 'IBM').
    :param interval: Time interval ('1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly').
    :param series_type: The desired price type ('close', 'open', 'high', 'low').
    :param month: Optional month in YYYY-MM format for intraday intervals.
    :param datatype: Output format ('json' or 'csv'). Default is 'json'.
    :return: JSON response.
    """
    params = {
        "function": "HT_DCPERIOD",
        "symbol": symbol,
        "interval": interval,
        "series_type": series_type,
        "datatype": datatype
    }
    if month:
        params["month"] = month
    return _make_request(params)

@mcp.tool()
def get_ht_dcphase(
    symbol: str,
    interval: str,
    series_type: str,
    month: Optional[str] = None,
    datatype: str = "json"
):
    """
    Hilbert Transform - Dominant Cycle Phase (HT_DCPHASE)

    This API returns the Hilbert Transform dominant cycle phase values.
    :param symbol: The ticker symbol (e.g., 'IBM').
    :param interval: Time interval ('1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly').
    :param series_type: The desired price type ('close', 'open', 'high', 'low').
    :param month: Optional month in YYYY-MM format for intraday intervals.
    :param datatype: Output format ('json' or 'csv'). Default is 'json'.
    :return: JSON response.
    """
    params = {
        "function": "HT_DCPHASE",
        "symbol": symbol,
        "interval": interval,
        "series_type": series_type,
        "datatype": datatype
    }
    if month:
        params["month"] = month
    return _make_request(params)

@mcp.tool()
def get_ht_phasor(
    symbol: str,
    interval: str,
    series_type: str,
    month: Optional[str] = None,
    datatype: str = "json"
):
    """
    Hilbert Transform - Phasor Components (HT_PHASOR)

    This API returns the Hilbert Transform phasor components values.
    :param symbol: The ticker symbol (e.g., 'IBM').
    :param interval: Time interval ('1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly').
    :param series_type: The desired price type ('close', 'open', 'high', 'low').
    :param month: Optional month in YYYY-MM format for intraday intervals.
    :param datatype: Output format ('json' or 'csv'). Default is 'json'.
    :return: JSON response.
    """
    params = {
        "function": "HT_PHASOR",
        "symbol": symbol,
        "interval": interval,
        "series_type": series_type,
        "datatype": datatype
    }
    if month:
        params["month"] = month
    return _make_request(params)


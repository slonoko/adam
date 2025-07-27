import requests
import os
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from typing import Optional

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
def get_daily_data(symbol: str, output_size: str = "compact"):
    """
    Fetch daily stock data.
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
def get_news_and_sentiment(
    tickers: str = "",
    time_from: str = "",
    time_to: str = "",
    sort: str = "RELEVANCE",
):
    """
    Fetch news and sentiment data for a given keyword.

    :param tickers: (Optional) The stock/crypto/forex symbols of your choice. For example: tickers=IBM will filter for articles that mention the IBM ticker; tickers=COIN,CRYPTO:BTC,FOREX:USD will filter for articles that simultaneously mention Coinbase (COIN), Bitcoin (CRYPTO:BTC), and US Dollar (FOREX:USD) in their content.
    :param topics: (Optional) The news topics of your choice. For example: topics=technology will filter for articles that write about the technology sector; topics=technology,ipo will filter for articles that simultaneously cover technology and IPO in their content.
        Below is the full list of supported topics:
            Blockchain: blockchain
            Earnings: earnings
            IPO: ipo
            Mergers & Acquisitions: mergers_and_acquisitions
            Financial Markets: financial_markets
            Economy - Fiscal Policy (e.g., tax reform, government spending): economy_fiscal
            Economy - Monetary Policy (e.g., interest rates, inflation): economy_monetary
            Economy - Macro/Overall: economy_macro
            Energy & Transportation: energy_transportation
            Finance: finance
            Life Sciences: life_sciences
            Manufacturing: manufacturing
            Real Estate & Construction: real_estate
            Retail & Wholesale: retail_wholesale
            Technology: technology
    :param time_from: (Optional) The time range of the news articles you are targeting, in YYYYMMDDTHHMM format. For example: time_from=20220410T0130. If time_from is specified but time_to is missing, the API will return articles published between the time_from value and the current time.
    :param time_to: (Optional) The time range of the news articles you are targeting, in YYYYMMDDTHHMM format. For example: time_from=20220410T0130. If time_from is specified but time_to is missing, the API will return articles published between the time_from value and the current time.
    :param sort: (Optional) By default, sort=LATEST and the API will return the latest articles first. You can also set sort=EARLIEST or sort=RELEVANCE based on your use case.
    :return: JSON response.
    """
    params = {
        "function": "NEWS_SENTIMENT",
        "tickers": tickers,
        "time_from": time_from,
        "time_to": time_to,
        "sort": sort,
    }
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
    :return: JSON response.
    """
    params = {
        "function": "EARNINGS_CALENDAR",
        "horizon": horizon
    }
    if symbol:
        params["symbol"] = symbol
    return _make_request(params)

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


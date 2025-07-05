import requests
import os
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
# Create an MCP server

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

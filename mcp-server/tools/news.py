import requests
import os
from fastmcp import FastMCP
from dotenv import load_dotenv
from typing import Optional
import requests
from langchain_community.utilities import GoogleSerperAPIWrapper

load_dotenv()

BASE_URL = "https://newsapi.org/v2/everything"
API_KEY = os.getenv("NEWS_API_KEY")
if not API_KEY:
    raise ValueError(
        "API key for NEWS API is not set. Please set the NEWS_API_KEY environment variable."
    )
AV_BASE_URL = "https://www.alphavantage.co/query"
AV_API_KEY = os.getenv("ALPHAVANTAGE_KEY")
if not AV_API_KEY:
    raise ValueError(
        "API key for Alpha Vantage is not set. Please set the ALPHAVANTAGE_KEY environment variable."
    )


def _make_request(params):
    params["apikey"] = AV_API_KEY
    response = requests.get(AV_BASE_URL, params=params)
    response.raise_for_status()
    return response.json()

mcp = FastMCP("news")

@mcp.tool
def google_search(query: str) -> str:
    """Search the web for information related to a query.

    Args:
        query: The search query

    Returns:
        Search results as text
    """
    try:
        search = GoogleSerperAPIWrapper()
        result = search.run(query)
        return result
    except Exception as e:
        return "I couldn't perform the search due to a technical issue."

@mcp.tool
def get_news(query: str, from_date: Optional[str] = None, sort_by: str = "popularity"):
    """Fetches news articles based on the provided query and date range.
    Args:
        query (str): The search query for news articles.
        from_date (Optional[str]): The start date for the news articles in YYYY-MM-DD format.
        sort_by (str): The order to sort the articles in. Possible options: relevancy, popularity, publishedAt
    Returns:
        dict: A dictionary containing the news articles.
    Raises:
        Exception: If the API request fails or returns an error.
    """

    params = {
        "q": query,
        "from": from_date,
        "sortBy": sort_by,
        "apiKey": API_KEY
    }
    
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Error fetching news: {response.status_code} - {response.text}")
    
    return response.json()


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
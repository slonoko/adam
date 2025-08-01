import requests
import os
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from typing import Optional
import requests

load_dotenv()
BASE_URL = "https://newsapi.org/v2/everything"
API_KEY = os.getenv("NEWS_API_KEY")
if not API_KEY:
    raise ValueError(
        "API key for NEWS API is not set. Please set the NEWS_API_KEY environment variable."
    )

mcp = FastMCP("news")

@mcp.tool()
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
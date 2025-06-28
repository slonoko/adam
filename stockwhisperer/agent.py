from google.adk.agents import LlmAgent
import logging
from dotenv import load_dotenv
import sys
from tools.stocks_data import *

load_dotenv()
logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)",
    datefmt="%Y-%m-%d %H:%M:%S",
)


root_agent = LlmAgent(
    name="StockWhisperer",
    model="gemini-2.5-flash-preview-04-17",
    description=("The Stock Whisperer – Speaks fluent bull and bear 🐂🐻. "
                    "An AI-powered stockbroker that provides real-time data access, "
                    "market analysis, and personalized financial recommendations. "
                    "It can analyze stock trends, monitor financial news, provide exchange rate updates, "
                    "and respond to market events while adapting to individual user goals and risk profiles. "
                    "Whether you are an investor seeking guidance, a trader looking for quick updates, "
                    "or a professional managing a portfolio, Stock Whisperer ensures intelligent, data-driven decision-making around the clock."
    ),
    tools=[
        get_intraday_data,
        get_daily_data,
        get_weekly_data,
        get_monthly_data,
        get_quote,
        search_symbol,
        get_news_and_sentiment,
    ],  # Tool to query memory
)

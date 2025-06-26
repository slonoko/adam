from google.adk.agents import LlmAgent
import logging
from dotenv import load_dotenv
import sys
from google.adk.tools import load_memory  # Tool to query memory
from tools.weather import get_current_weather, get_weather_forecast
from tools.exchange_rate import convert, get_exchange_rates
from tools.datetime import current_date_and_time
from tools.stocks_data import *

load_dotenv()
logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)",
    datefmt="%Y-%m-%d %H:%M:%S",
)


root_agent = LlmAgent(
    name="stockbroker",
    model="gemini-2.0-flash-exp",
    description=(
        "EquiBot is an advanced AI-powered assistant designed to support or replace the functions of a traditional stockbroker."
        "Equipped with real-time data access, EquiBot provides timely insights, market analysis, and personalized financial recommendations."
        "It is capable of performing key broker tasks such as analyzing stock trends, monitoring financial news, providing exchange rate updates, and responding to market events, all while adapting to individual user goals and risk profiles."
        "Whether you are an investor seeking guidance, a trader looking for quick updates, or a professional managing a portfolio, EquiBot ensures intelligent, data-driven decision-making around the clock."
    ),
    tools=[
        current_date_and_time,
        get_exchange_rates,
        convert,
        get_current_weather,
        get_weather_forecast,
        get_intraday_data,
        get_daily_data,
        get_weekly_data,
        get_monthly_data,
        get_quote,
        search_symbol,
    ],  # Tool to query memory
)

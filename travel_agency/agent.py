from google.adk.agents import LlmAgent
import logging
from dotenv import load_dotenv
import sys
from google.adk.tools import load_memory  # Tool to query memory
from tools.flights import *
from tools.weather import get_weather
from tools.exchange_rate import convert, get_exchange_rates
from tools.datetime import current_date_and_time

load_dotenv()
logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)",
    datefmt="%Y-%m-%d %H:%M:%S",
)


root_agent = LlmAgent(
    name="travel_agency",
    model="gemini-2.0-flash-exp",
    description=(
        "Travel agency assistant. I can help you with flight information, exchange rates, and weather conditions."
    ),
    instruction="You are a travel agency. As a coordinator, you may use your common knowledge to derive certain information, additionally, you can use the tools to help answer the user's questions by using the answers of tools to find the flights."
    "You can use tools to help you with your tasks:"
    "1. Echange rate tool: You can help users with exchange rates."
    "2. Weather tool: You can help users with weather conditions."
    "3. Date and time tool: You can help users with getting the current date and time, or use it yourself if you need to get the current date and time."
    "4. Flight assistant tool: You can help users with flight information."
    "Analyze the user's request, break it down to tasks, and execute these tasks to reach the desired answer. You may use your common knowledge as well as delegate it to the appropriate tools(s).",
    tools=[
        current_date_and_time,
        one_way_flight,
        twoway_flights_month,
        airports_information,
        round_trip_flight,
        oneway_flights_month,
        get_exchange_rates,
        convert,
        get_weather,
    ],  # Tool to query memory
)

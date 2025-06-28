from google.adk.agents import LlmAgent
import logging
from dotenv import load_dotenv
import sys
from google.adk.tools import load_memory  # Tool to query memory
from tools.weather import get_current_weather, get_weather_forecast
from google.adk.models.lite_llm import LiteLlm

load_dotenv()
logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)",
    datefmt="%Y-%m-%d %H:%M:%S",
)


root_agent = LlmAgent(
    name="DailyDrip",
    model="gemini-2.5-flash-preview-04-17",
    description=("The Daily Drip – For that slow, steady weather tea"
                 " that keeps you informed and ready for the day ahead."
                 " It provides daily weather updates, forecasts, and current conditions"
                 " to help you plan your day with confidence."
    ),
    tools=[
        get_current_weather,
        get_weather_forecast,
    ],  # Tool to query memory
)

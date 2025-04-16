from google.adk.agents import Agent
import requests
import datetime
from zoneinfo import ZoneInfo

def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city for which to retrieve the weather report.

    Returns:
        dict: status and result or error msg.
    """
    try:
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url)
        response.raise_for_status()
        weather_data = response.json()
        report = {
            "temperature": weather_data["current_condition"][0]["temp_C"],
            "description": weather_data["current_condition"][0]["weatherDesc"][0]["value"],
            "humidity": weather_data["current_condition"][0]["humidity"],
        }
        return {"status": "success", "report": weather_data["current_condition"]}
    except requests.RequestException as e:
        return {"status": "error", "error_message": f"Failed to fetch weather data: {e}"}
    except KeyError as e:
        return {"status": "error", "error_message": f"Unexpected response format: {e}"}

def current_date_and_time(format:str="%A, %B %d, %Y %H:%M:%S", timezone: str="localtime") -> str:
    """
    A usefull function that takes as input the date and time format as optional parameter, the timezone with default to the system locale, and returns the current date and time.
    Args:
        format (str): The date and time format to be returned.
        timezone (str): The timezone to be used. Default is "localtime".

    Returns:
        str: the current date and time in the specified format and timezone.
    """

    tz=ZoneInfo(timezone)
    return datetime.datetime.now(tz).strftime(format)

root_agent = Agent(
    name="weather_time_agent",
    model="gemini-2.0-flash-exp",
    description=(
        "Agent to answer questions about the time and weather in a city."
    ),
    instruction=(
        "I can answer your questions about the time and weather in a city."
    ),
    tools=[get_weather, current_date_and_time],
)
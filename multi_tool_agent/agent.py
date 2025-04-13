import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
import requests

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

def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.

    Args:
        city (str): The name of the city for which to retrieve the current time.

    Returns:
        dict: status and result or error msg.
    """
    try:
        url = f"https://nominatim.openstreetmap.org/search.php?q={city}&format=jsonv2"
        response = requests.get(url, headers={"User-Agent": "Agent/007", "Connection": "keep-alive"})
        response.raise_for_status()
        location_data = response.json()
        if not location_data:
            return {"status": "error", "error_message": f"City '{city}' not found."}
        lat = location_data[0]["lat"]
        lon = location_data[0]["lon"]

        time_url = f"https://timeapi.io/api/time/current/coordinate?latitude={lat}&longitude={lon}"
        t_response = requests.get(time_url,headers={"User-Agent": "Agent/007", "Connection": "keep-alive"})
        t_response.raise_for_status()
        t_data = t_response.json()
        now = t_data["dateTime"]
        report = (
            f'The current time in {city} is {now}'
        )
        return {"status": "success", "report": report}
    except requests.RequestException as e:
        return {"status": "error", "error_message": f"Failed to fetch timezone data: {e}"}

root_agent = Agent(
    name="weather_time_agent",
    model="gemini-2.0-flash-exp",
    description=(
        "Agent to answer questions about the time and weather in a city."
    ),
    instruction=(
        "I can answer your questions about the time and weather in a city."
    ),
    tools=[get_weather, get_current_time],
)
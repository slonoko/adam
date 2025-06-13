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
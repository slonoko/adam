from google.adk.agents import Agent
import requests
import datetime
from zoneinfo import ZoneInfo
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("stockwhisperer")   

@mcp.tool()
def get_current_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city for which to retrieve the weather report.

    Returns:
        dict: status and result or error msg.
    """
    return get_weather_forecast(city, datetime.datetime.now(ZoneInfo("UTC")).strftime("%Y-%m-%d"))

@mcp.tool()
def get_weather_forecast(city: str, date: str) -> dict:
    """Retrieves the weather report for a specified city and specific day.

    Args:
        city (str): The name of the city for which to retrieve the weather report.
        date (str): The date for which to retrieve the weather report in 'YYYY-MM-DD' format.

    Returns:
        dict: status and result or error msg.
    """
    try:
        url = f"https://wttr.in/{city}@{date}?format=j1"
        response = requests.get(url)
        response.raise_for_status()
        weather_data = response.json()
        return {"status": "success", "report": weather_data}
    except requests.RequestException as e:
        return {"status": "error", "error_message": f"Failed to fetch weather data: {e}"}
    except KeyError as e:
        return {"status": "error", "error_message": f"Unexpected response format: {e}"}
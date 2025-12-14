import requests
import datetime
from zoneinfo import ZoneInfo
from fastmcp import FastMCP

mcp = FastMCP("weather")


@mcp.tool()
def get_current_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city for which to retrieve the weather report.

    Returns:
        dict: status and result or error msg.
    """
    return __get_weather_forecast(
        city, datetime.datetime.now(ZoneInfo("UTC")).strftime("%Y-%m-%d")
    )


@mcp.tool()
def get_weather_forecast(city: str, date: str) -> dict:
    """Retrieves the weather report for a specified city and specific day.

    Args:
        city (str): The name of the city for which to retrieve the weather report.
        date (str): The date for which to retrieve the weather report in 'YYYY-MM-DD' format.

    Returns:
        dict: status and result or error msg.
    """
    return __get_weather_forecast(city, date)


def __get_weather_forecast(city: str, date: str) -> dict:
    try:
        url = f"https://wttr.in/{city}@{date}?format=j1"
        response = requests.get(url)
        response.raise_for_status()
        weather_data = response.json()
        return {"status": "success", "report": weather_data}
    except requests.RequestException as e:
        return {
            "status": "error",
            "error_message": f"Failed to fetch weather data: {e}",
        }
    except KeyError as e:
        return {"status": "error", "error_message": f"Unexpected response format: {e}"}


@mcp.tool()
def get_weather_alerts(city: str) -> dict:
    """Retrieves weather alerts and warnings for a specified city.

    Args:
        city (str): The name of the city for which to retrieve weather alerts.

    Returns:
        dict: status and alerts or error msg.
    """
    try:
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url)
        response.raise_for_status()
        weather_data = response.json()
        alerts = weather_data.get("alerts", [])
        return {"status": "success", "alerts": alerts}
    except requests.RequestException as e:
        return {
            "status": "error",
            "error_message": f"Failed to fetch weather alerts: {e}",
        }


@mcp.tool()
def get_extended_forecast(city: str, days: int = 5) -> dict:
    """Retrieves extended weather forecast for multiple days.

    Args:
        city (str): The name of the city for which to retrieve the forecast.
        days (int): Number of days to forecast (default: 5).

    Returns:
        dict: status and extended forecast or error msg.
    """
    try:
        forecasts = []
        base_date = datetime.datetime.now(ZoneInfo("UTC"))

        for i in range(days):
            forecast_date = (base_date + datetime.timedelta(days=i)).strftime(
                "%Y-%m-%d"
            )
            result = __get_weather_forecast(city, forecast_date)
            if result["status"] == "success":
                forecasts.append({"date": forecast_date, "weather": result["report"]})

        return {"status": "success", "extended_forecast": forecasts}
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to fetch extended forecast: {e}",
        }


@mcp.tool()
def compare_weather(city1: str, city2: str, date: str) -> dict:
    """Compares weather between two cities on a specific date.

    Args:
        city1 (str): First city to compare.
        city2 (str): Second city to compare.
        date (str): Date for the weather comparison in 'YYYY-MM-DD' format.

    Returns:
        dict: status and weather comparison or error msg.
    """
    weather1 = __get_weather_forecast(city1, date)
    weather2 = __get_weather_forecast(city2, date)

    if weather1["status"] == "error" or weather2["status"] == "error":
        return {
            "status": "error",
            "error_message": "Failed to fetch weather for one or both cities",
        }

    return {
        "status": "success",
        "comparison": {city1: weather1["report"], city2: weather2["report"]},
    }


@mcp.tool()
def get_weather_by_coordinates(lat: float, lon: float) -> dict:
    """Retrieves current weather by geographic coordinates.

    Args:
        lat (float): Latitude coordinate.
        lon (float): Longitude coordinate.

    Returns:
        dict: status and weather report or error msg.
    """
    try:
        url = f"https://wttr.in/{lat},{lon}?format=j1"
        response = requests.get(url)
        response.raise_for_status()
        weather_data = response.json()
        return {"status": "success", "report": weather_data}
    except requests.RequestException as e:
        return {
            "status": "error",
            "error_message": f"Failed to fetch weather data: {e}",
        }

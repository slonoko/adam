# http://192.168.178.63:1880/room/bed?from=2025-12-10&to=2025-12-14

from fastmcp import FastMCP
from dotenv import load_dotenv
import os
import logging
import sys
import json

load_dotenv()

logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)",
    datefmt="%Y-%m-%d %H:%M:%S",
)


# Create an MCP server
mcp = FastMCP("homesensor", streamable_http_path="/homesensor")

@mcp.tool
def get_room_temperature_humidity_with_only_latest(room: str) -> dict:
    """
    Get room tenperature and humidity data for the latest available date.

    Args:
        room (str): The room name to get data for. the only supported values are "bed", "bath", "guest", "balcony" and "living"

    Returns:
        str: Sensor data in JSON format.
    """
    import requests

    response = requests.get(f"{os.getenv('SENSOR_URL')}/{room}")
    if response.status_code == 200:
        return response.json()
    else:
        return {}

@mcp.tool
def get_room_temperature_humidity_with_date_range(room: str,from_date: str, to_date: str) -> dict:
    """
    Get room tenperature and humidity data for a given date range.

    Args:
        from_date (str): Start date in YYYY-MM-DD format.
        to_date (str): End date in YYYY-MM-DD format.
        room (str): The room name to get data for. the only supported values are "bed", "bath", "guest", "balcony" and "living"

    Returns:
        str: Sensor data in JSON format.
    """
    import requests

    response = requests.get(f"{os.getenv('SENSOR_URL')}/{room}?from={from_date}&to={to_date}")
    if response.status_code == 200:
        return response.json()
    else:
        return {}

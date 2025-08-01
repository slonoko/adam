import requests
import datetime
from zoneinfo import ZoneInfo
from dotenv import load_dotenv
import os
import logging
import sys
import json
from mcp.server.fastmcp import FastMCP

load_dotenv()

logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)",
    datefmt="%Y-%m-%d %H:%M:%S",
)

api_url = f"https://v6.exchangerate-api.com/v6/{os.getenv('EXCHANGE_RATE_API_KEY')}/" # https://v6.exchangerate-api.com/v6/798cf9e73e046e42a8be7813/latest/USD


# Create an MCP server
mcp = FastMCP("cashanova")


@mcp.tool()
def get_exchange_rates(from_currency: str = "USD") -> dict:
    """
    Get exchange rates for a given currency.
    Args:
        from_currency (str): The base currency for which to get exchange rates.
    Returns:
        dict: A dictionary containing exchange rates for the given currency.

    """

    response = requests.get(f"{api_url}/latest/{from_currency}")
    if response.status_code == 200:
        return response.json().get("conversion_rates", {})
    else:
        return {}

@mcp.tool()
def convert(
    amount: float, from_currency: str = "USD", to_currency: str = "EUR"
) -> dict:
    """
    Convert an amount from one currency to another.
    Args:
        amount (float): The amount to convert.
        from_currency (str): The currency to convert from.
        to_currency (str): The currency to convert to.
    Returns:
        dict: A Json object containing the conversion among other thing.
    Raises:
        ValueError: If the currency is not supported.
    """

    response = requests.get(f"{api_url}/pair/{from_currency}/{to_currency}/{amount}")
    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError(
            f"Error converting {amount} {from_currency} to {to_currency}: {response.text}"
        )
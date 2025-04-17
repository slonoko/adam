from google.adk.agents import Agent
import requests
import datetime
from zoneinfo import ZoneInfo

api_url = "https://api.exchangerate-api.com/v4/latest/"


def get_exchange_rates(from_currency: str = "USD") -> dict:
    """
    Get exchange rates for a given currency.
    Args:
        from_currency (str): The base currency for which to get exchange rates.
    Returns:
        dict: A dictionary containing exchange rates for the given currency.

    """

    response = requests.get(f"{api_url}{from_currency}")
    if response.status_code == 200:
        return response.json().get("rates", {})
    else:
        return {}


def convert(
    amount: float, from_currency: str = "USD", to_currency: str = "EUR"
) -> float:
    """
    Convert an amount from one currency to another.
    Args:
        amount (float): The amount to convert.
        from_currency (str): The currency to convert from.
        to_currency (str): The currency to convert to.
    Returns:
        float: The converted amount.
    Raises:
        ValueError: If the currency is not supported.
    """

    rates = get_exchange_rates(from_currency)
    if to_currency in rates:
        return amount * rates[to_currency]
    else:
        raise ValueError(f"Currency {to_currency} not supported.")


root_agent = Agent(
    name="exchange_rate_agent",
    model="gemini-2.0-flash-exp",
    description=("Agent to answer questions about the currencies exchange rates."),
    instruction=("I can answer your questions about the currencies exchange rate."),
    tools=[get_exchange_rates, convert],
)

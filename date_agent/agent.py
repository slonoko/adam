from google.adk.agents import Agent
import requests
import datetime
from zoneinfo import ZoneInfo

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
    name="date_agent",
    model="gemini-2.0-flash-exp",
    description=(
        "Agent to answer questions about the current date and time in a city."
    ),
    instruction=(
        "I can answer your questions about the current date and time in a city."
    ),
    tools=[current_date_and_time],
)
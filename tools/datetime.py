import datetime
from zoneinfo import ZoneInfo
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("timekeeper")   

@mcp.tool()
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


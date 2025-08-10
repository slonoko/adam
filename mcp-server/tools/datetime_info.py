import datetime
from zoneinfo import ZoneInfo
from fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("timekeeper", streamable_http_path="/timekeeper")


@mcp.tool
def current_date_and_time(
    format: str = "%A, %B %d, %Y %H:%M:%S", timezone: str = "localtime"
) -> str:
    """
    A usefull function that takes as input the date and time format as optional parameter, the timezone with default to the system locale, and returns the current date and time.
    Args:
        format (str): The date and time format to be returned.
        timezone (str): The timezone to be used. Default is "localtime".

    Returns:
        str: the current date and time in the specified format and timezone.
    """

    tz = ZoneInfo(timezone)
    return datetime.datetime.now(tz).strftime(format)


@mcp.tool
def date_difference(date1: str, date2: str, unit: str = "days") -> int:
    """
    Calculate the difference between two dates.
    Args:
        date1 (str): First date in YYYY-MM-DD format
        date2 (str): Second date in YYYY-MM-DD format
        unit (str): Unit of difference ('days', 'hours', 'minutes', 'seconds')

    Returns:
        int: The difference between the dates in the specified unit
    """
    d1 = datetime.datetime.fromisoformat(date1)
    d2 = datetime.datetime.fromisoformat(date2)
    diff = d2 - d1

    if unit == "days":
        return diff.days
    elif unit == "hours":
        return int(diff.total_seconds() / 3600)
    elif unit == "minutes":
        return int(diff.total_seconds() / 60)
    elif unit == "seconds":
        return int(diff.total_seconds())
    else:
        return diff.days


@mcp.tool
def add_time_to_date(
    date_str: str, days: int = 0, hours: int = 0, minutes: int = 0
) -> str:
    """
    Add time to a given date.
    Args:
        date_str (str): Date in YYYY-MM-DD HH:MM:SS format
        days (int): Number of days to add
        hours (int): Number of hours to add
        minutes (int): Number of minutes to add

    Returns:
        str: The resulting date and time
    """
    dt = datetime.datetime.fromisoformat(date_str)
    result = dt + datetime.timedelta(days=days, hours=hours, minutes=minutes)
    return result.isoformat()


@mcp.tool
def day_of_week(date_str: str) -> str:
    """
    Get the day of the week for a given date.
    Args:
        date_str (str): Date in YYYY-MM-DD format

    Returns:
        str: Day of the week (Monday, Tuesday, etc.)
    """
    dt = datetime.datetime.fromisoformat(date_str)
    return dt.strftime("%A")


@mcp.tool
def time_until_date(target_date: str, timezone: str = "localtime") -> str:
    """
    Calculate time remaining until a target date.
    Args:
        target_date (str): Target date in YYYY-MM-DD HH:MM:SS format
        timezone (str): Timezone to use for calculation

    Returns:
        str: Human readable time until the target date
    """
    tz = ZoneInfo(timezone)
    now = datetime.datetime.now(tz)
    target = datetime.datetime.fromisoformat(target_date).replace(tzinfo=tz)
    diff = target - now

    if diff.total_seconds() < 0:
        return "Target date has passed"

    days = diff.days
    hours, remainder = divmod(diff.seconds, 3600)
    minutes, _ = divmod(remainder, 60)

    return f"{days} days, {hours} hours, {minutes} minutes"


@mcp.tool
def convert_timezone(date_str: str, from_tz: str, to_tz: str) -> str:
    """
    Convert a datetime from one timezone to another.
    Args:
        date_str (str): Date and time in YYYY-MM-DD HH:MM:SS format
        from_tz (str): Source timezone
        to_tz (str): Target timezone

    Returns:
        str: Converted date and time
    """
    dt = datetime.datetime.fromisoformat(date_str)
    dt = dt.replace(tzinfo=ZoneInfo(from_tz))
    converted = dt.astimezone(ZoneInfo(to_tz))
    return converted.strftime("%Y-%m-%d %H:%M:%S %Z")

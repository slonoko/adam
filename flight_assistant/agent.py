from google.adk.agents import Agent
import requests
import logging
from dotenv import load_dotenv
import os

load_dotenv()
logging.basicConfig(level=logging.DEBUG)

headers = {
    "x-rapidapi-key": os.getenv("RAPIDAPI_KEY"),
    "x-rapidapi-host": os.getenv("SKYSCANNER_HOST"),
}

url = f"https://{headers['x-rapidapi-host']}/flights/"

def oneway_flights_month(
    from_airport_code:str="FRA", to_airport_code:str="STR", year_month:str="2025-03"
)-> dict:
    """
    A usefull function that takes as input the source airport code, destination airport code, and the month of the year (format YYYY-MM)
    and returns the flights data in json format. This function is useful to get flights for a specific month.

    Args:
        from_airport_code (str): The source airport code.
        to_airport_code (str): The destination airport code.
        year_month (str): The month of the year in YYYY-MM format.
    Returns:
        dict: The flights data in json format.
    """
    logging.debug(
        f"Searching flights from {from_airport_code} to {to_airport_code} for the month {year_month}"
    )

    querystring = {
        "fromEntityId": from_airport_code,
        "toEntityId": to_airport_code,
        "yearMonth": year_month,
        "currency": "EUR",
    }
    response = requests.get(
        f"{url}price-calendar-web", headers=headers, params=querystring
    )
    return response.json()


def twoway_flights_month(
    from_airport_code:str="FRA",
    to_airport_code:str="STR",
    year_month:str="2025-03",
    return_year_month:str="2025-04",
)-> dict:
    """
    A usefull function that takes as input the source airport code, destination airport code, and the month of the year (format YYYY-MM)
    and returns the flights data in json format. This function is useful to get flights for a specific departure month and returning month.

    Args:
        from_airport_code (str): The source airport code.
        to_airport_code (str): The destination airport code.
        year_month (str): The month of the year in YYYY-MM format.
        return_year_month (str): The return month of the year in YYYY-MM format.
    Returns:
        dict: The flights data in json format.
    """
    logging.debug(
        f"Searching flights from {from_airport_code} to {to_airport_code} for the month {year_month}, and returning on {return_year_month}"
    )

    querystring = {
        "fromEntityId": from_airport_code,
        "toEntityId": to_airport_code,
        "yearMonth": year_month,
        "yearMonthReturn": return_year_month,
        "currency": "EUR",
    }
    response = requests.get(
        f"{url}price-calendar-web-return",
        headers=headers,
        params=querystring,
    )
    return response.json()


def airports_information()-> dict:
    """
    A usefull function that returns the list of airports and their information in json format.

    Args:
        None
    Returns:
        dict: The airports information in json format.
    """
    logging.debug(f"Searching for airports information")

    querystring = {}
    response = requests.get(f"{url}airports", headers=headers, params=querystring)
    return response.json()


def one_way_flight(
    from_airport_code:str="FRA",
    to_airport_code:str="STR",
    depart_date:str="2025-02-14",
    stops:str="direct",
    children:int=0,
    infants:int=0,
    cabinClass:str="economy",
    adults:int=2,
    includeOriginNearbyAirports:bool=False,
    includeDestinationNearbyAirports:bool=False,
    airlines:str="",
)-> dict:
    """
    A usefull function that searches for one way flights for a specific date based on multiple parameters and returns the flights data in json format.
    Important to note that the parameter:
    - cabinClass can take exclusively one of the following values: economy, premium_economy, business, first
    - stops can take one or more of the following values: direct, 1stop, 2stops
    - airlines can be retrieved from response this endpoint(data->filterStats->carriers->id), and It can input multiple values, and the values should be separated by commas. Ex: -32753,-32695,-32677
    - includeOriginNearbyAirports and includeDestinationNearbyAirports can take the values: true, false

    Args:
        from_airport_code (str): The source airport code.
        to_airport_code (str): The destination airport code.
        depart_date (str): The departure date in YYYY-MM-DD format.
        stops (str): The number of stops. Default is "direct".
        children (int): The number of children. Default is 0.
        infants (int): The number of infants. Default is 0.
        cabinClass (str): The cabin class. Default is "economy".
        adults (int): The number of adults. Default is 2.
        includeOriginNearbyAirports (bool): Include nearby airports for origin. Default is False.
        includeDestinationNearbyAirports (bool): Include nearby airports for destination. Default is False.
        airlines (str): The airlines to filter by.
    Returns:
        dict: The flights data in json format.
    """

    logging.debug(
        f"Searching for one way flights from {from_airport_code} to {to_airport_code} for the depart date {depart_date}"
    )

    querystring = {
        "fromEntityId": from_airport_code,
        "toEntityId": to_airport_code,
        "departDate": depart_date,
        "currency": "EUR",
        "stops": stops,
        "children": children,
        "infants": infants,
        "cabinClass": cabinClass,
        "adults": adults,
        "includeOriginNearbyAirports": includeOriginNearbyAirports,
        "includeDestinationNearbyAirports": includeDestinationNearbyAirports,
        "sort": "cheapest_first",
        "airlines": airlines,
    }
    response = requests.get(
        f"{url}search-one-way",
        headers=headers,
        params=querystring,
    )
    return response.json()


def round_trip_flight(
    from_airport_code:str="FRA",
    to_airport_code:str="STR",
    depart_date:str="2025-02-14",
    return_date:str="2025-03-14",
    stops:str="direct",
    children:int=0,
    infants:int=0,
    cabinClass:str="economy",
    adults:int=2,
    includeOriginNearbyAirports:bool=False,
    includeDestinationNearbyAirports:bool=False,
    airlines:str="",
)-> dict:
    """
    A usefull function that searches for round trip flights for specific dates based on multiple parameters and returns the flights data in json format.
    Important to note that the parameter:
    - cabinClass can take exclusively one of the following values: economy, premium_economy, business, first
    - stops can take one or more of the following values: direct, 1stop, 2stops
    - airlines can be retrieved from response this endpoint(data->filterStats->carriers->id), and It can input multiple values, and the values should be separated by commas. Ex: -32753,-32695,-32677
    - includeOriginNearbyAirports and includeDestinationNearbyAirports can take the values: true, false

    Args:
        from_airport_code (str): The source airport code.
        to_airport_code (str): The destination airport code.
        depart_date (str): The departure date in YYYY-MM-DD format.
        return_date (str): The return date in YYYY-MM-DD format.
        stops (str): The number of stops. Default is "direct".
        children (int): The number of children. Default is 0.
        infants (int): The number of infants. Default is 0.
        cabinClass (str): The cabin class. Default is "economy".
        adults (int): The number of adults. Default is 2.
        includeOriginNearbyAirports (bool): Include nearby airports for origin. Default is False.
        includeDestinationNearbyAirports (bool): Include nearby airports for destination. Default is False.
        airlines (str): The airlines to filter by.
    Returns:
        dict: The flights data in json format.
    """

    logging.debug(
        f"Searching for round trip flights from {from_airport_code} to {to_airport_code} for the depart date {depart_date} and returning on {return_date}"
    )

    querystring = {
        "fromEntityId": from_airport_code,
        "toEntityId": to_airport_code,
        "departDate": depart_date,
        "returnDate": return_date,
        "currency": "EUR",
        "stops": stops,
        "children": children,
        "infants": infants,
        "cabinClass": cabinClass,
        "adults": adults,
        "includeOriginNearbyAirports": includeOriginNearbyAirports,
        "includeDestinationNearbyAirports": includeDestinationNearbyAirports,
        "sort": "cheapest_first",
        "airlines": airlines,
    }
    response = requests.get(
        f"{url}search-roundtrip",
        headers=headers,
        params=querystring,
    )
    return response.json()


root_agent = Agent(
    name="flight_assistant_agent",
    model="gemini-2.0-flash-exp",
    description=("Travel assistant Agent to answer questions about flights."),
    instruction=("I can answer your questions about flights."),
    tools=[
        one_way_flight,
        twoway_flights_month,
        airports_information,
        round_trip_flight,
        oneway_flights_month,
    ],
)

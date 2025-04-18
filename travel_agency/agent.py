from google.adk.agents import LlmAgent
from google.adk.tools import agent_tool
import logging
from dotenv import load_dotenv
import sys
from flight_assistant import agent as flight_assistant
from exchange_rate import agent as exchange_rate
from weather_agent import agent as weather_agent
from date_agent import agent as date_agent
from google.adk.tools import load_memory # Tool to query memory

load_dotenv()
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format="%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)", datefmt="%Y-%m-%d %H:%M:%S")


root_agent = LlmAgent(
    name="travel_agency",
    model="gemini-2.0-flash-exp",
    description=("Travel agency assistant. I can help you with flight information, exchange rates, and weather conditions."),
    instruction="You are a travel agency assistant. You can help users with flight information."
                 "You can also help users with exchange rates and weather conditions, using your specialized agents:"
                 "1. Echange rate agent: You can help users with exchange rates."
                 "2. Weather agent: You can help users with weather conditions."
                 "3. Date and time agent: You can help users with getting the current date and time."
                 "Analyze the user's request and delegate it to the appropriate agent.",
    tools=[agent_tool.AgentTool(flight_assistant.root_agent)],
    sub_agents=[exchange_rate.root_agent,weather_agent.root_agent, date_agent.root_agent], # Sub-agents to be used by the root agent
)

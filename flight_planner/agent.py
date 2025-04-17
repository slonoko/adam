from google.adk.agents import LlmAgent
from google.adk.tools import agent_tool
import logging
from dotenv import load_dotenv
import sys
from flight_assistant import agent as flight_assistant
from exchange_rate import agent as exchange_rate
from weather_agent import agent as weather_agent
from google.adk.tools import load_memory # Tool to query memory

load_dotenv()
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format="%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)", datefmt="%Y-%m-%d %H:%M:%S")


root_agent = LlmAgent(
    name="flight_planner_agent",
    model="gemini-2.0-flash-exp",
    description=("Travel planner Agent to answer questions about flights."),
    instruction=("I can answer your questions about flights."),
    tools=[
        agent_tool.AgentTool(agent=flight_assistant.root_agent),
        agent_tool.AgentTool(agent=exchange_rate.root_agent),
        agent_tool.AgentTool(agent=weather_agent.root_agent),
    ],
)

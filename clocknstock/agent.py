from google.adk.agents import LlmAgent
import logging
from dotenv import load_dotenv
import sys
from google.adk.tools import load_memory  # Tool to query memory
from google.adk.models.lite_llm import LiteLlm
from cashanova.agent import root_agent as cashanova_agent
from dailydrip.agent import root_agent as weather_agent
from stockwhisperer.agent import root_agent as stock_agent
from timekeeper.agent import root_agent as time_agent
from google.adk.tools import load_memory  # Tool to query memory
import os
load_dotenv()
logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logging.debug("ClocknStock agent initialized with model: %s", os.getenv("MODEL_NAME", ""))

root_agent = LlmAgent(
    name="ClocknStock",
    model= os.getenv("MODEL_NAME",""), # LiteLlm(model="ollama/gemma3:latest")
    description=(
        "Clock & Stock – Ticking time, trading tips, and thunderous weather 🌤️⏰. "
        "Your all-in-one assistant, I coordinate with specialized agents to provide "
        "real-time stock data via the stockwhisperer agent, weather updates via the dailydrip agent, currency exchange via the cashanova agent, and current time information via timekeeper agent. "
        
    ),
    instruction=(
        "You are a multi-functional assistant. "
        "You can retrieve stock data, weather updates, currency exchange rates, and current time information. "
        "You will coordinate with specialized agents to provide these services. "
    ),
    tools=[load_memory],
    sub_agents=[
        cashanova_agent,
        weather_agent,
        stock_agent,
        time_agent 
    ]
)
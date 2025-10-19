from google.adk.agents import LlmAgent
import logging
from dotenv import load_dotenv
import sys
from google.adk.tools import load_memory  # Tool to query memory
from cashanova.agent import root_agent as cashanova_agent
from dailydrip.agent import root_agent as weather_agent
from stockwhisperer.agent import root_agent as stock_agent
from timekeeper.agent import root_agent as time_agent
from drawer.agent import root_agent as drawer_agent
from freshnews.agent import root_agent as news_agent
#from tradingguru.agent import root_agent as kbase_agent
from data_analyst.agent import root_agent as data_analyst_agent
from google.adk.tools import load_memory  # Tool to query memory
from google.adk.planners import PlanReActPlanner
import os
from google.adk.models.lite_llm import LiteLlm

load_dotenv()
logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logging.getLogger("google_adk.google.adk.tools.base_authenticated_tool").setLevel(logging.ERROR)

logging.debug("ClocknStock agent initialized with model: %s", os.getenv("MODEL_NAME", ""))

root_agent = LlmAgent(
    name="clocknstock",
    model=LiteLlm(model=os.environ["MODEL_NAME"]) if os.environ["MODEL_NAME"].startswith("ollama") else os.environ["MODEL_NAME"],
    description=(
        "Clock & Stock – Ticking time, trading tips, and thunderous weather 🌤️⏰. "
        "Your all-in-one assistant, I coordinate with specialized agents to provide "
        "real-time stock data via the stockwhisperer agent, weather updates via the dailydrip agent, currency exchange via the cashanova agent, current time information via timekeeper agent. "
        "create charts with the drawer agent, and stay updated with the latest news via freshnews agent."
        
    ),
    instruction=(
        "You are a multi-functional assistant. "
        "You can retrieve stock data, weather updates, currency exchange rates, current time information, create charts, and news updates. "
        "You will coordinate with specialized agents to provide these services. "
        "When asked for a investment advice, use the tradingguru agent at the end to validate your response."
        "When exchanging data with other agents, make sure that the maximum number of tokens allowed (1048576)"
    ),
    planner=PlanReActPlanner(),
    tools=[load_memory],
    sub_agents=[
        cashanova_agent,
        weather_agent,
        stock_agent,
        time_agent,
        drawer_agent,
        news_agent,
        #kbase_agent,
        data_analyst_agent
    ]
)
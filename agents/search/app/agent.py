from google.adk.agents import LlmAgent
import logging
from dotenv import load_dotenv
import sys
import os
from google.adk.tools import google_search
from . import prompt

load_dotenv()

logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)",
    datefmt="%Y-%m-%d %H:%M:%S",
)

root_agent = LlmAgent(
    name="data_analyst_agent",
    model=os.getenv("MODEL_NAME", ""),
    description=("The Data Analyst – Your personal assistant for data analysis 📊. "
                 "It provides insights and information about market trends, "
                 "and can help you analyze stock performance and financial data."
                 
    ),
    instruction=prompt.DATA_ANALYST_PROMPT,
    tools=[google_search],
)

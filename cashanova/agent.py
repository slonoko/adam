from google.adk.agents import LlmAgent
import logging
from dotenv import load_dotenv
import sys
from google.adk.tools import load_memory  # Tool to query memory
from tools.exchange_rate import convert, get_exchange_rates
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import SseConnectionParams
import os

load_dotenv()
logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logging.debug("Cashanova agent initialized with model: %s", os.getenv("MODEL_NAME", ""))

root_agent = LlmAgent(
    name="Cashanova",
    model=os.getenv("MODEL_NAME", ""), # LiteLlm(model="ollama/gemma3n:latest")
    description=(
        "Smooth with the money 💸. "
        "Can retrieve exchange rates, and convert from one currency to another."
    ),
    instruction=(
        "You are a financial assistant. "
        "You can retrieve exchange rates and convert from one currency to another. "
    ),
    tools=[MCPToolset(connection_params=SseConnectionParams(url="http://localhost:8001/cashanova/sse"))],
)
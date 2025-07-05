from google.adk.agents import LlmAgent
import logging
from dotenv import load_dotenv
import sys
from google.adk.tools import load_memory  # Tool to query memory
from tools.exchange_rate import convert, get_exchange_rates
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import SseConnectionParams

load_dotenv()
logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)",
    datefmt="%Y-%m-%d %H:%M:%S",
)


root_agent = LlmAgent(
    name="Cashanova",
    model="gemini-2.5-flash-preview-04-17", # LiteLlm(model="ollama/gemma3n:latest")
    description=(
        "Smooth with the money 💸. "
        "Can retrieve exchange rates, and convert from one currency to another."
    ),
    tools=[MCPToolset(connection_params=SseConnectionParams(url="http://localhost:8001/cashanova/sse"), tool_filter=["get_exchange_rate","convert_currency"])],
)
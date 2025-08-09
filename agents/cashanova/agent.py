from google.adk.agents import LlmAgent
import logging
from dotenv import load_dotenv
import sys
from google.adk.tools import load_memory  # Tool to query memory
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams
import os

load_dotenv()
logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logging.debug("Cashanova agent initialized with model: %s", os.getenv("MODEL_NAME", ""))

def custom_tool_filter(tool, readonly_context=None):
    tool_name = tool.name if hasattr(tool, 'name') else str(tool)
    logging.info(f"Looking for {tool}")
    return tool_name.startswith("c_")

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
    tools=[MCPToolset(connection_params=StreamableHTTPConnectionParams(url=f"{os.getenv('mcp_server_url')}/mcp"), tool_filter=custom_tool_filter)],
)
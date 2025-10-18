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
logging.getLogger("google_adk.google.adk.tools.base_authenticated_tool").setLevel(logging.ERROR)

def custom_tool_filter(tool, readonly_context=None):
    tool_name = tool.name if hasattr(tool, 'name') else str(tool)
    logging.info(f"Looking for {tool}")
    return tool_name.startswith("d_")


root_agent = LlmAgent(
    name="DailyDrip",
    model=os.getenv("MODEL_NAME", ""),
    description=("The Daily Drip – For that slow, steady weather tea"
                 " that keeps you informed and ready for the day ahead."
                 " It provides daily weather updates, forecasts, and current conditions"
                 " to help you plan your day with confidence."
    ),
    instruction=(
        "You are a weather assistant. "
        "You can provide daily weather updates, forecasts, and current conditions. "
        "You will use specialized tools to retrieve this information."
    ),
    tools=[MCPToolset(connection_params=StreamableHTTPConnectionParams(url=f"{os.getenv('mcp_server_url')}/mcp"), tool_filter=custom_tool_filter)],
)

from google.adk.agents import LlmAgent
import logging
from dotenv import load_dotenv
import sys
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams
import os

load_dotenv()

def custom_tool_filter(tool, readonly_context=None):
    tool_name = tool.name if hasattr(tool, 'name') else str(tool)
    logging.info(f"Looking for {tool}")
    return tool_name.startswith("cs_")

logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logging.getLogger("google_adk.google.adk.tools.base_authenticated_tool").setLevel(logging.ERROR)

root_agent = LlmAgent(
    name="tradingguru",
    model=os.getenv("MODEL_NAME", ""),
    description=("The Trading Guru – Your personal assistant for trading insights 📈🤖. "
                 "It helps you find and retrieve information from various trading corpora."
    ),
    instruction=("Use the tools provided to search and retrieve information from the trading corpora."),
    tools=[MCPToolset(connection_params=StreamableHTTPConnectionParams(url=f"{os.getenv('mcp_server_url')}/mcp"), tool_filter=custom_tool_filter)],
)

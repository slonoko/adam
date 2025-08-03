from google.adk.agents import LlmAgent
import logging
from dotenv import load_dotenv
import sys
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

root_agent = LlmAgent(
    name="tradingguru",
    model=os.getenv("MODEL_NAME", ""),
    description=("The Trading Guru – Your personal assistant for trading insights 📈🤖. "
                 "It helps you find and retrieve information from various trading corpora."
    ),
    instruction=("Use the tools provided to search and retrieve information from the trading corpora."),
    tools=[MCPToolset(connection_params=SseConnectionParams(url=f"{os.getenv('mcp_server_url')}/corpora_search/sse"))],
)

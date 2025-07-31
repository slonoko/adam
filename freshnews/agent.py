from google.adk.agents import LlmAgent
import logging
from dotenv import load_dotenv
import sys
from tools.stocks_data import *
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


root_agent = LlmAgent(
    name="freshnews",
    model=os.getenv("MODEL_NAME", ""),
    description=(
        "FreshNews is your go-to source for the latest news and insights. "
        "Stay updated with real-time information from various domains, including technology, health, and finance. "
        "Whether you're looking for breaking news, in-depth analysis, or personalized content, FreshNews has you covered."
    ),
    instruction=(
        "You are a news assistant. "
        "You can provide real-time news updates, article summaries, and personalized content recommendations. "
        "When asked about current events, trends, or specific topics, use the tools available to fetch the latest information. "
    ),
    tools=[MCPToolset(connection_params=SseConnectionParams(url="http://localhost:8001/news/sse"))],
)

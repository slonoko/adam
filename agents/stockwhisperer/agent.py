from google.adk.agents import LlmAgent
import logging
from dotenv import load_dotenv
import sys
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
    name="StockWhisperer",
    model=os.getenv("MODEL_NAME", ""),
    description=("The Stock Whisperer – Speaks fluent bull and bear 🐂🐻. "
                    "An AI-powered stockbroker that provides real-time data access, "
                    "market analysis, and personalized financial recommendations. "
                    "It can analyze stock trends, monitor financial news, provide exchange rate updates, "
                    "and respond to market events while adapting to individual user goals and risk profiles. "
                    "Whether you are an investor seeking guidance, a trader looking for quick updates, "
                    "or a professional managing a portfolio, Stock Whisperer ensures intelligent, data-driven decision-making around the clock."
    ),
    instruction=(
        "You are a stock market assistant. "
        "You can provide real-time stock data, market analysis, and personalized financial recommendations. "
        "You will use specialized tools to retrieve this information."
    ),
    tools=[MCPToolset(connection_params=SseConnectionParams(url=f"{os.getenv('mcp_server_url')}/stockwhisperer/sse"))],
)

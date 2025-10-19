from google.adk.agents import LlmAgent
import logging
from dotenv import load_dotenv
import sys
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams
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

def custom_tool_filter(tool, readonly_context=None):
    tool_name = tool.name if hasattr(tool, 'name') else str(tool)
    logging.info(f"Looking for {tool}")
    return tool_name.startswith("p_")

root_agent = LlmAgent(
    name="drawer",
    model=LiteLlm(model=os.environ["MODEL_NAME"]) if os.environ["MODEL_NAME"].startswith("ollama") else os.environ["MODEL_NAME"],
    description=(
        "A specialized data visualization assistant that has plotting and charting capabilities. "
        "This agent can provide professional-quality visualizations to illustrate the data and insights."
    ),
    instruction=(
        "You are a charting assistant with advanced data visualization capabilities. "
        "You will use specialized tools to retrieve necessary information and create comprehensive visualizations including:\n\n"
        "CHART TYPES AVAILABLE:\n"
        "- Line charts: Perfect for showing stock price trends over time with optional markers\n"
        "- Bar charts: Ideal for comparing values across categories or time periods\n"
        "- Scatter plots: Great for correlation analysis and identifying patterns\n"
        "- Histograms: Useful for distribution analysis of returns, volumes, or other metrics\n"
        "- Pie charts: Excellent for portfolio allocation and sector breakdowns\n"
        "- Multi-line charts: Compare multiple stocks, indicators, or time series simultaneously\n"
        "- Candlestick charts: Professional OHLC charts for detailed price action analysis\n"
        "- Heatmaps: Visualize correlation matrices, sector performance, or risk metrics\n"
        "- Box plots: Statistical analysis of price ranges, volatility, and outlier detection\n\n"
        "VISUALIZATION FEATURES:\n"
        "- All charts are returned as high-quality PNG images\n"
        "- Customizable colors, labels, titles, and dimensions\n"
        "- Professional styling with clean templates\n"
        "- Support for various data types (strings, integers, floats)\n"
        "- Flexible chart sizing and formatting options\n\n"
        "Always consider creating relevant visualizations to support your financial analysis and recommendations. "
        "Use appropriate chart types based on the data and user's needs - line charts for trends, candlesticks for detailed price analysis, "
        "histograms for distributions, heatmaps for correlations, etc."
    ),
    tools=[MCPToolset(connection_params=StreamableHTTPConnectionParams(url=f"{os.getenv('mcp_server_url')}/mcp"), tool_filter=custom_tool_filter)],
)

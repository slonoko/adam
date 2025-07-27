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
    name="drawer",
    model=os.getenv("MODEL_NAME", ""),
    description=(
        "A specialized data visualization assistant that combines financial analysis with advanced charting capabilities. "
        "This agent can provide professional-quality visualizations to illustrate the data and insights."
    ),
    instruction=(
        "You are a stock market assistant with advanced data visualization capabilities. "
        "You can provide real-time stock data, market analysis, and personalized financial recommendations. "
        "You will use specialized tools to retrieve this information and create comprehensive visualizations including:\n\n"
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
    tools=[MCPToolset(connection_params=SseConnectionParams(url="http://localhost:8001/plotter/sse"))],
)

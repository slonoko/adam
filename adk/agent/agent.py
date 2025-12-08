from google.adk.agents import LlmAgent, Agent
import logging
from dotenv import load_dotenv
import sys
from google.adk.tools.load_memory_tool import load_memory  # Tool to query memory
from google.adk.planners import PlanReActPlanner
import os
from google.adk.models.lite_llm import LiteLlm
import warnings
from agent import instructions
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams
from google.adk.tools.google_search_agent_tool import create_google_search_agent, GoogleSearchAgentTool
from google.adk.tools import load_web_page
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from google.adk.tools.agent_tool import AgentTool

load_dotenv()
logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logging.getLogger("google_adk.google.adk.tools.base_authenticated_tool").setLevel(logging.ERROR)

logging.debug("ClocknStock agent initialized with model: %s", os.getenv("MODEL_NAME", ""))

# Suppress Pydantic validation for arbitrary types used internally
warnings.filterwarnings("ignore", category=DeprecationWarning)

def get_model():
    """Helper function to get the appropriate model based on MODEL_NAME environment variable."""
    model_name = os.environ["MODEL_NAME"]
    return LiteLlm(model=model_name) if model_name.startswith("ollama") else model_name

broker_agent = LlmAgent(
    name="ExchangeRateAgent",
    model=get_model(),
    description=(instructions.CASHANOVA_DESCRIPTION),
    instruction=(instructions.CASHANOVA_INSTRUCTION),
    tools=[MCPToolset(connection_params=StreamableHTTPConnectionParams(url=f"{os.getenv('mcp_server_url')}/mcp"), tool_filter=lambda tool,readonly_context: tool.name.startswith("c_") if hasattr(tool, 'name') else str(tool).startswith("c_")),load_memory],
)

weather_agent = LlmAgent(
    name="WeatherAgent",
    model=get_model(),
    description=(instructions.DAILYDRIP_DESCRIPTION),
    instruction=(instructions.DAILYDRIP_INSTRUCTION),
    tools=[MCPToolset(connection_params=StreamableHTTPConnectionParams(url=f"{os.getenv('mcp_server_url')}/mcp"), tool_filter=lambda tool,readonly_context: tool.name.startswith("d_") if hasattr(tool, 'name') else str(tool).startswith("d_")),load_memory],
)

stock_agent = LlmAgent(
    name="StockAgent",
    model=get_model(),
    description=(instructions.STOCKWHISPERER_DESCRIPTION),
    instruction=(instructions.STOCKWHISPERER_INSTRUCTION),
    tools=[MCPToolset(connection_params=StreamableHTTPConnectionParams(url=f"{os.getenv('mcp_server_url')}/mcp"), tool_filter=lambda tool,readonly_context: tool.name.startswith("s_") if hasattr(tool, 'name') else str(tool).startswith("s_")),load_memory],
)

time_agent = LlmAgent(
    name="TimeAgent",
    model=get_model(),
    description=(instructions.TIMEKEEPER_DESCRIPTION),
    instruction=(instructions.TIMEKEEPER_INSTRUCTION),
    tools=[MCPToolset(connection_params=StreamableHTTPConnectionParams(url=f"{os.getenv('mcp_server_url')}/mcp"), tool_filter=lambda tool,readonly_context: tool.name.startswith("t_") if hasattr(tool, 'name') else str(tool).startswith("t_")),load_memory],
)

google_search_agent = create_google_search_agent(get_model())
google_search_tool = GoogleSearchAgentTool(google_search_agent)

news_agent = LlmAgent(
    name="NewsAgent",
    model=get_model(),
    description=(instructions.FRESHNEWS_DESCRIPTION),
    instruction=(instructions.FRESHNEWS_INSTRUCTION),
    tools=[google_search_tool, MCPToolset(connection_params=StreamableHTTPConnectionParams(url=f"{os.getenv('mcp_server_url')}/mcp"), tool_filter=lambda tool,readonly_context: tool.name.startswith("n_") if hasattr(tool, 'name') else str(tool).startswith("n_")),load_memory],
)

root_agent = Agent(
    name="MrKnowItAll",
    model=get_model(),
    description=(instructions.CLOCKNSTOCK_DESCRIPTION),
    instruction=(instructions.CLOCKNSTOCK_INSTRUCTION),
    planner=PlanReActPlanner(),
    tools=[load_memory, AgentTool(agent=broker_agent), AgentTool(agent=weather_agent), AgentTool(agent=stock_agent), AgentTool(agent=time_agent), AgentTool(agent=news_agent)],
)

a2a_app = to_a2a(root_agent, port=8002)
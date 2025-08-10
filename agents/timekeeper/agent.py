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
    return tool_name.startswith("t_")
logging.getLogger("google_adk.google.adk.tools.base_authenticated_tool").setLevel(logging.ERROR)

logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)",
    datefmt="%Y-%m-%d %H:%M:%S",
)

root_agent = LlmAgent(
    name="Timekeeper",
    model=os.getenv("MODEL_NAME", ""),
    description=("The Timekeeper – Your personal assistant for time 🌤️⏰. "
                 "It provides current date and time information, "
                 "and can help you manage your schedule and reminders."
                 
    ),
    instruction=(
        "You are a time management assistant. "
        "You can provide current date and time information, "
        "and help manage schedules and reminders. "
        "and use the tool if certain words are mentioned in the user input, such as today, tomorrow, yesterday, now, current time, current date, schedule, reminder, etc. "
    ),
    tools=[MCPToolset(errlog=None,connection_params=StreamableHTTPConnectionParams(url=f"{os.getenv('mcp_server_url')}/mcp"), tool_filter=custom_tool_filter)], # type: ignore
)

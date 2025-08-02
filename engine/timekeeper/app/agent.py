from google.adk.agents import LlmAgent
import logging
from dotenv import load_dotenv
import sys
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import SseConnectionParams, SseServerParams
import os

load_dotenv()

logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)",
    datefmt="%Y-%m-%d %H:%M:%S",
)

root_agent = LlmAgent(
    name="Timekeeper",
    model=os.getenv("MODEL_NAME", "gemini-2.5-flash"),
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
    tools=[MCPToolset(connection_params=SseConnectionParams(url=f"{os.getenv('mcp_server_url')}/timekeeper/sse"), errlog=None)])
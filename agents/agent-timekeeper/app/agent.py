import os

import google.auth
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams
import logging
from dotenv import load_dotenv
import sys
from google.adk.auth.auth_credential import (
    AuthCredentialTypes,
    HttpAuth,
    HttpCredentials,
    AuthCredential
)
import google.auth.transport.requests
import google.oauth2.id_token
from fastapi.openapi.models import HTTPBearer


_, project_id = google.auth.default()
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "us-central1")
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")

load_dotenv()

logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def custom_tool_filter(tool, readonly_context=None):
    tool_name = tool.name if hasattr(tool, "name") else str(tool)
    logging.info(f"Looking for {tool}")
    return tool_name.startswith("t_")


def make_authorized_get_request(audience):
    auth_req = google.auth.transport.requests.Request()
    id_token = google.oauth2.id_token.fetch_id_token(auth_req, audience)

    return id_token


id_token = make_authorized_get_request(
    "https://mcp-server-186919647719.us-central1.run.app/"
)
auth_cred = AuthCredential(
    auth_type=AuthCredentialTypes.HTTP,
    http=HttpAuth(
        scheme="bearer",
        credentials=HttpCredentials(token=id_token),
    ),
)

tool = MCPToolset(
    auth_scheme=HTTPBearer(),
    auth_credential=auth_cred,
    errlog=None,
    connection_params=StreamableHTTPConnectionParams(
        url=f"{os.getenv('mcp_server_url')}/mcp/",
        headers={"Authorization": f"Bearer {id_token}"}
    ),
    tool_filter=custom_tool_filter,
)

root_agent = LlmAgent(
    name="Timekeeper",
    model=os.getenv("MODEL_NAME", ""),
    description=(
        "The Timekeeper – Your personal assistant for time 🌤️⏰. "
        "It provides current date and time information, "
        "and can help you manage your schedule and reminders."
    ),
    instruction=(
        "You are a time management assistant. "
        "You can provide current date and time information, "
        "and help manage schedules and reminders. "
        "and use the tool if certain words are mentioned in the user input, such as today, tomorrow, yesterday, now, current time, current date, schedule, reminder, etc. "
    ),
    tools=[tool],
)
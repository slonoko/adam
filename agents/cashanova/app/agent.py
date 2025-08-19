from google.adk.agents import LlmAgent
import logging
from dotenv import load_dotenv
import sys
from google.adk.tools import load_memory  # Tool to query memory
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams
import os
import google.auth
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
                      
load_dotenv()
logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logging.getLogger("google_adk.google.adk.tools.base_authenticated_tool").setLevel(logging.ERROR)

logging.debug("Cashanova agent initialized with model: %s", os.getenv("MODEL_NAME", ""))

def custom_tool_filter(tool, readonly_context=None):
    tool_name = tool.name if hasattr(tool, 'name') else str(tool)
    logging.info(f"Looking for {tool}")
    return tool_name.startswith("c_")


def make_authorized_get_request(audience):
    auth_req = google.auth.transport.requests.Request()
    id_token = google.oauth2.id_token.fetch_id_token(auth_req, audience)

    return id_token


id_token = make_authorized_get_request(
    os.environ.get("mcp_server_url")
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
    name="Cashanova",
    model=os.getenv("MODEL_NAME", ""), # LiteLlm(model="ollama/gemma3n:latest")
    description=(
        "Smooth with the money 💸. "
        "Can retrieve exchange rates, and convert from one currency to another."
    ),
    instruction=(
        "You are a financial assistant. "
        "You can retrieve exchange rates and convert from one currency to another. "
    ),
    tools=[tool],
)
# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
import os
from zoneinfo import ZoneInfo

import google.auth
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams
import logging
from dotenv import load_dotenv
import sys
from google import auth as google_auth
from google.auth.transport import requests as google_requests
import requests
import json
from google.adk.auth.auth_credential import (
    AuthCredentialTypes,
    HttpAuth,
    HttpCredentials,
    AuthCredential,
)

_, project_id = google.auth.default()
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "us-central1")
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")

load_dotenv()


def get_identity_token():
    credentials, _ = google_auth.default()
    auth_request = google_requests.Request()
    credentials.refresh(auth_request)
    return credentials.token


def custom_tool_filter(tool, readonly_context=None):
    tool_name = tool.name if hasattr(tool, "name") else str(tool)
    logging.info(f"Looking for {tool}")
    return tool_name.startswith("t_")


logging.getLogger("google_adk.google.adk.tools.base_authenticated_tool").setLevel(
    logging.ERROR
)

logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)",
    datefmt="%Y-%m-%d %H:%M:%S",
)

auth_cred = AuthCredential(
    auth_type=AuthCredentialTypes.HTTP,
    http=HttpAuth(
        scheme="bearer",
        credentials=HttpCredentials(token=get_identity_token()),
    ),
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
    tools=[MCPToolset(auth_credential=auth_cred, errlog=None, connection_params=StreamableHTTPConnectionParams(url=f"{os.getenv('mcp_server_url')}/mcp"), tool_filter=custom_tool_filter)],  # type: ignore
)

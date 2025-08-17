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
    AuthCredential,ServiceAccount, ServiceAccountCredential
)
from google.adk.tools.openapi_tool.auth.auth_helpers import service_account_scheme_credential
import json
from google.auth import crypt, jwt
import time
from google.auth import compute_engine

#_, project_id = google.auth.default()
# os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)
# os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "us-central1")
# os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")

load_dotenv()

logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)",
    datefmt="%Y-%m-%d %H:%M:%S",
)

def get_sa_token():
    credentials, _ = google_auth.load_credentials_from_file("/home/elie/Projects/adam/agents/agent-timekeeper/adam-sa.json",scopes=["https://www.googleapis.com/auth/cloud-platform"])
    auth_request = google_requests.Request()
    credentials.refresh(auth_request)
    return credentials.token

def get_identity_token():
  credentials, _ = google_auth.default()
  auth_request = google_requests.Request()
  credentials.refresh(auth_request)
  
  return credentials.token

def custom_tool_filter(tool, readonly_context=None):
    tool_name = tool.name if hasattr(tool, "name") else str(tool)
    logging.info(f"Looking for {tool}")
    return tool_name.startswith("t_")

def generate_jwt(
    sa_keyfile = "/home/elie/Projects/adam/agents/agent-timekeeper/adam-sa.json",
    sa_email="adam-agent@assistant-424508.iam.gserviceaccount.com",
    audience="mcp-server-186919647719.us-central1.run.app",
    expiry_length=3600,
):
    """Generates a signed JSON Web Token using a Google API Service Account."""

    now = int(time.time())

    # build payload
    payload = {
        "iat": now,
        # expires after 'expiry_length' seconds.
        "exp": now + expiry_length,
        # iss must match 'issuer' in the security configuration in your
        # swagger spec (e.g. service account email). It can be any string.
        "iss": "https://accounts.google.com",
        # aud must be either your Endpoints service name, or match the value
        # specified as the 'x-google-audience' in the OpenAPI document.
        "aud": audience,
        # sub and email should match the service account's email address
        "sub": sa_email,
    }

    # sign with keyfile
    signer = crypt.RSASigner.from_service_account_file(sa_keyfile)
    output = jwt.encode(signer, payload)

    return output

with open("/home/elie/Projects/adam/agents/agent-timekeeper/adam-sa.json") as f:
    d = json.load(f)
    sa_cred = ServiceAccountCredential.model_validate_json(json.dumps(d))

sa = ServiceAccount(service_account_credential=sa_cred, scopes=["https://www.googleapis.com/auth/cloud-platform"])
auth_scheme, auth_cred = service_account_scheme_credential(sa)

# auth_cred = AuthCredential(
#     auth_type=AuthCredentialTypes.SERVICE_ACCOUNT,
#     service_account=ServiceAccount(service_account_credential=sa_cred, scopes=["https://www.googleapis.com/auth/cloud-platform"], use_default_credential=True), 
#     # http=HttpAuth(
#     #     scheme="bearer",
#     #     credentials=HttpCredentials(token=get_identity_token()),
#     # ),
# )

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
    tools=[MCPToolset(auth_scheme=auth_scheme, auth_credential=auth_cred, errlog=sys.stderr, connection_params=StreamableHTTPConnectionParams(url=f"{os.getenv('mcp_server_url')}/mcp"), tool_filter=custom_tool_filter)],  # type: ignore
)
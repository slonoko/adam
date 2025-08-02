import logging
import vertexai
from vertexai import agent_engines

PROJECT_ID = "assistant-424508"
LOCATION = "us-central1"

vertexai.init(
    project=PROJECT_ID,
    location=LOCATION,
)

remote_app = agent_engines.get("projects/assistant-424508/locations/us-central1/reasoningEngines/440851386180042752")
remote_session = remote_app.list_sessions(user_id="user-12345")
print("Remote session created:", remote_session)

events =remote_app.stream_query(
    user_id="u_456",
    session_id=remote_session["sessions"][0]["id"],
    message="what is the current time in Stuttgart?",
)

# Print responses
for event in events:
    for part in event["content"]["parts"]:
        if "text" in part:
            response_text = part["text"]
            print("[remote response]", response_text)
            logging.info("[remote response] " + response_text)
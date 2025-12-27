from google.adk.agents.remote_a2a_agent import AGENT_CARD_WELL_KNOWN_PATH
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
from google.adk.runners import Runner
from google.genai.types import Content, Part
import uuid
from google.adk.sessions.sqlite_session_service import SqliteSessionService
from google.adk.memory import InMemoryMemoryService
import asyncio
import logging
from dotenv import load_dotenv
import sys
from google.adk.tools.load_memory_tool import load_memory  # Tool to query memory
import os
import warnings

load_dotenv()

logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logging.getLogger("google_adk.google.adk.tools.base_authenticated_tool").setLevel(logging.ERROR)

logging.debug("ClocknStock agent initialized with model: %s", os.getenv("MODEL_NAME", ""))
logger = logging.getLogger(__name__)

# Suppress Pydantic validation for arbitrary types used internally
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Services must be shared across runners to share state and memory
session_service = SqliteSessionService("session.db")
memory_service = InMemoryMemoryService() # Use in-memory for demo

root_agent = RemoteA2aAgent(
    name='trading_advisor',
    description='A helpful assistant for user questions.',
    agent_card=(
        f"http://localhost:8000/{AGENT_CARD_WELL_KNOWN_PATH}"
    ),
)

async def run():
    runner = Runner(agent=root_agent,
                    app_name="TradingAdvisor",
                    session_service=session_service,
                    memory_service=memory_service)
    session_id = str(uuid.uuid4())
    await runner.session_service.create_session(app_name="TradingAdvisor", user_id="elie", session_id=session_id)
    user_input = Content(parts=[Part(text="What is the current value of nvidia in euros?")])
    async for event in runner.run_async(user_id="elie", session_id=session_id, new_message=user_input):
        if event.is_final_response() and event.content and event.content.parts:
            final_response_text = event.content.parts[0].text
    print(f"Agent 1 Response: {final_response_text}")
    completed_session = await runner.session_service.get_session(app_name="TradingAdvisor", user_id="elie", session_id=session_id)
    await memory_service.add_session_to_memory(completed_session)

# asyncio.run(run())
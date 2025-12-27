from google.adk.agents.remote_a2a_agent import AGENT_CARD_WELL_KNOWN_PATH
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
from google.adk.runners import Runner
from google.genai.types import Content, Part
import uuid
from google.adk.sessions.sqlite_session_service import SqliteSessionService, Session
from agent.utils.vertex_ai_rag_memory_service import FixedVertexAiRagMemoryService
import asyncio
import logging
from dotenv import load_dotenv
import sys
from google.adk.tools.load_memory_tool import load_memory  # Tool to query memory
import os
import warnings
import vertexai
from google.adk.tools.preload_memory_tool import PreloadMemoryTool
load_dotenv()

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logging.getLogger("google_adk.google.adk.tools.base_authenticated_tool").setLevel(logging.ERROR)

logging.debug("ClocknStock agent initialized with model: %s", os.getenv("MODEL_NAME", ""))
logger = logging.getLogger(__name__)

# Suppress Pydantic validation for arbitrary types used internally
warnings.filterwarnings("ignore", category=DeprecationWarning)

vertexai.init()

# Services must be shared across runners to share state and memory
session_service = SqliteSessionService("session.db")
memory_service = FixedVertexAiRagMemoryService(f"projects/{os.getenv("GOOGLE_CLOUD_PROJECT")}/locations/{os.getenv("GOOGLE_CLOUD_REGION")}/ragCorpora/2305843009213693952")

async def auto_save_session_to_memory_callback(callback_context):
    await callback_context._invocation_context.memory_service.add_session_to_memory(
        callback_context._invocation_context.session)
    
root_agent = RemoteA2aAgent(
    name='trading_advisor',
    description='A helpful assistant for user questions.',
    agent_card=(
        f"http://localhost:8000/{AGENT_CARD_WELL_KNOWN_PATH}"
    ),
    after_agent_callback=auto_save_session_to_memory_callback,
)

APP_NAME = "TradingAdvisor"
USER_ID = "elie"

async def run():
    runner = Runner(agent=root_agent,
                    app_name=APP_NAME,
                    session_service=session_service,
                    memory_service=memory_service)
    q = input("Q: ")
    user_input = Content(parts=[Part(text=q)])
    session:Session = await runner.session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=str(uuid.uuid4()))
    async for event in runner.run_async(user_id=USER_ID, session_id=session.id, new_message=user_input):
        if event.is_final_response() and event.content and event.content.parts:
            final_response_text = event.content.parts[0].text
    logger.info(f"Agent response: {final_response_text}")
    completed_session = await runner.session_service.get_session(app_name=APP_NAME, user_id=USER_ID, session_id=session.id)
    await memory_service.add_session_to_memory(completed_session)

#asyncio.run(run())
from google.adk.agents import LlmAgent
import logging
from dotenv import load_dotenv
import sys
import os
from google.adk.models.lite_llm import LiteLlm
import warnings
from code_agent import instructions
from google.adk.code_executors.container_code_executor import ContainerCodeExecutor
from google.adk.a2a.utils.agent_to_a2a import to_a2a
import vertexai

load_dotenv()

vertexai.init()

logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logging.getLogger("google_adk.google.adk.tools.base_authenticated_tool").setLevel(logging.ERROR)

logging.debug("Code agent initialized with model: %s", os.getenv("MODEL_NAME", ""))
logger = logging.getLogger(__name__)

# Suppress Pydantic validation for arbitrary types used internally
warnings.filterwarnings("ignore", category=DeprecationWarning)

def get_model():
    """Helper function to get the appropriate model based on MODEL_NAME environment variable."""
    model_name = os.environ["MODEL_NAME"]
    return LiteLlm(model=model_name) if model_name.startswith("ollama") else model_name

async def auto_save_session_to_memory_callback(callback_context):
    await callback_context._invocation_context.memory_service.add_session_to_memory(
        callback_context._invocation_context.session)
    
root_agent = LlmAgent(
    name="CodeAgent",
    model=get_model(),
    code_executor=ContainerCodeExecutor(image="python:3.13-alpine"),
    instruction=instructions.DRAWER_INSTRUCTION,
    description=instructions.DRAWER_DESCRIPTION,
    after_agent_callback=auto_save_session_to_memory_callback
)

a2a_app = to_a2a(root_agent)

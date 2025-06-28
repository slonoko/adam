from google.adk.agents import LlmAgent
import logging
from dotenv import load_dotenv
import sys
from tools.datetime import current_date_and_time
from google.adk.models.lite_llm import LiteLlm

load_dotenv()
logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)",
    datefmt="%Y-%m-%d %H:%M:%S",
)


root_agent = LlmAgent(
    name="Timekeeper",
    model="gemini-2.5-flash-preview-04-17",
    description=("The Timekeeper – Your personal assistant for time 🌤️⏰. "
                 "It provides current date and time information, "
                 "and can help you manage your schedule and reminders."
                 
    ),
    tools=[
        current_date_and_time,
    ],  # Tool to query memory
)

from vertexai import agent_engines
import asyncio
from dotenv import load_dotenv
from vertexai.agent_engines._agent_engines import AgentEngine

load_dotenv()

adk_app:AgentEngine = agent_engines.get("3842546848472498176")

agent_engines.list()

def query():
    for event in adk_app.stream_query(
        user_id="elie",
        session_id="498147486859264000",
        message="convert 100 usd to euros?",
    ):
        print(event)

# session = asyncio.run(adk_app.async_create_session(user_id="elie"))
# session = asyncio.run(adk_app.async_get_session(user_id="elie", session_id="8868087394327330816"))

query()
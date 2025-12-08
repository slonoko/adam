from google.adk.agents.remote_a2a_agent import AGENT_CARD_WELL_KNOWN_PATH
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
from agent import instructions

root_agent = RemoteA2aAgent(
    name="MrKnowItAll",
    description=(instructions.CLOCKNSTOCK_DESCRIPTION),
    agent_card=f"http://localhost:8002/{AGENT_CARD_WELL_KNOWN_PATH}",
)
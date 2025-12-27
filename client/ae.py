import vertexai
from dotenv import load_dotenv

load_dotenv()

vertexai.init()

client = vertexai.Client()
agent_engine = client.agent_engines.create()

# Optionally, print out the Agent Engine resource name. You will need the
# resource name to interact with your Agent Engine instance later on.
print(agent_engine.api_resource.name)
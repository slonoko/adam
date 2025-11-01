from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
import os
import logging
import sys
from dataclasses import dataclass
from langchain.tools import tool, ToolRuntime
from langgraph.checkpoint.memory import InMemorySaver
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_core.messages import HumanMessage
import asyncio

load_dotenv()  # Load environment variables from .env file
logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)",
)
logging.getLogger("google_adk.google.adk.tools.base_authenticated_tool").setLevel(logging.ERROR)

logging.debug("Agent initialized with model: %s", os.getenv("MODEL_NAME", ""))

llm = ChatGoogleGenerativeAI(
    model=os.getenv("MODEL_NAME"),
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.7
)

# llm = AzureChatOpenAI(
#     azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
# )

SYSTEM_PROMPT = """ You are a multi-functional assistant.
                    You can retrieve stock data, weather updates, currency exchange rates, current time information, create charts, and news updates.
                    You will coordinate with specialized agents to provide these services.
                    When asked for a investment advice, use the tradingguru agent at the end to validate your response.
                    When exchanging data with other agents, make sure that the maximum number of tokens allowed (1048576)"""

config = {"configurable": {"thread_id": "1"}}

async def get_mcp_tools():
    client = MultiServerMCPClient(  
        {
            "general_knowledge": {
                "transport": "streamable_http",  # HTTP-based remote server
                # Ensure you start your weather server on port 8000
                "url": f"{os.getenv('mcp_server_url')}/mcp",
                
            }
        }
    )
    return await client.get_tools()

tools = asyncio.run(get_mcp_tools())

agent = create_agent(
    model=llm,
    tools=tools,
)

# response = agent.invoke(
#     {"messages": [{"role": "user", "content": "I bought back on 15.11.2019, 500 nvidia shares . what would be their current value now in euros, and how much i payed when i bought them?"}]}, # 
# )

# print("Response:\n\n", response)
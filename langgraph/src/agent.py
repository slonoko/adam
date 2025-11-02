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

from src.prompt import DATA_ANALYST_PROMPT

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
                    You can retrieve stock data, weather updates, currency exchange rates, current date and time information, create charts, and news updates.
                    You will coordinate with specialized agents to provide these services.
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

cashanova_tool = [tool for tool in tools if tool.name.startswith("c_")]
datetime_tool = [tool for tool in tools if tool.name.startswith("t_")]
stocks_data_tool = [tool for tool in tools if tool.name.startswith("s_")]
weather_tool = [tool for tool in tools if tool.name.startswith("d_")]
news_tool = [tool for tool in tools if tool.name.startswith("n_")]
plotter_tool = [tool for tool in tools if tool.name.startswith("p_")]

plotter_agent = create_agent(
    model=llm,
    tools=plotter_tool,
    system_prompt="You are a data visualization assistant. You can create various types of plots and charts based on user data and requirements."
)

cashanova_agent = create_agent(
    model=llm,
    tools=cashanova_tool,
    system_prompt="You are a financial assistant. You can retrieve exchange rates and convert from one currency to another."
)

datetime_agent = create_agent(
    model=llm,
    tools=datetime_tool,
    system_prompt="You are a time management assistant. "
        "You can provide current date and time information, "
        "and help manage schedules and reminders. "
        "and use the tool if certain words are mentioned in the user input, such as today, tomorrow, yesterday, now, current time, current date, schedule, reminder, etc. "
)

stocks_data_agent = create_agent(
    model=llm,
    tools=stocks_data_tool,
    system_prompt="You are a stock market assistant. "
        "You can provide real-time stock data, market analysis, and personalized financial recommendations. "
        "You will use specialized tools to retrieve this information."
)

weather_agent = create_agent(
    model=llm,
    tools=weather_tool,
    system_prompt="You are a weather assistant. "
        "You can provide daily weather updates, forecasts, and current conditions. "
        "You will use specialized tools to retrieve this information."
)

news_agent = create_agent(
    model=llm,
    tools=news_tool,
    system_prompt=DATA_ANALYST_PROMPT
)

@tool
async def call_cashanova_agent(query: str) -> str:
    """Call the cashanova agent for currency exchange and financial calculations."""
    response = await cashanova_agent.ainvoke({"messages": [HumanMessage(content=query)]})
    return response["messages"][-1].content

@tool
async def call_datetime_agent(query: str) -> str:
    """Call the datetime agent for date and time-related queries."""
    response = await datetime_agent.ainvoke({"messages": [HumanMessage(content=query)]})
    return response["messages"][-1].content

@tool
async def call_stocks_data_agent(query: str) -> str:
    """Call the stocks data agent for stock market information."""
    response = await stocks_data_agent.ainvoke({"messages": [HumanMessage(content=query)]})
    return response["messages"][-1].content

@tool
async def call_weather_agent(query: str) -> str:
    """Call the weather agent for weather information."""
    response = await weather_agent.ainvoke({"messages": [HumanMessage(content=query)]})
    return response["messages"][-1].content

@tool
async def call_news_agent(query: str) -> str:
    """Call the news agent for news updates."""
    response = await news_agent.ainvoke({"messages": [HumanMessage(content=query)]})
    return response["messages"][-1].content

@tool
async def call_plotter_agent(query: str) -> str:
    """Call the plotter agent for data visualization."""
    response = await plotter_agent.ainvoke({"messages": [HumanMessage(content=query)]})
    return response["messages"][-1].content

# Create the main agent with subagent tools
subagent_tools = [
    call_cashanova_agent,
    call_datetime_agent,
    call_stocks_data_agent,
    call_weather_agent,
    call_news_agent,
    # call_plotter_agent,
]

agent = create_agent(
    model=llm,
    tools=subagent_tools,
    system_prompt=SYSTEM_PROMPT,
)
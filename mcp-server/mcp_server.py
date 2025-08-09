import asyncio
import logging
from fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.routing import Mount
from tools.exchange_rate import mcp as cashanova_mcp
from tools.datetime_info import mcp as datetime_mcp
from tools.stocks_data import mcp as stocks_data_mcp
from tools.weather import mcp as weather_mcp
from tools.plotter import mcp as plotter_mcp
from tools.news import mcp  as news_mcp
from tools.corpora_search import mcp as corpus_tools
import sys
from dotenv import load_dotenv
import uvicorn

load_dotenv()

logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Define main server
main_mcp = FastMCP(name="AdamMCP", stateless_http=True)

# Import subserver
async def setup():
    await main_mcp.import_server(cashanova_mcp, prefix="c")
    await main_mcp.import_server(datetime_mcp, prefix="t")
    await main_mcp.import_server(stocks_data_mcp, prefix="s")
    await main_mcp.import_server(weather_mcp, prefix="d")
    await main_mcp.import_server(plotter_mcp, prefix="p")
    await main_mcp.import_server(news_mcp, prefix="n")
    await main_mcp.import_server(corpus_tools, prefix="cs")

if __name__ == "__main__":
    asyncio.run(setup())
    main_mcp.run(transport= "streamable-http", host="localhost")
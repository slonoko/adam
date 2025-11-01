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
#from tools.corpora_search import mcp as corpus_tools
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
app = FastMCP(name="AdamMCP")


# Import subserver
def setup():
    app.mount(cashanova_mcp, prefix="c")
    app.mount(datetime_mcp, prefix="t")
    app.mount(stocks_data_mcp, prefix="s")
    app.mount(weather_mcp, prefix="d")
    # app.mount(plotter_mcp, prefix="p")
    app.mount(news_mcp, prefix="n")
    # app.mount(corpus_tools, prefix="cs")

setup()

if __name__ == "__main__":
    app.run(transport= "streamable-http", host="0.0.0.0")
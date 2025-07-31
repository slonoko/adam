import logging
import gunicorn
from starlette.applications import Starlette
from starlette.routing import Mount
from tools.exchange_rate import mcp as cashanova_mcp
from tools.datetime import mcp as datetime_mcp
from tools.stocks_data import mcp as stocks_data_mcp
from tools.weather import mcp as weather_mcp
from tools.plotter import mcp as plotter_mcp
from tools.news import mcp  as news_mcp
import sys
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)",
    datefmt="%Y-%m-%d %H:%M:%S",
)

app = Starlette(
    debug=True,
    routes=[
        Mount("/cashanova", app=cashanova_mcp.sse_app()),
        Mount("/timekeeper", app=datetime_mcp.sse_app()),
        Mount("/stockwhisperer", app=stocks_data_mcp.sse_app()),
        Mount("/dailydrip", app=weather_mcp.sse_app()),
        Mount("/plotter", app=plotter_mcp.sse_app()),
        Mount("/news", app=news_mcp.sse_app()),
    ],
)
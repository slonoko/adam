import logging
import uvicorn
from starlette.applications import Starlette
from starlette.routing import Mount
from tools.exchange_rate import mcp as cashanova_mcp
from tools.datetime import mcp as datetime_mcp
from tools.stocks_data import mcp as stocks_data_mcp
from tools.weather import mcp as weather_mcp
import sys

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
    ],
)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8001)
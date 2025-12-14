# Adam MCP Server

A Model Context Protocol (MCP) server providing financial, weather, news, and data tools for Adam AI agents.

## Setup

### 1. Install uv

Install the `uv` package manager:

```bash
pip install uv
```

### 2. Install Dependencies

Sync project dependencies:

```bash
uv sync
```

### 3. Configure Environment

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

- **ALPHAVANTAGE_KEY**: Get from [Alpha Vantage](https://www.alphavantage.co/support/#api-key)
- **EXCHANGE_RATE_API_KEY**: Get from [Exchange Rate API](https://exchangerate-api.com/)
- **NEWS_API_KEY**: Get from [News API](https://newsapi.org/)

### 4. Activate Environment

Activate the virtual environment:

**Linux/macOS:**
```bash
source .venv/bin/activate
```

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

### 5. Run the Server

Start the MCP server:

```bash
fastmcp run server.py:app --transport streamable-http --host 0.0.0.0 --port 8001
```

The server will be available at `http://0.0.0.0:8001`.

## Available Tools

- **Exchange Rates** - Currency conversion
- **Date/Time** - Current time and date
- **Stock Data** - Market data and analysis
- **Weather** - Weather information
- **News** - News aggregation
- **Home Sensors** - Home sensor data

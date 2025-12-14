# Adam Agents (ADK)

AI agents for trading, finance, weather, news, and data visualization built with Google ADK and Model Context Protocol.

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

Edit `.env` and add your configuration:

- **GOOGLE_API_KEY**: Get from [Google AI Studio](https://aistudio.google.com/app/apikey)
- **MODEL_NAME**: AI model to use (e.g., `gemini-2.5-flash`)
- **mcp_server_url**: MCP server URL (default: `http://localhost:8001`)

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

### 5. Run the Web Interface

Start the ADK web interface:

```bash
adk web --allow_origins "http://localhost:3000"
```

The web interface will be available for interactive access to all agents.

## Available Agents

- **ClocknStock** - Multi-agent coordinator
- **StockWhisperer** - Stock market analysis
- **Cashanova** - Currency exchange
- **DailyDrip** - Weather information
- **Drawer** - Data visualization
- **FreshNews** - News aggregation
- **TradingGuru** - Trading insights
- **Timekeeper** - Time management
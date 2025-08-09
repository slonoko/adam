# Adam MCP Server

A Model Context Protocol (MCP) server that provides specialized tools for the Adam AI agents. This server exposes various financial, weather, news, and data visualization capabilities through MCP-compliant HTTP-streamable endpoints.

## 🚀 Features

### Available Tools

- **💰 Exchange Rate Tools** - Currency conversion and exchange rate data
- **🕒 DateTime Tools** - Current time and date information
- **📈 Stock Data Tools** - Real-time stock market data and analysis
- **🌤️ Weather Tools** - Current weather and forecast information  
- **📊 Plotting Tools** - Data visualization and charting capabilities
- **📰 News Tools** - Latest news aggregation and updates
- **🔍 Corpora Search Tools** - Document search and retrieval using RAG

## 📁 Project Structure

```
mcp-server/
├── tools/                    # Tool implementations
│   ├── __init__.py
│   ├── datetime_info.py      # Time and date utilities
│   ├── exchange_rate.py      # Currency exchange tools
│   ├── news.py               # News aggregation tools
│   ├── plotter.py            # Data visualization tools
│   ├── stocks_data.py        # Stock market data tools
│   ├── weather.py            # Weather information tools
│   └── corpora_search.py     # Document search and RAG tools
├── mcp_server.py             # Main MCP server application
├── pyproject.toml            # Python dependencies
├── uv.lock                   # Lock file for dependencies
├── Dockerfile                # Container configuration
├── compose.yml               # Multi-container setup
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules
└── README.md                 # This file
```

## 🛠️ Installation

### Prerequisites

- Python 3.10 or higher
- `uv` package manager
- Environment variables configured
- Required API keys for external services

### Setup Instructions

1. **Install uv package manager (if not already installed):**
   ```bash
   pip install uv
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```

3. **Set up environment variables:**
   - Copy the example environment file:
     ```bash
     cp .env.example .env
     ```
   - Configure required API keys and settings in `.env`:
     ```env
     # Google Cloud Configuration
     GOOGLE_CLOUD_PROJECT=your-project-id
     GOOGLE_CLOUD_LOCATION=us-central1
     GOOGLE_API_KEY=your-api-key
     ...
     
     # External API Keys
     # Weather API keys, stock data APIs, news APIs, etc.
     # Add your service-specific API keys here
     ```

4. **Set up Google Cloud credentials (for corpora search):**
   - Configure Application Default Credentials via `gcloud auth application-default login`
   - Or place your service account JSON file in the project root and set the environment variable:
     ```env
     GOOGLE_APPLICATION_CREDENTIALS=path/to/your/service-account.json
     ```

## 🚦 Running the Server

### Local Development

Start the MCP server:

```bash
uv run mcp_server.py
```

The server will be available at `http://localhost:8001` with MCP endpoints accessible via HTTP-streamable transport.

### Docker Deployment

Build and run using Docker:

```bash
# Build the container
docker build -t adam-mcp-server .

# Run the container
docker run -p 8001:8000 adam-mcp-server

# Or use Docker Compose
docker compose up --build
```

## 🧪 Testing the Server

### MCP Inspector

To test and interact with the MCP server during development, you can use the official MCP Inspector tool:

```bash
# Install and run the MCP Inspector
npx @modelcontextprotocol/inspector
```

The inspector provides a web-based interface to:
- Connect to your running MCP server endpoints
- Test individual tools and their parameters
- View tool responses and debug issues
- Validate MCP protocol compliance
- Explore available tools and their schemas

#### Using the Inspector:

1. **Start your MCP server:**
   ```bash
   uv run mcp_server.py
   ```

2. **Launch the inspector in a new terminal:**
   ```bash
   npx @modelcontextprotocol/inspector
   ```

3. **Connect to your server endpoints:**
   - Open the inspector web interface (usually at `http://localhost:5173`)
   - Add your MCP server endpoints (e.g., `http://localhost:8001/stockwhisperer/sse`)
   - Test individual tools with sample parameters

### Google Cloud Deployment

Deploy to Google Cloud using Cloud Build, Artifact Registry, and Cloud Run:

#### Prerequisites

- Google Cloud Project with billing enabled
- `gcloud` CLI installed and authenticated
- Required APIs enabled (Cloud Build, Artifact Registry, Cloud Run)

#### Deployment Steps

1. **Create an Artifact Registry repository to store the container image:**
   ```bash
   gcloud artifacts repositories create remote-mcp-servers \
     --repository-format=docker \
     --location=us-central1 \
     --description="Repository for remote MCP servers" \
     --project=$PROJECT_ID
   ```

2. **Build the container image and push it to Artifact Registry with Cloud Build:**
   ```bash
   gcloud builds submit --region=us-central1 --tag us-central1-docker.pkg.dev/$PROJECT_ID/remote-mcp-servers/mcp-server:latest
   ```

3. **Deploy the MCP server container image to Cloud Run:**
   ```bash
   gcloud run deploy mcp-server \
     --image us-central1-docker.pkg.dev/$PROJECT_ID/remote-mcp-servers/mcp-server:latest \
     --region=us-central1 \
     --no-allow-unauthenticated
   ```

#### Deployment Verification

Once deployment is complete, you will see a success message similar to:

```
Service [mcp-server] revision [mcp-server-12345-abc] has been deployed and is serving 100 percent of traffic.
```

The service will be accessible at the Cloud Run service URL provided in the deployment output.

## 🔧 Tool Details

### Exchange Rate Tools (`cashanova`)
- Currency conversion between different currencies
- Real-time exchange rate data
- Financial calculations

### DateTime Tools (`timekeeper`)
- Current date and time retrieval
- Timezone-aware time operations
- Schedule and reminder utilities

### Stock Data Tools (`stockwhisperer`)
- Real-time stock price data
- Historical market data
- Stock analysis and trends
- Portfolio calculations

### Weather Tools (`dailydrip`)
- Current weather conditions
- Weather forecasts
- Location-based weather data

### Plotting Tools (`plotter`)
- Chart generation (line, bar, candlestick, etc.)
- Data visualization utilities
- Multiple chart formats and export options

### News Tools (`news`)
- Latest news aggregation
- Topic-specific news filtering
- Real-time news updates

### Corpora Search Tools (`corpora_search`)
- Document search and retrieval using Google Cloud RAG
- Semantic search across document collections
- Vector-based document similarity matching
- Support for multiple corpora and knowledge bases

## 🔗 MCP Integration

This server implements the Model Context Protocol (MCP) specification:

- **Protocol**: MCP over HTTP-streamable transport
- **Transport**: HTTP with streaming for real-time communication
- **Tool Discovery**: Automatic tool registration and discovery
- **Error Handling**: Standardized MCP error responses

## 🔧 Configuration

### Environment Variables

Configure the following environment variables as needed:

- **API Keys**: Weather API, stock data APIs, news APIs, Google Cloud credentials
- **Google Cloud**: `GOOGLE_CLOUD_PROJECT`, `GOOGLE_CLOUD_LOCATION`, `GOOGLE_API_KEY`
- **Server Configuration**: Port, host, logging levels
- **External Services**: API endpoints and authentication tokens

### Server Settings

The server runs on port 8001 by default (mapped to container port 8000) and can be configured through environment variables or the main application file.

## 📊 Logging

The server includes comprehensive logging:

- Request/response logging for all MCP interactions
- Tool execution logging with debug information
- Error tracking and debugging support

## 🤝 Contributing

1. Add new tools in the `tools/` directory
2. Register new MCP endpoints in `mcp_server.py`
3. Follow MCP protocol specifications
4. Include proper error handling and logging
5. Test with MCP-compatible clients

---

Built with ❤️ using Model Context Protocol (MCP) and HTTP-streamable transport

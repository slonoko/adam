# Adam Agents

A collection of specialized AI agents for trading, finance, weather, news, and data visualization. Built using the Google ADK framework and Model Context Protocol (MCP), these agents provide intelligent assistance across multiple domains through a sophisticated multi-agent architecture.

## 🚀 Features

### Specialized Agents

- **🕒 Timekeeper** - Time management and scheduling assistant
- **📈 StockWhisperer** - Real-time stock market analysis and trading insights
- **💰 Cashanova** - Currency exchange rates and financial conversions
- **🌤️ DailyDrip** - Weather forecasts and current conditions
- **📊 Drawer** - Advanced data visualization and charting
- **📰 FreshNews** - Latest news and market insights
- **📚 TradingGuru** - Trading insights and information retrieval from trading corpora
- **⚡ ClocknStock** - Multi-functional coordinator agent that orchestrates all specialized agents

### Core Capabilities

- **Real-time Market Data**: Live stock prices, market analysis, and financial recommendations
- **Weather Intelligence**: Current conditions, forecasts, and weather-based planning
- **Currency Exchange**: Real-time exchange rates and multi-currency conversions
- **News Aggregation**: Latest news updates across technology, finance, and health
- **Data Visualization**: Professional charts, graphs, and financial visualizations
- **Time Management**: Current time, scheduling, and reminder assistance

## 📁 Project Structure

```
agents/
├── cashanova/          # Currency exchange agent
├── clocknstock/        # Multi-agent coordinator
├── dailydrip/          # Weather information agent
├── drawer/             # Data visualization agent
├── freshnews/          # News aggregation agent
├── stockwhisperer/     # Stock market agent
├── timekeeper/         # Time management agent
├── tradingguru/        # Trading insights and corpora search agent
├── .env.example        # Environment variables template
├── pyproject.toml      # Python dependencies
└── README.md           # This file
```

## 🛠️ Installation

### Prerequisites

- Python 3.10 or higher
- `uv` package manager
- Environment variables configured
- MCP server running (provides tools to agents)

### Setup Instructions

1. **Install uv package manager (if not already installed):**
   ```bash
   pip install uv
   ```

2. **Install dependencies:**
   ```bash
   uv install
   ```

3. **Set up environment variables:**
   - Copy the example environment file:
     ```bash
     cp .env.example .env
     ```
   - Configure required API keys and model settings in `.env`:
     ```env
     # Google Cloud Configuration
     GOOGLE_CLOUD_PROJECT=your_google_cloud_project_id
     GOOGLE_CLOUD_LOCATION=us-central1
     GOOGLE_GENAI_USE_VERTEXAI=False

     # Google API Key for Gemini models
     GOOGLE_API_KEY=your_google_api_key_here

     # AI Model to use for agents
     MODEL_NAME=gemini-2.5-flash

     # MCP Server URL (where the MCP tools server is running)
     mcp_server_url=http://localhost:8080
     ```

## 🚦 Running the Agents

### Running Individual Agents

Each agent can be run independently using the Google ADK framework:

```bash
# Run the multi-agent coordinator
adk run clocknstock

# Or run individual agents
adk run stockwhisperer
adk run cashanova
adk run dailydrip
adk run timekeeper
adk run drawer
adk run freshnews
adk run tradingguru
```

### Web Interface

Launch the web interface for interactive access:

```bash
adk web
```

### API Server

Run as a server for programmatic access:

```bash
adk api_server
```

> **Note**: These agents require the MCP server to be running to access their tools. Each agent connects to specific MCP endpoints for their functionality.

## 🐳 Docker Deployment

The agents can be containerized and deployed using Docker configurations available in the parent project.

## 🤖 Agent Descriptions

### ClocknStock (Coordinator Agent)
The main orchestrator that coordinates all specialized agents to provide comprehensive assistance. It uses a PlanReActPlanner to intelligently route requests to appropriate sub-agents, including validation of investment advice through the TradingGuru agent.

### StockWhisperer
An AI-powered stockbroker providing:
- Real-time stock data and analysis
- Market trend monitoring
- Personalized financial recommendations
- Portfolio management insights

### Cashanova
Financial exchange specialist offering:
- Real-time currency exchange rates
- Multi-currency conversions
- Financial calculations

### DailyDrip
Weather intelligence agent providing:
- Current weather conditions
- Weather forecasts
- Location-based weather insights

### Drawer
Data visualization specialist creating:
- Line charts for trends
- Candlestick charts for stock analysis
- Bar charts for comparisons
- Scatter plots for correlations
- Heatmaps for data relationships
- Histograms for distributions

### FreshNews
News aggregation agent delivering:
- Real-time news updates
- Technology, health, and finance news
- Personalized content recommendations

### TradingGuru
Trading insights specialist providing:
- Information retrieval from trading corpora
- Trading knowledge and insights
- Investment advice validation

### Timekeeper
Time management assistant providing:
- Current date and time
- Schedule management
- Reminder services

## 📊 Example Use Cases

1. **Trading Analysis**: "I own 2835 NVIDIA stocks bought at €74 each one year ago. What's their current value in euros and my profit?"

2. **Weather Planning**: "What's the weather forecast for New York this week?"

3. **Currency Exchange**: "Convert $1000 USD to EUR at current rates"

4. **Market Visualization**: "Create a candlestick chart for Apple stock over the last month"

5. **News Updates**: "Get the latest technology news"

## 🔧 Configuration

### Environment Variables

Key environment variables to configure:

- `GOOGLE_CLOUD_PROJECT`: Your Google Cloud project ID
- `GOOGLE_CLOUD_LOCATION`: Google Cloud region (default: us-central1)
- `GOOGLE_API_KEY`: Google API key for Gemini models
- `MODEL_NAME`: The LLM model to use for agents (e.g., gemini-2.5-flash)
- `mcp_server_url`: URL of the MCP server providing tools to agents (default: http://localhost:8080)

### MCP Integration

The agents connect to MCP server endpoints for their tools:
- Each agent is configured to connect to specific MCP endpoints
- The MCP server provides the actual tool implementations
- Agents use SSE (Server-Sent Events) connections to communicate with MCP tools

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is part of the Adam assistant ecosystem. Please refer to the main repository for licensing information.

## 🆘 Support

For issues and questions:
1. Check the existing issues in the repository
2. Create a new issue with detailed information
3. Include logs and reproduction steps

---

Built with ❤️ using Google ADK and Model Context Protocol (MCP)
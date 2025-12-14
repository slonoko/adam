# ADAM Project

A multi-service application with MCP server, ADK agent, and web UI.

## Quick Start

### Prerequisites

- Docker and Docker Compose installed
- API keys for the services you want to use

### Setup

1. **Create environment files**

   Before running the application, you need to create `.env` files for the required services:

   **For `adk` project:**
   ```bash
   cp adk/.env.example adk/.env
   ```
   Edit `adk/.env` and add your configuration. **Important:** Set the MCP server URL:
   ```env
   mcp_server_url=http://mcp:8000
   ```

   **For `mcp-server` project:**
   ```bash
   cp mcp-server/.env.example mcp-server/.env
   ```
   Edit `mcp-server/.env` and add your configuration.

2. **Run the application**

   **On Linux:**
   ```bash
   docker compose up -d
   ```

   **On Windows (Docker Desktop):**
   ```powershell
   docker-compose -f compose.yml up -d
   ```
   Or using Docker Compose V2:
   ```powershell
   docker compose -f compose.yml up -d
   ```

3. **Access the services**

   - Web UI: http://localhost:8003
   - ADK Agent: http://localhost:8000
   - MCP Server: http://localhost:8001

### Stop the application

```bash
docker-compose -f compose.yml down
```

## Notes

- The `adk` service depends on the `mcp` service and will wait for it to start
- The `ui` service depends on the `adk` service
- All services are connected via the `adam-network` bridge network

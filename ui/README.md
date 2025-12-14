# Adam Dashboard

An interactive dashboard for the Adam ADK API that creates dynamic widgets based on conversational queries.

## Features

- **Dynamic Widget Grid**: Automatically arranges widgets in a responsive grid layout
- **Chat Interface**: Natural language interaction with the ADK API
- **Multiple Widget Types**: Automatically creates appropriate widgets for different response types:
  - Text panels for conversational responses
  - Tables for structured data
  - Images for visualizations
  - Error widgets for failed requests
- **Real-time Integration**: Connects to the ADK API at http://localhost:8000/
- **Built with Streamlit**: Fast, Python-based UI framework

## Getting Started

### Prerequisites

- Python 3.10 or higher
- `uv` package manager
- ADK API running at http://localhost:8000/

### Installation

Install dependencies using `uv`:

```bash
uv pip install -e .
```

### Running the Dashboard

**Option 1: Using the run script**
```bash
./run.sh
```

**Option 2: Manually**
```bash
source .venv/bin/activate
streamlit run app.py --server.port 8501
```

The dashboard will open at http://localhost:8501/

**Note:** Make sure your ADK API is running at http://localhost:8000/ before using the dashboard.

## Usage

1. Type your question in the chat box at the bottom
2. Press Enter to send
3. A new widget will appear on the dashboard with the results
4. Remove individual widgets using the × button
5. Clear all widgets using the sidebar button

## Configuration

The API endpoint can be configured by editing the `API_BASE_URL` variable in [app.py](app.py):

```python
API_BASE_URL = "http://localhost:8000"
```

## API Integration

The dashboard integrates with the **Google Agent Development Kit (ADK) FastAPI server** using the `/run_sse` endpoint.

### API Configuration

Edit these variables in [app.py](app.py):

```python
API_BASE_URL = "http://localhost:8000"  # Your ADK server URL
APP_NAME = "tradingadvisor"              # Your agent app name
```

### Session Management

The dashboard automatically manages sessions:

1. **Create Session**: First time a user interacts, a POST request is made to:
   ```
   POST /apps/{app_name}/users/{user_id}/sessions
   ```
   This returns a session object with an `id` field.

2. **Use Session**: Subsequent messages use this session ID.

### Request Format

The dashboard sends requests to `/run_sse` with the following structure:

```json
{
  "app_name": "tradingadvisor",
  "userId": "dashboard_user_123",
  "sessionId": "1d9237cc-69b9-40e9-baad-510514191b4e",
  "newMessage": {
    "role": "user",
    "parts": [{"text": "Your question here"}]
  }
}
```

### Response Format

The ADK API streams responses using Server-Sent Events (SSE). The dashboard processes these events and extracts:

- Text content from agent responses
- Structured data for tables
- Images and visualizations
- Error messages

### Supported Response Types

**Text responses:** Any text content returned by the agent

**Table responses:** Responses containing a `data` array:
```json
{
  "data": [
    {"column1": "value1", "column2": "value2"},
    {"column1": "value3", "column2": "value4"}
  ]
}
```

**Image responses:** Responses with image URLs:
```json
{
  "image": "https://example.com/chart.png"
}
```

### Starting Your ADK Server

Make sure your ADK server is running:

```bash
# From your ADK project directory
adk api_server /path/to/adk/project

# Or using uvicorn with a custom main.py
uvicorn main:app --host 0.0.0.0 --port 8000
```

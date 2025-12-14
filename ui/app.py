import streamlit as st
import requests
import json
import pandas as pd
from datetime import datetime
from PIL import Image
import io
import base64
import config

# Page configuration
st.set_page_config(
    page_title="Adam Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stChatMessage {
        background-color: white;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .widget-container {
        background-color: white;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    .widget-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    h1 {
        color: white;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    }
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 500;
    }
    .empty-state {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 3rem;
        border-radius: 12px;
        text-align: center;
        color: white;
        margin: 2rem auto;
        max-width: 600px;
    }
    .empty-state h2 {
        font-size: 2rem;
        margin-bottom: 1rem;
    }
    .empty-state ul {
        text-align: left;
        list-style: none;
        padding: 0;
    }
    .empty-state li:before {
        content: "💡 ";
    }
</style>
""", unsafe_allow_html=True)

# API Configuration (loaded from config.py)
API_BASE_URL = config.API_BASE_URL
APP_NAME = config.APP_NAME

# Initialize session state
if 'widgets' not in st.session_state:
    st.session_state.widgets = []
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'user_id' not in st.session_state:
    st.session_state.user_id = f"dashboard_user_{int(datetime.now().timestamp())}"
if 'session_id' not in st.session_state:
    st.session_state.session_id = None
if 'session_initialized' not in st.session_state:
    st.session_state.session_initialized = False

def create_session() -> str:
    """Create a new session via the ADK API and return the session ID"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/apps/{APP_NAME}/users/{st.session_state.user_id}/sessions",
            json={},
            timeout=10
        )
        response.raise_for_status()
        session_data = response.json()
        session_id = session_data.get("id")
        if session_id:
            st.session_state.session_id = session_id
            st.session_state.session_initialized = True
            return session_id
        else:
            raise ValueError("No session ID in response")
    except Exception as e:
        st.error(f"Failed to create session: {str(e)}")
        return None

def ensure_session():
    """Ensure a valid session exists, create one if needed"""
    if not st.session_state.session_initialized or not st.session_state.session_id:
        return create_session()
    return st.session_state.session_id

def call_adk_api(message: str) -> dict:
    """Call the Google ADK API with the user's message using Server-Sent Events"""
    try:
        # Ensure we have a valid session before making the API call
        session_id = ensure_session()
        if not session_id:
            return {"error": "Failed to create or retrieve session"}
        
        # Use the SSE endpoint for streaming responses
        response = requests.post(
            f"{API_BASE_URL}/run_sse",
            json={
                "app_name": APP_NAME,
                "userId": st.session_state.user_id,
                "sessionId": session_id,
                "newMessage": {
                    "role": "user",
                    "parts": [{"text": message}]
                }
            },
            timeout=60,
            stream=False
        )
        response.raise_for_status()
        
        # Parse SSE stream and collect all events
        full_response = {"text": "", "events": []}
        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8')
                if line_str.startswith('data: '):
                    try:
                        event_data = json.loads(line_str[6:])
                        full_response["events"].append(event_data)
                        
                        # Extract text content from various event types
                        if event_data.get("type") == "agent_response":
                            content = event_data.get("data", {}).get("content", "")
                            if content:
                                full_response["text"] += content
                        elif event_data.get("type") == "text":
                            full_response["text"] += event_data.get("data", "")
                        elif event_data.get("type") == "final_response":
                            response_data = event_data.get("data", {})
                            if isinstance(response_data, dict):
                                full_response.update(response_data)
                            
                    except json.JSONDecodeError:
                        continue
        
        # If we collected text, return it
        if full_response.get("text"):
            return {"message": full_response["text"], "events": full_response["events"]}
        elif full_response.get("events"):
            # Return the last meaningful event
            return {"type": "text", "content": full_response.get("events", [{}])[-1].get("content").get("parts")[0].get("text"), "message": "Response received"}
        else:
            return {"message": "Response received but no content available"}
            
    except requests.exceptions.ConnectionError:
        return {
            "error": f"Cannot connect to API at {API_BASE_URL}. Make sure the ADK server is running."
        }
    except requests.exceptions.Timeout:
        return {"error": "Request timed out. The server took too long to respond."}
    except requests.exceptions.RequestException as e:
        return {"error": f"API Error: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

def determine_widget_type(response: dict) -> str:
    """Determine the type of widget to display based on response"""
    if "error" in response:
        return "error"
    if "data" in response and isinstance(response.get("data"), list):
        return "table"
    if any(key in response for key in ["image", "chart", "visualization", "plot"]):
        return "image"
    return "text"

def render_widget(widget_data: dict, index: int):
    """Render a widget based on its type"""
    with st.container():
        col1, col2 = st.columns([20, 1])
        
        with col1:
            st.markdown(f'<div class="widget-header">💬 {widget_data["message"]}</div>', unsafe_allow_html=True)
        
        with col2:
            if st.button("×", key=f"remove_{index}", help="Remove widget"):
                st.session_state.widgets.pop(index)
                st.rerun()
        
        # Render content based on type
        widget_type = widget_data["type"]
        content = widget_data["content"]
        
        if widget_type == "error":
            st.error(f"❌ {content.get('error', 'An error occurred')}")
        
        elif widget_type == "table":
            data = content.get("data", content)
            if isinstance(data, list) and len(data) > 0:
                df = pd.DataFrame(data)
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("No data available")
        
        elif widget_type == "image":
            image_url = content.get("image") or content.get("chart") or content.get("visualization")
            if image_url:
                try:
                    # Handle both URLs and base64 encoded images
                    if image_url.startswith("http"):
                        st.image(image_url, use_container_width=True)
                    elif image_url.startswith("data:image"):
                        st.image(image_url, use_container_width=True)
                    else:
                        st.image(image_url, use_container_width=True)
                except Exception as e:
                    st.error(f"Failed to load image: {str(e)}")
            else:
                st.info("No image available")
        
        else:  # text widget
            # Extract text content
            if isinstance(content, str):
                text = content
            elif isinstance(content, dict):
                text = (
                       content.get("content") or 
                       json.dumps(content, indent=2))
            else:
                text = str(content)
            
            st.markdown(text)

# Header
st.title(config.DASHBOARD_TITLE)
st.markdown(config.DASHBOARD_SUBTITLE)

# Main content area
if len(st.session_state.widgets) == 0:
    # Empty state
    st.markdown("""
    <div class="empty-state">
        <h2>Welcome to Adam Dashboard</h2>
        <p>Ask a question below to create your first widget</p>
        <div style="margin-top: 2rem;">
            <h3>Try asking:</h3>
            <ul>
                {''.join(f'<li>{query}</li>' for query in config.EXAMPLE_QUERIES)}
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    # Display widgets in grid layout
    cols_per_row = config.WIDGETS_PER_ROW
    for i in range(0, len(st.session_state.widgets), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col in enumerate(cols):
            idx = i + j
            if idx < len(st.session_state.widgets):
                with col:
                    st.markdown('<div class="widget-container">', unsafe_allow_html=True)
                    render_widget(st.session_state.widgets[idx], idx)
                    st.markdown('</div>', unsafe_allow_html=True)

# Chat input at the bottom
st.markdown("---")
with st.container():
    col1, col2 = st.columns([6, 1])
    
    with col1:
        user_input = st.chat_input("Ask a question...", key="chat_input")
    
    if user_input:
        # Add to messages
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Call API
        with st.spinner("Getting response..."):
            response = call_adk_api(user_input)
        
        # Create widget
        widget = {
            "id": f"widget_{datetime.now().timestamp()}",
            "type": determine_widget_type(response),
            "content": response,
            "message": user_input,
            "timestamp": datetime.now().isoformat()
        }
        
        st.session_state.widgets.append(widget)
        st.rerun()

# Sidebar with controls
with st.sidebar:
    st.header("Dashboard Controls")
    
    if st.button("🗑️ Clear All Widgets"):
        st.session_state.widgets = []
        st.session_state.messages = []
        st.rerun()
    
    if st.button("🔄 New Session"):
        # Reset session state and create a new session via API
        st.session_state.session_id = None
        st.session_state.session_initialized = False
        st.session_state.widgets = []
        st.session_state.messages = []
        # Create new session
        with st.spinner("Creating new session..."):
            create_session()
        st.rerun()
    
    st.markdown("---")
    st.subheader("API Status")
    
    # Check API health by listing apps
    try:
        apps_response = requests.get(f"{API_BASE_URL}/list-apps", timeout=5)
        if apps_response.status_code == 200:
            apps = apps_response.json()
            st.success("✅ API Connected")
            st.info(f"📱 Available apps: {', '.join(apps)}")
            if APP_NAME not in apps:
                st.warning(f"⚠️ App '{APP_NAME}' not found. Update APP_NAME in app.py")
        else:
            st.warning("⚠️ API Responding (Non-200)")
    except:
        st.error("❌ API Not Available")
    
    st.markdown(f"**Endpoint:** `{API_BASE_URL}`")
    st.markdown(f"**App Name:** `{APP_NAME}`")
    st.markdown(f"**User ID:** `{st.session_state.user_id}`")
    if st.session_state.session_id:
        st.markdown(f"**Session:** `{st.session_state.session_id}`")
        if st.session_state.session_initialized:
            st.success("✓ Session Active")
    else:
        st.warning("⚠️ No active session")
    
    st.markdown("---")
    st.subheader("Statistics")
    st.metric("Active Widgets", len(st.session_state.widgets))
    st.metric("Total Messages", len(st.session_state.messages))

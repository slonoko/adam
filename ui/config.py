"""
Configuration file for the Adam Dashboard
Edit these settings to customize your dashboard
"""

# ADK API Configuration
API_BASE_URL = "http://localhost:8000"
APP_NAME = "tradingadvisor"  # Change to your agent app name

# Dashboard Settings
DASHBOARD_TITLE = "🤖 Adam Dashboard"
DASHBOARD_SUBTITLE = "Ask questions and create interactive widgets"

# Layout Settings
WIDGETS_PER_ROW = 2  # Number of widgets to display per row

# Example queries to show on empty dashboard
EXAMPLE_QUERIES = [
    "What's the current weather?",
    "Show me AAPL stock data",
    "Get the latest tech news",
    "What's the exchange rate for USD to EUR?",
    "What time is it?",
]

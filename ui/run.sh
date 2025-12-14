#!/bin/bash
# Start the Adam Dashboard

cd "$(dirname "$0")"

# Activate virtual environment
source .venv/bin/activate

# Run Streamlit
streamlit run app.py --server.port 8501

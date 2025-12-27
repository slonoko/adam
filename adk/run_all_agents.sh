#!/bin/bash

# Script to run all agents with uvicorn
# Each agent runs on a different port

# Activate virtual environment
source .venv/bin/activate

# Base port
BASE_PORT=8002

echo "Starting all agents..."
echo "================================"

# Array of agent folders
agents=(
    "broker_agent"
    "home_sensor_agent"
    "weather_agent"
    "stock_agent"
    "time_agent"
    "code_agent"
    "news_agent"
)

# Start each agent in the background
port=$BASE_PORT
for agent in "${agents[@]}"; do
    echo "Starting $agent on port $port..."
    uvicorn ${agent}.agent:a2a_app --host localhost --port $port &
    port=$((port + 1))
done

echo "================================"
echo "All agents started!"
echo "Ports: $BASE_PORT to $((BASE_PORT + ${#agents[@]} - 1))"
echo ""
echo "Agent assignments:"
port=$BASE_PORT
for agent in "${agents[@]}"; do
    echo "  - $agent: http://localhost:$port"
    port=$((port + 1))
done
echo ""
echo "Press Ctrl+C to stop all agents"

# Wait for all background processes
wait

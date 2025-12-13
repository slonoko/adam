# Use official Python runtime as base image
FROM python:3.14-slim

# Create agents directory
RUN mkdir -p /app/agents

# Set working directory
WORKDIR /app/agents

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
COPY tradingadvisor/ ./tradingadvisor/

RUN pip install --no-cache-dir -r requirements.txt

# Create non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser
RUN chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Start the application
CMD ["adk", "web", "--allow_origins", "*" ,"--host", "0.0.0.0", "--port", "8000", "/app/agents/"]

# uvicorn tradingadvisor.agent:a2a_app --host localhost --port 8000
# CMD ["uvicorn", "tradingadvisor.agent:a2a_app", "--host", "0.0.0.0", "--port", "8000"]
# Use official Python runtime as base image
FROM python:3.14-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Copy dependency files
COPY pyproject.toml uv.lock ./
COPY tradingadvisor/ ./tradingadvisor/

# Install dependencies with uv
RUN uv sync
RUN . ./.venv/bin/activate

# Create non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser
RUN chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Start the application
# CMD [".venv/bin/adk", "web", "--host", "0.0.0.0", "--port", "8000", "/app"]

# uvicorn tradingadvisor.agent:a2a_app --host localhost --port 8000
CMD [".venv/bin/uvicorn", "tradingadvisor.agent:a2a_app", "--host", "0.0.0.0", "--port", "8000"]
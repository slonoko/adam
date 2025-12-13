# Use Python 3.14 slim image as base
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY requirements.txt ./

# Install dependencies using requrirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY server.py ./
#COPY adam-sa.json ./
COPY tools/ ./tools/

# Create a non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose the port uvicorn will run on
EXPOSE 8000

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Command to run the uvicorn server
CMD ["fastmcp", "run", "server.py:app", "--transport", "streamable-http", "--host", "0.0.0.0", "--port", "8000"]
# fastmcp run server.py:app --transport streamable-http --host 0.0.0.0 --port 8001
# Use Python 3.11 as the base image
FROM python:3.11-slim

# Set metadata
LABEL maintainer="PyGWalker Docker"
LABEL description="Dockerized PyGWalker application for interactive data visualization"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYGWALKER_HOST=0.0.0.0 \
    PYGWALKER_PORT=8888

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application script
COPY app.py .

# Create data directory for mounting volumes
RUN mkdir -p /data

# Copy sample data into the container
COPY data/sample_data.csv /data/

# Expose the port for PyGWalker web interface
EXPOSE 8888

# Run Streamlit directly
CMD ["streamlit", "run", "app.py", "--server.port=8888", "--server.address=0.0.0.0", "--server.headless=true", "--browser.gatherUsageStats=false"]

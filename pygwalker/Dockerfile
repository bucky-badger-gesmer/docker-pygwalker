FROM python:3.13-slim

# Set metadata
LABEL maintainer="PyGWalker Docker"
LABEL description="Dockerized PyGWalker application for interactive data visualization"

# Set environment variables
# PYTHONUNBUFFERED=1 enables interactive input prompts to work in Docker
# ENV PYTHONUNBUFFERED=1 \
#     PYTHONDONTWRITEBYTECODE=1 \
#     PIP_NO_CACHE_DIR=1 \
#     PIP_DISABLE_PIP_VERSION_CHECK=1 \
#     PYGWALKER_HOST=0.0.0.0 \
#     PYGWALKER_PORT=8888

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
COPY data/ /data/

# Expose the port for PyGWalker web interface
EXPOSE 8888

# Run the Flask application
CMD ["python", "app.py"]

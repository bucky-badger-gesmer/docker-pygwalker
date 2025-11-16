FROM python:3.13-slim

# Set metadata
LABEL maintainer="PyGWalker Docker"
LABEL description="Dockerized PyGWalker application for interactive data visualization"

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

RUN mkdir -p /data

# Copy sample data into the container
COPY sample_data.csv .

# Expose the port for PyGWalker web interface
EXPOSE 8888

# Run the Flask application
CMD ["python", "app.py"]

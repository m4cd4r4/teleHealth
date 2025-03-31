# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies if needed (e.g., for psycopg2)
# RUN apt-get update && apt-get install -y --no-install-recommends some-package && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
# Copy only requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on (adjust if needed, e.g., 8003)
EXPOSE 8003

# Command to run the application using Uvicorn
# The port here should match the EXPOSE port and the port in docker-compose.yml
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8003", "--reload"]

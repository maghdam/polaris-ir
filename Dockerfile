# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN apt-get update && apt-get install -y curl && \
    pip install --no-cache-dir -r requirements.txt && \
    rm -rf /var/lib/apt/lists/*

# Copy the application code into the container
# Copy the entire src directory
COPY ./src ./src

# Copy the entrypoint script
COPY api-entrypoint.sh .
RUN chmod +x api-entrypoint.sh

# Expose the port the app runs on
EXPOSE 8000
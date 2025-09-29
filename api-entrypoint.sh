#!/bin/sh
# api-entrypoint.sh

# Exit immediately if a command exits with a non-zero status.
set -e

OLLAMA_URL="http://ollama:11434"

echo "Waiting for Ollama service to be ready..."

# Use a loop to check if the ollama service is up and the model is available.
# We check for the model by querying the /api/tags endpoint.
until curl -s -f "$OLLAMA_URL/api/tags" | grep -q '"name":"llama3:latest"'; do
  echo "Ollama or llama3 model not ready yet, waiting 5 seconds..."
  sleep 5
done

echo "Ollama service is ready with llama3 model. Starting API server."
exec uvicorn src.polaris.main:app --host 0.0.0.0 --port 8000
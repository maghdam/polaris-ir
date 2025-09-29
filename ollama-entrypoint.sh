#!/bin/sh

# Start the Ollama server in the background
ollama serve &

# Capture the process ID of the server
pid=$!

echo "Waiting for Ollama server to be ready..."
sleep 5 # Give it a moment to start

echo "Pulling llama3 model..."
ollama pull llama3

# Bring the Ollama server process back to the foreground
wait $pid
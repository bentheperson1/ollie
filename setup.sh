#!/bin/bash

set -e

if ! command -v ollama &> /dev/null; then
  echo "Ollama not found. Installing Ollama..."

  echo "Downloading Ollama"
  curl -fsSL https://ollama.com/install.sh | sh
else
  echo "Ollama is already installed."
fi

MODEL="gemma2:2b"

echo "Pulling model '$MODEL'..."

if ollama pull "$MODEL"; then
  echo "Model '$MODEL' pulled successfully."
else
  echo "Error: Failed to pull model '$MODEL'."
  exit 1
fi

echo "Startup script completed successfully."

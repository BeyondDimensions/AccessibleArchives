#!/bin/bash
# Script for running the web UI app

# Define text colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No color

# the absolute path of this script's directory
SCRIPT_DIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
PROJ_DIR=$SCRIPT_DIR/../..
PY_VENV_DIR=$PROJ_DIR/.venv

# Function to check if Ollama is running
is_ollama_running() {
  pgrep -f ollama > /dev/null 2>&1
}

# Start Ollama if not running
if is_ollama_running; then
  printf "${GREEN}✔ Ollama is already running.${NC}\n"
else
  printf "${GREEN}✔ Starting Ollama...${NC}\n"
  nohup ollama serve &> /dev/null &
  sleep 5  # Wait for a few seconds to ensure Ollama starts
  if is_ollama_running; then
    printf "${GREEN}✔ Ollama started in the background.${NC}\n"
  else
    printf "${RED}✘ Failed to start Ollama. Please check logs.${NC}\n"
    exit 1
  fi
fi

# TODO add check as well if IPFS is running and run it if not

# Activate the Python virtual environment
if [ -d "$PY_VENV_DIR" ]; then
  source "$PY_VENV_DIR/bin/activate"
else
  printf "${RED}✘ Virtual environment not found at ${PY_VENV_DIR}\n${NC}"
  exit 1
fi

# Run your Streamlit app
printf "${GREEN}✔ Starting the application...${NC}\n"
streamlit run "$PROJ_DIR/src/app.py" --server.port 8501
if [ $? -eq 0 ]; then
  printf "${GREEN}✔ Application started successfully!${NC}\n"
else
  printf "${RED}✘ Failed to start the application.${NC}\n"
  exit 1
fi

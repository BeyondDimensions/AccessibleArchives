#!/bin/bash
# Script for running the web UI app

# Define text colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No color

# Change to the project directory
cd ../../src/ || { echo -e "${RED}✘ Failed to change directory to src.${NC}\n"; exit 1; }

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

# Activate the Python virtual environment
if [ -d "../.venv" ]; then
  source ../.venv/bin/activate
else
  printf "${RED}✘ Virtual environment not found. Please run the installation script first.${NC}\n"
  exit 1
fi

# Run your Streamlit app
printf "${GREEN}✔ Starting the application...${NC}\n"
streamlit run your_app.py --server.address accessible-archives.local --server.port 8501
if [ $? -eq 0 ]; then
  printf "${GREEN}✔ Application started successfully!${NC}\n"
else
  printf "${RED}✘ Failed to start the application.${NC}\n"
  exit 1
fi

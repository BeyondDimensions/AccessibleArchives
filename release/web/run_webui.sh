#!/bin/bash
# Script for running the webui app

# Define text colors
GREEN='\033[0;32m'
NC='\033[0m' # No color

cd ../../src/

# Function to check if Ollama is running
is_ollama_running() {
  pgrep -f ollama > /dev/null 2>&1
}

# Start Ollama if not running
if is_ollama_running; then
  echo -e "${GREEN}✔ Ollama is already running.${NC}"
else
  echo "Starting Ollama..."
  nohup ollama serve &> /dev/null &
  echo -e "${GREEN}✔ Ollama started in the background.${NC}"
fi

# Run your Streamlit app
echo "Starting the application..."
streamlit run app.py
echo -e "${GREEN}✔ Application started successfully!${NC}"

# Function to check if Ollama service is running
# ollama_init() {
#   local max_attempts=5  # Maximum number of attempts to start the service
#   local attempt=1        # Current attempt number
#
#   while [ $attempt -le $max_attempts ]; do
#     # Check if the Ollama service is active
#     if ! systemctl is-active --quiet ollama; then
#       printf "${YELLOW}Ollama service is not running. Attempting to start it (Attempt %d of %d)...${NC}\n" "$attempt" "$max_attempts"
#       sudo systemctl start ollama
#
#       # Wait for a few seconds to allow Ollama to initialize
#       sleep 5  # You can adjust this duration if needed
#
#       # Check again if the service is running
#       if systemctl is-active --quiet ollama; then
#         printf "${GREEN}✔ Ollama service started successfully!${NC}\n"
#         return  # Exit the function if the service started successfully
#       fi
#     else
#       printf "${GREEN}✔ Ollama service is already running.${NC}\n"
#       sleep 5
#       return  # Exit the function if the service is running
#     fi
#
#     # Increment the attempt counter
#     attempt=$((attempt + 1))
#   done
#
#   # If we reach here, it means we exhausted all attempts
#   printf "${RED}✘ Failed to start Ollama service after %d attempts. Please check logs.${NC}\n" "$max_attempts"
#   exit 1
# }

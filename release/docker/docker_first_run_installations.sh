#!/bin/bash
LOG_FILE=/opt/AccessibleArchives/FinalInstallations.log
echo "Running final installations..." > $LOG_FILE
/opt/AccessibleArchives/release/web/accessible_archives.service.sh
systemctl start ollama
systemctl enable ollama

echo "Downloading llama models..." >> $LOG_FILE
# Download Ollama model
ollama pull llama3.1:8b
# ollama pull qwen2:7b
ollama pull mxbai-embed-large

# Start Ollama as a background service
nohup ollama serve &> /dev/null &

echo "Adding DocumentCollection to IPFS..." >> $LOG_FILE
ipfs add -r /opt/AccessibleArchives/DocumentCollection

sudo systemctl enable accessible_archives
sudo systemctl start accessible_archives

echo "Finished final installations!" >> $LOG_FILE

# 
# if sudo systemctl is-active --quiet ollama; then
#   echo "Ollama is already installed and running."
# else
#   # Install Ollama
#   show_progress "Installing" "Ollama"
#   curl -fsSL https://ollama.com/install.sh -o $OLLAMA_INSTALL_SCRIPT
#   chmod +x $OLLAMA_INSTALL_SCRIPT
#   bash $OLLAMA_INSTALL_SCRIPT
#   check_status "Ollama installed" "install Ollama"
# 
#   # Cleanup files
#   cleanup_file $OLLAMA_INSTALL_SCRIPT
# 
#   # Initialize Ollama
#   show_progress "Initializing" "Ollama"
#   sudo systemctl daemon-reload
#   sudo systemctl restart ollama
#   sleep 5
#   sudo systemctl is-active --quiet ollama
#   check_status "Ollama initialized" "initialize Ollama"
# fi
systemctl start ollama
systemctl enable ollama

# Download Ollama model
# show_progress "Pulling" "Ollama Model: llama3.1:8b"
ollama pull llama3.1:8b
# check_status "Ollama Model: llama3.1:8b pulled" "pull Ollama Model: llama3.1:8b"

# show_progress "Pulling" "Ollama Model: qwen2:7b"
# ollama pull qwen2:7b
# check_status "Ollama Model: qwen2:7b pulled" "pull Ollama Model: qwen2:7b"
# # Download Ollama embedding model
# show_progress "Pulling" "Ollama Model: mxbai-embed-large"
ollama pull mxbai-embed-large
# check_status "Ollama Model: mxbai-embed-large pulled" "pull Ollama Model: mxbai-embed-large"

# Start Ollama as a background service
# show_progress "Starting" "Ollama Service"
nohup ollama serve &> /dev/null &
# check_status "Ollama Service started" "start Ollama Service"

ipfs add -r /opt/AccessibleArchives/DocumentCollections
/opt/AccessibleArchives/release/web/accessible_archives.service.sh
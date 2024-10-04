#!/bin/bash
# Script for deploying the webui app

# Define text colors for output
GREEN="\033[0;32m"
RED="\033[0;31m"
YELLOW="\033[1;33m"
NC="\033[0m" # No color

USERNAME=$(whoami)

# the absolute path of this script's directory
SCRIPT_DIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
PROJ_DIR=$SCRIPT_DIR/../..
SRC_DIR=$PROJ_DIR/src
PY_REQUIREMENTS=$PROJ_DIR/release/requirements.txt
PY_VENV_DIR=$PROJ_DIR/.venv

# TODO add data from the project to DATA_DIR!!!
# TODO clean after ipfs installation or is it done?

OLLAMA_DIR=/tmp/Ollama
OLLAMA_INSTALL_SCRIPT=$OLLAMA_DIR/install_ollama.sh
INSTALL_DIR=/opt/AccessibleArchives
DATA_DIR=/opt/AccessibleArchives/data
SYMLINK_TARGET=$INSTALL_DIR/release/web/run_webui.sh
SYMLINK_PATH=/usr/local/bin/accessible-archives
APP_DATA=$HOME/.local/share/
DESKTOP_ENTRY=$APP_DATA/applications/AccessibleArchives.desktop
# CHROMADB_DIR=/var/lib/AccessibleArchives/ChromaDB
CHROMADB_DIR=$INSTALL_DIR/ChromaDB

# Function to create a directory if it doesn't yet exist and check permissions
ensure_dir() {
if ! [ -e $1 ];then
  sudo mkdir -p $1
fi
sudo chown $USER:$USER $1
}

ensure_dir $OLLAMA_DIR
ensure_dir $INSTALL_DIR
ensure_dir $CHROMADB_DIR
ensure_dir $DATA_DIR
ensure_dir $APP_DATA

# Function to show progress bar
show_progress() {
  printf "${YELLOW}%s %s...${NC}\n" "$1" "$2"
}

# Function to check if a command succeeded or failed
check_status() {
  if [ $? -eq 0 ]; then
    printf "${GREEN}✔ %s successfully!${NC}\n" "$1"
  else
    printf "${RED}✘ Failed to %s. Please check logs.${NC}\n" "$2"
    exit 1
  fi
}

# Function to clean up files
cleanup_file() {
  if [ -f "$1" ]; then
    sudo rm -f "$1"
    printf "${GREEN}✔ Cleanup complete: $1 removed.${NC}\n"
  else
    printf "${YELLOW}✔ No $1 file found for cleanup.${NC}\n"
  fi
}

# Function to update /etc/hosts
update_hosts_file() {
  show_progress "Updating" "/etc/hosts file"
  HOSTS_FILE="/etc/hosts"
  HOST_ENTRY="127.0.0.1 accessible-archives.local"

  # Check if the entry already exists
  if grep -q "$HOST_ENTRY" "$HOSTS_FILE"; then
    printf "${GREEN}✔ Entry for accessible-archives.local already exists in $HOSTS_FILE.${NC}\n"
  else
    # Add the entry
    echo "$HOST_ENTRY" | sudo tee -a "$HOSTS_FILE" > /dev/null
    check_status "/etc/hosts file updated" "update /etc/hosts file"
  fi
}

# Update and upgrade packages
show_progress "Installing" "System Update"
sudo apt-get update -y
sudo apt-get upgrade -y
check_status "System Update installed" "install System Update"

# Install curl
show_progress "Installing" "Curl"
sudo apt-get install -y curl rsync git 
check_status "Curl installed" "install Curl"

# Install Pandoc
show_progress "Installing" "Pandoc and texlive"
sudo apt-get install pandoc texlive texlive-xetex texlive-fonts-recommended texlive-latex-extra -y
check_status "Pandoc and texlive installed" "install Pandoc and texlive"

# Install IPFS
if sudo systemctl is-active --quiet ipfs || [ -e $SCRIPT_DIR/we_are_in_docker ]; then
  printf "${GREEN}✔ IPFS already installed!.${NC}\n"
else
  show_progress "Installing" "IPFS"
  $SCRIPT_DIR/ipfs/install_ipfs.sh
  $SCRIPT_DIR/ipfs/setup_ipfs_systemd.sh
  # check_status "IPFS started" "start IPFS"
fi

# Install Python 3 and pip
show_progress "Installing" "Python3"
sudo apt-get install python3 python3-pip python3-virtualenv -y
check_status "Python3 installed" "install Python3"

# Install Python dependencies
show_progress "Installing" "Python Dependencies"
python3 -m virtualenv $PY_VENV_DIR
source $PY_VENV_DIR/bin/activate
check_status "Python Environment installed" "install Python Environment"
pip3 install -r $PY_REQUIREMENTS
check_status "Python Dependencies installed" "install Python Dependencies"



if sudo systemctl is-active --quiet ollama; then
  echo "Ollama is already installed and running."
else
  # Install Ollama
  show_progress "Installing" "Ollama"
  curl -fsSL https://ollama.com/install.sh -o $OLLAMA_INSTALL_SCRIPT
  chmod +x $OLLAMA_INSTALL_SCRIPT
  bash $OLLAMA_INSTALL_SCRIPT
  check_status "Ollama installed" "install Ollama"

  # Cleanup files
  cleanup_file $OLLAMA_INSTALL_SCRIPT
  if ! [ -e $SCRIPT_DIR/we_are_in_docker ];then

    # Initialize Ollama
    show_progress "Initializing" "Ollama"
    sudo systemctl daemon-reload
    sudo systemctl restart ollama
    sleep 5
    sudo systemctl is-active --quiet ollama
    check_status "Ollama initialized" "initialize Ollama"
  fi
fi

if [ -e $SCRIPT_DIR/we_are_in_docker ];then
  echo "Finished installing for docker."
  exit 0
fi

# Download Ollama model
show_progress "Pulling" "Ollama Model: llama3.1:8b"
ollama pull llama3.1:8b
check_status "Ollama Model: llama3.1:8b pulled" "pull Ollama Model: llama3.1:8b"

# show_progress "Pulling" "Ollama Model: qwen2:7b"
# ollama pull qwen2:7b
# check_status "Ollama Model: qwen2:7b pulled" "pull Ollama Model: qwen2:7b"
# # Download Ollama embedding model
show_progress "Pulling" "Ollama Model: mxbai-embed-large"
ollama pull mxbai-embed-large
check_status "Ollama Model: mxbai-embed-large pulled" "pull Ollama Model: mxbai-embed-large"

# Start Ollama as a background service
show_progress "Starting" "Ollama Service"
nohup ollama serve &> /dev/null &
check_status "Ollama Service started" "start Ollama Service"

# Update hosts file
# update_hosts_file

# # Install Nginx
# show_progress "Installing" "Nginx"
# sudo apt-get install nginx -y
# check_status "Nginx installed" "install Nginx"
#
# # Configure Nginx for the Streamlit app
# show_progress "Configuring" "Nginx"
# NGINX_CONF="/etc/nginx/sites-available/accessible-archives"
# cat <<EOF | sudo tee $NGINX_CONF
# server {
#     listen 80;
#     server_name accessible-archives.local;
#
#     location / {
#         proxy_pass http://localhost:8501;  # Default Streamlit port
#         proxy_set_header Host \$host;
#         proxy_set_header X-Real-IP \$remote_addr;
#         proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
#         proxy_set_header X-Forwarded-Proto \$scheme;
#     }
# }
# EOF
# check_status "Nginx configured" "configure Nginx"
#
# # Enable the Nginx configuration
# show_progress "Enabling" "Nginx"
# sudo ln -s $NGINX_CONF /etc/nginx/sites-enabled/
# check_status "Nginx enabled" "enable Nginx"
#
# # Test Nginx configuration and reload
# show_progress "Testing" "Nginx"
# sudo nginx -t
# check_status "Nginx tested" "test Nginx"
#
# # Reload Nginx
# show_progress "Reloading" "Nginx"
# sudo systemctl reload nginx
# check_status "Nginx reloaded" "reload Nginx"
#
# # Enable Nginx in firewall
# show_progress "Enabling" "Nginx in firewall"
# sudo ufw allow 'Nginx Full'
# check_status "Nginx in firewall enabled" "enable Nginx in firewall"

# Copy the entire project folder to ~/.local/share/
show_progress "Copying" "files"
rsync -XAva $PROJ_DIR $INSTALL_DIR/
check_status "Files copied" "copy files"

# Create symlink to run the app
show_progress "Creating" "symlink to run the app"
sudo ln -sf $SYMLINK_TARGET $SYMLINK_PATH
check_status "Symlink created" "create symlink"

if ! [ -e $SCRIPT_DIR/we_are_in_docker ];then
  # Create desktop entry
  show_progress "Creating" "desktop entry"

  cat <<EOF > $DESKTOP_ENTRY
  [Desktop Entry]
  Name=Accessible Archives
  Exec=$SYMLINK_PATH
  Icon=/home/$USERNAME/.local/share/AccessibleArchives/release/icon.png
  Terminal=true
  Type=Application
  Comment=RAG based Chat assistant
  Categories=Utility;
  EOF

  # Make the desktop entry executable
  chmod +x $DESKTOP_ENTRY
  check_status "Desktop entry created" "create desktop entry"
fi
printf "${GREEN}✔ Installation complete! You can now run 'accessible-archives' to start the app.${NC}\n"

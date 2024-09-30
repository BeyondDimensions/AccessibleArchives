#!/bin/bash
# Script for deploying the webui app

# Define text colors for output
GREEN="\033[0;32m"
RED="\033[0;31m"
YELLOW="\033[1;33m"
NC="\033[0m" # No color

# Function to show progress bar
show_progress() {
  printf "\n${YELLOW}Installing %s...${NC}\n" "$1"
}

# Function to check if a command succeeded or failed
check_status() {
  if [ $? -eq 0 ]; then
    printf "${GREEN}✔ %s installed successfully!${NC}\n" "$1"
  else
    printf "${RED}✘ Failed to install %s. Please check logs.${NC}\n" "$1"
    exit 1
  fi
}

# Function to clean up files
cleanup_file() {
  if [ -f "$1" ]; then
    rm "$1"
    printf "${GREEN}✔ Cleanup complete: $1 removed.${NC}\n"
  else
    printf "${YELLOW}✔ No $1 file found for cleanup.${NC}\n"
  fi
}

# Update and upgrade packages
show_progress "System Update"
sudo apt-get update -y
sudo apt-get upgrade -y
check_status "System Update"

# Install curl
show_progress "Curl"
sudo apt-get install curl -y
check_status "Curl"

# Install Python 3 and pip
show_progress "Python3"
sudo apt-get install python3 python3-pip python3-venv -y
check_status "Python3"

# Install Pandoc
show_progress "Pandoc and texlive"
sudo apt-get install pandoc texlive texlive-xetex texlive-fonts-recommended texlive-latex-extra -y
check_status "Pandoc and texlive"

# Install Ollama
show_progress "Ollama"
curl -fsSL https://ollama.com/install.sh -o install_ollama.sh
chmod +x install_ollama.sh
bash install_ollama.sh
check_status "Ollama"

# ollama_init
sudo systemctl daemon-reload
sudo systemctl restart ollama
sleep 5 #wait to start the service

# Download Ollama model
show_progress "Ollama Model: llama3.1:8b"
ollama pull llama3.1:8b
check_status "Ollama Model: llama3.1:8b"

# Download Ollama embedding model
show_progress "Ollama Model: mxbai-embed-large"
ollama pull mxbai-embed-large
check_status "Ollama Model: mxbai-embed-large"

# Start Ollama as a background service
show_progress "Ollama Service"
nohup ollama serve &> /dev/null &
check_status "Ollama Service"

# Install Python dependencies
show_progress "Python Dependencies"
python3 -m venv ../../.venv
source ../../.venv/bin/activate
pip3 install -r ../requirements.txt
check_status "Python Dependencies"

# Install Nginx
show_progress "Nginx"
sudo apt-get install nginx -y
check_status "Nginx"

# Configure Nginx for the Streamlit app
NGINX_CONF="/etc/nginx/sites-available/accessible-archives"
cat <<EOF | sudo tee $NGINX_CONF
server {
    listen 80;
    server_name accessible-archives.local;

    location / {
        proxy_pass http://127.0.0.1:8501;  # Default Streamlit port
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF
check_status "Nginx Configuration"

# Enable the Nginx configuration
sudo ln -s $NGINX_CONF /etc/nginx/sites-enabled/
check_status "Enable Nginx Site"

# Test Nginx configuration and reload
sudo nginx -t
check_status "Nginx Test"
sudo systemctl reload nginx
check_status "Nginx Reload"

# Create symlink to run the app
echo "Creating symlink to run the app..."
sudo ln -sf "$(pwd)/run_webui.sh" /usr/local/bin/accessible-archives
printf "${GREEN}✔ Symlink created successfully!${NC}"

cleanup_file "install_ollama.sh"

printf "\n${YELLOW}Copying files...${NC}\n"
# Create necessary directories
mkdir -p ~/.local/share/

# Copy the entire project folder to ~/.local/share/
cp -r "$(cd ../.. && pwd)" ~/.local/share/
printf "${GREEN}✔ Project directory copied to ~/.local/share/.${NC}"

printf "\n${YELLOW}Creating desktop entry...${NC}\n"

# Define the username
USERNAME=$(whoami)

# Define the desktop entry file
DESKTOP_ENTRY="$HOME/.local/share/applications/AccessibleArchives.desktop"

# Create desktop entry
cat <<EOF > "$DESKTOP_ENTRY"
[Desktop Entry]
Name=Accessible Archives
Exec=/home/$USERNAME/.local/share/AccessibleArchives/release/web/run_webui.sh
Icon=/home/$USERNAME/.local/share/AccessibleArchives/release/icon.png
Terminal=false
Type=Application
Comment=RAG based Chat assistant
Categories=Utility;
EOF

# Make the desktop entry executable
chmod +x "$DESKTOP_ENTRY"

printf "${GREEN}✔ Desktop entry created.${NC}\n"

printf "${GREEN}✔ Installation complete! You can now run 'accessible-archives' to start the app.${NC}\n"

printf "${YELLOW}✔ Access your app at http://accessible-archives.local${NC}\n"  # Inform the user about the access URL

#!/bin/bash
# the absolute path of this script's directory
script_dir="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
sudo cp $script_dir/accessible_archives.service /etc/systemd/system/

 
sudo systemctl enable accessible_archives
# sudo systemctl start accessible_archives

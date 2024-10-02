#!/bin/bash

# In this script, it matters with which user this script is being run, as that
# user is used to run the IPFS service
echo "[Unit]
Description=InterPlanetary FileSystem - the infrastructure of a P2P internet

[Service]
User=$USER
Environment=LIBP2P_TCP_REUSEPORT=false
ExecStart=ipfs daemon --enable-pubsub-experiment

[Install]
WantedBy=multi-user.target
" | sudo tee /etc/systemd/system/ipfs.service
sudo systemctl enable ipfs
sudo systemctl start ipfs

sleep 1
if systemctl is-active --quiet ipfs; then
  echo "Installation succeeded!"
else
  echo "Installation failed."
  exit 1
fi
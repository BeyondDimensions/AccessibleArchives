#!/bin/bash

cd $(mktemp -d)
git clone https://github.com/emendir/IPFS-Monitor
cat ./IPFS-Monitor/install_linux_systemd.sh | bash

echo "Installed IPFS-Monitor"
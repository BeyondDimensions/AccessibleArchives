#!/bin/bash

cd $(mktemp -d)
git clone https://github.com/emendir/IPFS-Monitor
./IPFS-Monitor/install_linux_systemd.sh
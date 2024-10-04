# create one-shot systemd service to run the IPFS initialisation script
echo "[Unit]
Description=Run the final installation steps for AccessibleArchives.
After=ipfs.service

[Service]
User=root
Type=oneshot
ExecStart=su root -c /opt/AccessibleArchives/release/docker/docker_first_run_installations.sh

[Install]
WantedBy=multi-user.target
" | tee /etc/systemd/system/final_installations.service

systemctl daemon-reload
systemctl enable final_installations
#!/bin/bash

exec > /var/log/user-data.log 2>&1

# Set up working directory
WORK_DIR=$HOME
cd $WORK_DIR

# Stop script if an error occurs
set -e

# Update package list with sudo
apt update -y

# Install necessary packages with sudo
apt install -y python3 python3-pip python3-venv curl git

# Clone repository
git clone https://github.com/Code4life-Labs/header-server.git

# Checkout to repository
cd header-server

# Create virtual environment for python
cd python
python3 -m venv venv
source venv/bin/activate

# Install python packages
pip install -r requirements.txt

# Setup service
cd ..
cp services/header.service /etc/systemd/system

# Start service
systemctl daemon-reload
systemctl start header.service

# Enable service
# Make sure the service start each time it reboot
systemctl enable header.service
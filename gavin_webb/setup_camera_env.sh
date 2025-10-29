#!/usr/bin/env bash
set -e
sudo apt update
sudo apt install -y python3-picamera2 python3-opencv python3-numpy rpicam-apps gpac unzip
mkdir -p "$HOME/media"
echo "✅ Camera environment ready!"

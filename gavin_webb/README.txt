Camera Scripts (Raspberry Pi 5 + Camera Module 3)
=================================================

1) take_photo.py      - Capture a single image to ~/media/photo_YYYYMMDD_HHMMSS.jpg
2) record_clip.py     - Record a short video for N seconds and auto-wrap to MP4 in ~/media/
3) setup_camera_env.sh- Installs required packages

Quick Start (VNC Drag & Drop)
-----------------------------
1. Drag 'camera_scripts.zip' into your Pi desktop (VNC Viewer).
2. Right-click ZIP > 'Extract Here'.
3. In terminal:
   cd ~/camera_scripts
   bash setup_camera_env.sh
   python3 take_photo.py
   python3 record_clip.py 8

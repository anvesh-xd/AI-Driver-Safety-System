from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput
from datetime import datetime
import subprocess, time, os, sys

duration_s = float(sys.argv[1]) if len(sys.argv) > 1 else 5.0

save_dir = os.path.expanduser("~/media")
os.makedirs(save_dir, exist_ok=True)

ts = datetime.now().strftime("%Y%m%d_%H%M%S")
h264_path = os.path.join(save_dir, f"clip_{ts}.h264")
mp4_path  = os.path.join(save_dir, f"clip_{ts}.mp4")

cam = Picamera2()
cam.configure(cam.create_video_configuration(main={"size": (1920, 1080)}))
encoder = H264Encoder(bitrate=6_000_000)
cam.start_recording(encoder, FileOutput(h264_path))
time.sleep(duration_s)
cam.stop_recording()

try:
    subprocess.run(["MP4Box", "-add", h264_path, "-new", mp4_path], check=True)
    print(f"✅ Saved: {mp4_path}")
except Exception as e:
    print(f"⚠️ MP4 wrap failed: {e}")

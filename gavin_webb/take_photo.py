from picamera2 import Picamera2
from datetime import datetime
import time, os

save_dir = os.path.expanduser("~/media")
os.makedirs(save_dir, exist_ok=True)

picam2 = Picamera2()
picam2.configure(picam2.create_still_configuration())
picam2.start()
time.sleep(0.5)

ts = datetime.now().strftime("%Y%m%d_%H%M%S")
out_path = os.path.join(save_dir, f"photo_{ts}.jpg")
picam2.capture_file(out_path)
picam2.stop()
print(f"✅ Saved: {out_path}")

import time
import cv2
import numpy as np
from ultralytics import YOLO

# ===== CONFIGURATION =====
MODEL_PATH = "best.pt"     # change to your model
SOURCE = 0                 # 0 = default camera, or use /dev/video0
CONF_THRESH = 0.5

# Load once (IMPORTANT for performance)
model = YOLO(MODEL_PATH, task='detect')
labels = model.names

def run(queue):
    cap = cv2.VideoCapture(SOURCE)

    if not cap.isOpened():
        print("ERROR: Camera failed to open")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        results = model(frame, verbose=False)
        detections = results[0].boxes

        objects = []

        for det in detections:
            conf = float(det.conf.item())
            if conf < CONF_THRESH:
                continue

            classidx = int(det.cls.item())
            classname = labels[classidx]

            xyxy = det.xyxy.cpu().numpy().squeeze()
            xmin, ymin, xmax, ymax = xyxy.astype(int)

            objects.append({
                "label": classname,
                "confidence": conf,
                "bbox": [xmin, ymin, xmax, ymax],

                # Placeholder distance (replace later if using depth)
                "distance": 999
            })

        output = {
            "objects": objects,
            "timestamp": time.time()
        }

        # Prevent queue backlog (VERY important)
        if queue.full():
            try:
                queue.get_nowait()
            except:
                pass

        queue.put(output)

        time.sleep(0.01)   # small yield to avoid CPU saturation

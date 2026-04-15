import time
import numpy as np
from ultralytics import YOLO
from picamera2 import Picamera2

MODEL_PATH = "best.pt"
CONF_THRESH = 0.5

model = YOLO(MODEL_PATH, task='detect')
labels = model.names

def run(queue):
    picam2 = Picamera2()
    config = picam2.create_preview_configuration(main={"format": "RGB888", "size": (640, 480)})
    picam2.configure(config)
    picam2.start()
    time.sleep(2)
    print("Pi Camera started", flush=True)

    while True:
        frame = picam2.capture_array()
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
                "distance": 999
            })
        output = {
            "objects": objects,
            "timestamp": time.time()
        }
        if queue.full():
            try:
                queue.get_nowait()
            except:
                pass
        queue.put(output)
        time.sleep(0.01)

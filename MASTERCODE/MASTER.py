import time
import multiprocessing as mp
import queue
import random
import math

# =========================
# GPS PROCESS
# =========================
def gps_process(gps_queue):
    """
    Simulates GPS data.
    Replace with real GPS reading code later.
    """
    while True:
        gps_data = {
            "lat": 40.7128 + random.uniform(-0.0001, 0.0001),
            "lon": -74.0060 + random.uniform(-0.0001, 0.0001),
            "speed": random.uniform(0, 20),      # m/s
            "heading": random.uniform(0, 360),    # degrees
            "timestamp": time.time()
        }
        gps_queue.put(gps_data)
        time.sleep(0.2)  # 5 Hz update rate


# =========================
# GYROSCOPE PROCESS
# =========================
def gyro_process(gyro_queue):
    """
    Simulates gyroscope/IMU data.
    Replace with real IMU sensor reads.
    """
    while True:
        gyro_data = {
            "yaw": random.uniform(-math.pi, math.pi),
            "pitch": random.uniform(-0.2, 0.2),
            "roll": random.uniform(-0.2, 0.2),
            "turn_rate": random.uniform(-1.0, 1.0),
            "timestamp": time.time()
        }
        gyro_queue.put(gyro_data)
        time.sleep(0.05)  # 20 Hz update rate


# =========================
# YOLO PROCESS
# =========================
def yolo_process(yolo_queue):
    """
    Simulates YOLO object detection output.
    Replace with real camera + YOLO inference.
    """
    labels = ["car", "pedestrian", "bicycle", "none"]

    while True:
        detected_objects = []

        # Random chance of detecting something
        if random.random() < 0.6:
            label = random.choice(labels[:-1])
            detected_objects.append({
                "label": label,
                "confidence": round(random.uniform(0.6, 0.95), 2),
                "x": random.randint(0, 640),
                "y": random.randint(0, 480),
                "distance": random.uniform(2, 30)  # meters
            })

        yolo_data = {
            "objects": detected_objects,
            "timestamp": time.time()
        }

        yolo_queue.put(yolo_data)
        time.sleep(0.1)  # ~10 FPS


# =========================
# AUDIO PROCESS
# =========================
def audio_process(audio_queue):
    """
    Receives alert messages and plays audio.
    Replace print() with TTS or audio playback.
    """
    while True:
        try:
            alert = audio_queue.get(timeout=1)
            print(f"[AUDIO ALERT] {alert['message']}")
        except queue.Empty:
            pass


# =========================
# FUSION / DECISION LOGIC
# =========================
def fusion_loop(gps_queue, gyro_queue, yolo_queue, audio_queue):
    """
    Central brain of the system.
    """
    latest_gps = None
    latest_gyro = None
    latest_yolo = None

    last_alert_time = 0
    ALERT_COOLDOWN = 3  # seconds

    while True:
        # ---- Read GPS data ----
        try:
            while True:
                latest_gps = gps_queue.get_nowait()
        except queue.Empty:
            pass

        # ---- Read Gyro data ----
        try:
            while True:
                latest_gyro = gyro_queue.get_nowait()
        except queue.Empty:
            pass

        # ---- Read YOLO data ----
        try:
            while True:
                latest_yolo = yolo_queue.get_nowait()
        except queue.Empty:
            pass

        # ---- Decision logic ----
        if latest_gps and latest_gyro and latest_yolo:
            speed = latest_gps["speed"]
            objects = latest_yolo["objects"]

            for obj in objects:
                if obj["label"] == "pedestrian":
                    if speed > 3 and obj["distance"] < 15:
                        now = time.time()
                        if now - last_alert_time > ALERT_COOLDOWN:
                            audio_queue.put({
                                "type": "alert",
                                "priority": "high",
                                "message": "Warning: Pedestrian ahead"
                            })
                            last_alert_time = now

        time.sleep(0.02)  # main loop ~50 Hz


# =========================
# MAIN ENTRY POINT
# =========================
def main():
    mp.set_start_method("spawn")  # safer on Raspberry Pi

    gps_queue = mp.Queue()
    gyro_queue = mp.Queue()
    yolo_queue = mp.Queue()
    audio_queue = mp.Queue()

    processes = [
        mp.Process(target=gps_process, args=(gps_queue,), daemon=True),
        mp.Process(target=gyro_process, args=(gyro_queue,), daemon=True),
        mp.Process(target=yolo_process, args=(yolo_queue,), daemon=True),
        mp.Process(target=audio_process, args=(audio_queue,), daemon=True),
    ]

    for p in processes:
        p.start()

    print("System started. Fusion loop running.")

    try:
        fusion_loop(gps_queue, gyro_queue, yolo_queue, audio_queue)
    except KeyboardInterrupt:
        print("Shutting down system...")
        for p in processes:
            p.terminate()


if __name__ == "__main__":
    main()

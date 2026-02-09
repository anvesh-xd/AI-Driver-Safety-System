import time
import multiprocessing as mp
import queue

import gps_module
import gyro_module
import yolo_module
import audio_module


def fusion_loop(gps_q, gyro_q, yolo_q, audio_q):
    latest = {
        "gps": None,
        "gyro": None,
        "yolo": None
    }

    last_alert = 0
    ALERT_COOLDOWN = 3  # seconds

    while True:
        # ---- Drain queues (always keep newest data) ----
        for name, q in [("gps", gps_q), ("gyro", gyro_q), ("yolo", yolo_q)]:
            try:
                while True:
                    latest[name] = q.get_nowait()
            except queue.Empty:
                pass

        # ---- Decision logic ----
        if all(latest.values()):
            speed = latest["gps"]["speed"]
            objects = latest["yolo"]["objects"]

            for obj in objects:
                if obj["label"] == "pedestrian":
                    if speed > 3 and obj["distance"] < 15:
                        now = time.time()
                        if now - last_alert > ALERT_COOLDOWN:
                            audio_q.put({
                                "type": "alert",
                                "message": "Warning: Pedestrian ahead",
                                "priority": "high"
                            })
                            last_alert = now

        time.sleep(0.02)  # ~50 Hz


def main():
    mp.set_start_method("spawn")

    gps_q = mp.Queue(maxsize=5)
    gyro_q = mp.Queue(maxsize=5)
    yolo_q = mp.Queue(maxsize=2)
    audio_q = mp.Queue()

    processes = [
        mp.Process(target=gps_module.run, args=(gps_q,), daemon=True),
        mp.Process(target=gyro_module.run, args=(gyro_q,), daemon=True),
        mp.Process(target=yolo_module.run, args=(yolo_q,), daemon=True),
        mp.Process(target=audio_module.run, args=(audio_q,), daemon=True),
    ]

    for p in processes:
        p.start()

    print("Master system running")

    try:
        fusion_loop(gps_q, gyro_q, yolo_q, audio_q)
    except KeyboardInterrupt:
        print("Shutting down...")
        for p in processes:
            p.terminate()


if __name__ == "__main__":
    main()

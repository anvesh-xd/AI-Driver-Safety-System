import time
import multiprocessing as mp
import queue

import gps_module
import gyro_module
import yolo_module
import audio_module


def fusion_loop(gps_q, gyro_q, yolo_q, audio_q):
    import time
    import queue

    latest = {"gps": None, "gyro": None, "yolo": None}

    last_alert_time = {}
    ALERT_COOLDOWN = 3.0      # seconds per alert type

    def can_alert(alert_name):
        now = time.time()
        if alert_name not in last_alert_time:
            last_alert_time[alert_name] = 0
        if now - last_alert_time[alert_name] > ALERT_COOLDOWN:
            last_alert_time[alert_name] = now
            return True
        return False

    while True:

        # ---- Drain queues (keep freshest data) ----
        for name, q in [("gps", gps_q), ("gyro", gyro_q), ("yolo", yolo_q)]:
            try:
                while True:
                    latest[name] = q.get_nowait()
            except queue.Empty:
                pass

        if all(latest.values()):

            speed = latest["gps"]["speed_mph"] or 0
            sudden_motion = latest["gyro"]["sudden_motion"]
            objects = latest["yolo"]["objects"]

            pedestrian_close = False
            vehicle_close = False

            for obj in objects:
                label = obj["label"]

                # Distance placeholder logic
                distance = obj.get("distance", 999)

                if label == "pedestrian" and distance < 15:
                    pedestrian_close = True

                if label in ["car", "truck", "bus"] and distance < 10:
                    vehicle_close = True

            # ================================
            # RULE SET
            # ================================

            # ---- Pedestrian Risk ----
            if pedestrian_close:

                if speed > 20:
                    if can_alert("pedestrian_critical"):
                        audio_q.put({
                            "type": "alert",
                            "priority": "critical",
                            "message": "CRITICAL WARNING. Pedestrian ahead."
                        })

                elif speed > 5:
                    if can_alert("pedestrian_warning"):
                        audio_q.put({
                            "type": "alert",
                            "priority": "high",
                            "message": "Warning. Pedestrian ahead."
                        })

            # ---- Sudden Motion Detection ----
            if sudden_motion and speed > 10:
                if can_alert("sudden_motion"):
                    audio_q.put({
                        "type": "alert",
                        "priority": "high",
                        "message": "Warning. Abrupt vehicle movement detected."
                    })

            # ---- Forward Vehicle Proximity ----
            if vehicle_close and speed > 10:
                if can_alert("vehicle_close"):
                    audio_q.put({
                        "type": "alert",
                        "priority": "medium",
                        "message": "Caution. Vehicle ahead."
                    })

            # ---- High Speed Advisory ----
            if speed > 35:
                if can_alert("overspeed"):
                    audio_q.put({
                        "type": "alert",
                        "priority": "low",
                        "message": "Reduce speed."
                    })

        time.sleep(0.02)



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

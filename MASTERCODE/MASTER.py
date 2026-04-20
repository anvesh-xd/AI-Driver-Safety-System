
import time
import multiprocessing as mp
import queue

import gps_module
import gyro_module
import yolo_module
import audio_module1 as audio_module


def fusion_loop(gps_q, gyro_q, yolo_q, audio_q):
    import time
    import queue

    latest = {"gps": None, "gyro": None, "yolo": None}

    last_alert_time = {}
    ALERT_COOLDOWN = 6.7      # seconds per alert type
    speed_limit = 100
    speed_last = -1

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

        gps_data = latest["gps"] or {}
        gyro_data = latest["gyro"] or {}
        yolo_data = latest["yolo"] or {}
        speed = gps_data.get("speed_mph", 0)
        sudden_motion = gyro_data.get("sudden_motion", False)
        delta = gyro_data.get("delta", 0)
        objects = yolo_data.get("objects", []) or []
        pedestrian_close = False
        vehicle_close = False
        stop_close = False
        red_light_close = False

        for obj in objects:
            label = obj["label"]
            
            # Distance placeholder logic
            distance = obj.get("distance", 999)
            
            if label == "Speed Limit 5":
                speed_limit = 5;
            if label == "Speed Limit 10":
                speed_limit = 10;
            if label == "Speed Limit 15":
                speed_limit = 15;
            if label == "Speed Limit 20":
                speed_limit = 20;
            if label == "Speed Limit 25":
                speed_limit = 25;
            if label == "Speed Limit 30":
                speed_limit = 30;
            if label == "Speed Limit 35":
                speed_limit = 35;
            if label == "Speed Limit 40":
                speed_limit = 40;
            if label == "Speed Limit 45":
                speed_limit = 45;
            if label == "Speed Limit 50":
                speed_limit = 50;
            if label == "Speed Limit 55":
                speed_limit = 55;
            if label == "Speed Limit 60":
                speed_limit = 60
            if label == "Speed Limit 65":
                speed_limit = 65;
            if label == "Speed Limit 70":
                speed_limit = 70;
            if label == "Speed Limit 75":
                speed_limit = 75;
            if label == "Speed Limit 80":
                speed_limit = 80;
            if label == "Stop":
                stop_close = True
            if label == "Red Light":
                red_light_close = True
        # ===============================
        # RULE SET
        # ================================
        
        # ---- Sudden Motion Detection ----
        if sudden_motion:
            if can_alert("sudden_motion"):
                print("Sudden Motion:", delta)
                audio_q.put({
                    "type": "alert",
                    "priority": "high",
                    "message": "Warning. Abrupt vehicle movement detected."
                })
                
        # ---- High Speed Advisory ----
        if speed > 20:
            if can_alert("overspeed"):
                audio_q.put({
                    "type": "alert",
                    "priority": "low",
                    "message": "Reduce speed."
                })
                
        # ---- Stop Sign Ahead ----
        if stop_close:
            if can_alert("Stop_Sign"):
                print("Stop sign detected")
                audio_q.put({
                    "type": "alert",
                    "priority": "high",
                    "message": "Warning. Stop sign detected."
                })
                        
        # ---- Red Light Ahead ----
        if red_light_close:
            if can_alert("Red_Light"):
                print("Red light detected")
                audio_q.put({
                    "type": "alert",
                    "priority": "high",
                    "message": "Warning. Traffic light detected."
                })
                
        if(speed >= speed_last + 1 or speed <= speed_last - 1):
            print("Speed:",speed)
            speed_last = speed
            
        time.sleep(1)



import time

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
    speed_limit = 100

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

        gps_data = latest["gps"] or {}
        gyro_data = latest["gyro"] or {}
        yolo_data = latest["yolo"] or {}
        speed = gps_data.get("speed_mph", 0)
        sudden_motion = gyro_data.get("sudden_motion", False)
        delta = gyro_data.get("delta", 0)
        objects = yolo_data.get("objects", []) or []
        pedestrian_close = False
        vehicle_close = False
        stop_close = False

        for obj in objects:
            label = obj["label"]
            
            # Distance placeholder logic
            distance = obj.get("distance", 999)
            
            if label == "Speed Limit 5":
                speed_limit = 5;
            if label == "Speed Limit 10":
                speed_limit = 10;
            if label == "Speed Limit 15":
                speed_limit = 15;
            if label == "Speed Limit 20":
                speed_limit = 20;
            if label == "Speed Limit 25":
                speed_limit = 25;
            if label == "Speed Limit 30":
                speed_limit = 30;
            if label == "Speed Limit 35":

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
    speed_limit = 100

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

        gps_data = latest["gps"] or {}
        gyro_data = latest["gyro"] or {}
        yolo_data = latest["yolo"] or {}
        speed = gps_data.get("speed_mph", 0)
        sudden_motion = gyro_data.get("sudden_motion", False)
        delta = gyro_data.get("delta", 0)
        objects = yolo_data.get("objects", []) or []
        pedestrian_close = False
        vehicle_close = False
        stop_close = False

        for obj in objects:
            label = obj["label"]
            
            # Distance placeholder logic
            distance = obj.get("distance", 999)
            
            if label == "Speed Limit 5":
                speed_limit = 5;
            if label == "Speed Limit 10":
                speed_limit = 10;
            if label == "Speed Limit 15":
                speed_limit = 15;
            if label == "Speed Limit 20":
                speed_limit = 20;
            if label == "Speed Limit 25":
                speed_limit = 25;
            if label == "Speed Limit 30":
                speed_limit = 30;
            if label == "Speed Limit 35":


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

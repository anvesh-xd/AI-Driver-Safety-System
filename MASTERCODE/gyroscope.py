from mpu6050 import mpu6050
import time
import numpy as np

# Initialize MPU6050
sensor = mpu6050(0x68)

# --- Configuration ---
SAMPLE_INTERVAL = 0.05     # 20 Hz
THRESHOLD = 750.0          # sudden change trigger

def run(queue):
    previous_gyro = np.array([0.0, 0.0, 0.0])

    while True:
        try:
            gyro_data = sensor.get_gyro_data()
            gx, gy, gz = gyro_data['x'], gyro_data['y'], gyro_data['z']

            current_gyro = np.array([gx, gy, gz])

            # Magnitude of change
            delta = np.linalg.norm(current_gyro - previous_gyro)

            previous_gyro = current_gyro

            output = {
                "gx": gx,
                "gy": gy,
                "gz": gz,
                "delta": delta,
                "sudden_motion": delta > THRESHOLD,
                "timestamp": time.time()
            }

            # Prevent queue overflow (important on Pi)
            if queue.full():
                try:
                    queue.get_nowait()
                except:
                    pass

            queue.put(output)

            time.sleep(SAMPLE_INTERVAL)

        except Exception:
            time.sleep(0.1)

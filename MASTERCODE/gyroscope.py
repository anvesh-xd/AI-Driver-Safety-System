from mpu6050 import mpu6050
import time
import numpy as np

# Initialize MPU6050 (I2C address 0x68)
sensor = mpu6050(0x68)

# --- Configuration ---
SAMPLE_INTERVAL = 0.05   # seconds between readings
THRESHOLD = 500.0        # degrees/sec change to trigger alert
previous_gyro = np.array([0.0, 0.0, 0.0])

print("Monitoring gyro data for sudden momentum changes...\n")

while True:
    try:
        # Read gyro data (angular velocity in deg/s)
        gyro_data = sensor.get_gyro_data()
        gx, gy, gz = gyro_data['x'], gyro_data['y'], gyro_data['z']

        # Current gyro vector
        current_gyro = np.array([gx, gy, gz])

        # Compute magnitude of change (delta)
        delta = np.linalg.norm(current_gyro - previous_gyro)

        # Update previous reading
        previous_gyro = current_gyro

        # Detect sudden movement
        if delta > THRESHOLD:
            print(f"⚠️ Sudden change detected! Δ={delta:.1f}°/s "
                  f"(gx={gx:.1f}, gy={gy:.1f}, gz={gz:.1f})")

        # Optional: print running data
        # print(f"Gyro: X={gx:.2f}, Y={gy:.2f}, Z={gz:.2f}, Δ={delta:.1f}")

        time.sleep(SAMPLE_INTERVAL)

    except KeyboardInterrupt:
        print("\nStopped by user.")
        break
    except Exception as e:
        print("Error:", e)
        time.sleep(0.5)

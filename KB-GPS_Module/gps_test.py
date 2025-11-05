import serial
import pynmea2

//ser = serial.Serial('/dev/serial0', 9600, timeout=1)
ser = serial.Serial('/dev/ttyAMA0’, 9600, timeout=1)

while True:
    try:
        line = ser.readline().decode('ascii', errors='replace')
        if line.startswith('$GPGGA'):
            msg = pynmea2.parse(line)
            print(f"Lat: {msg.latitude}, Lon: {msg.longitude}, Alt: {msg.altitude}")
    except Exception as e:
        print("Error:", e)

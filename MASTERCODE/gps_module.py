
import serial
import pynmea2
import time

# Connect to GPS module
ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)

# Global variables
latitude = None
longitude = None
altitude = None
speed_knots = None
speed_over_grnd = None

def parse_nmea_sentence(sentence):
    global latitude, longitude, altitude, speed_knots, speed_over_grnd
    try:
        msg = pynmea2.parse(sentence)
        if msg.talker == 'GP':  # GPS talker
            if isinstance(msg, pynmea2.types.talker.GGA):
                latitude = msg.latitude
                longitude = msg.longitude
                altitude = msg.altitude
            elif isinstance(msg, pynmea2.types.talker.RMC):
                speed_over_grnd = msg.spd_over_grnd
            elif isinstance(msg, pynmea2.types.talker.VTG):
                speed_knots = msg.spd_over_grnd_kts
    except pynmea2.ParseError:
        pass  # ignore errors

def get_gps_data():
    """Return structured GPS data for master program"""
    return {
        "latitude": latitude,
        "longitude": longitude,
        "altitude": altitude,
        "speed_knots": speed_knots,
        "speed_mph": speed_knots * 1.15078 if speed_knots else None,
        "speed_over_grnd": speed_over_grnd,
        "timestamp": time.time()
    }

# ======== Multiprocessing-compatible entry point ========
def run(queue):
    """Run loop for Option A master"""
    while True:
        line = ser.readline().decode('ascii', errors='replace').strip()
        parse_nmea_sentence(line)
        # Only push if we have a valid fix
        if latitude and longitude:
            data = get_gps_data()
            if queue.full():
                try:
                    queue.get_nowait()  # remove oldest if full
                except:
                    pass
            queue.put(data)

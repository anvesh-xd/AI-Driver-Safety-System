#Windows vscode powershell, activate venv using .venv\Scripts\Activate.ps1
import serial
import pynmea2

ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=1) #Connect to GPS module via serial port [UART0, GPIO 14/15], 9600 baud rate

#global variables for important data including latitude, longitude, altitude, speed in knots
speed_kph = None
speed_mph = None
enable_print = True  #Enable or disable printing of data
print_raw = False #Print raw nmea message


def read_VTG(msg): #Course Over Ground and Ground Speed
    if isinstance(msg, pynmea2.types.talker.VTG):
        if enable_print:
            print(f"Speed (km/h): {msg.spd_over_grnd_kmph}\n Speed (m/h):{kph_to_mph(msg.spd_over_grnd_kmph)}\n")
        global speed_knots, speed_mph #Update global variable
        speed_kph = msg.spd_over_grnd_kmph
        speed_mph = kph_to_mph(msg.spd_over_grnd_kmph)
     
#Convert speed units
def kph_to_mph(kph):
    if kph:
        return kph * 0.621371
    return None

#Parse NMEA sentence and call appropriate functions
def parse_nmea_sentence(sentence):
    try:
        msg = pynmea2.parse(sentence)
        if isinstance(msg, pynmea2.types.talker.VTG):
            read_VTG(msg)
    except pynmea2.ParseError as e:
        print("Parse error:", e)

#Continuously read from serial port
while True:
    line = ser.readline().decode('ascii', errors='replace')
    if print_raw:
        print(f"Raw NMEA Sentence: {line.strip()}\n")
    parse_nmea_sentence(line)
    #print(f"Location: {get_location()}\n")


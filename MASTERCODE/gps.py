#Windows vscode powershell, activate venv using .venv\Scripts\Activate.ps1
import serial
import pynmea2

ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=1) #Connect to GPS module via serial port [UART0, GPIO 14/15], 9600 baud rate

#global variables for important data including latitude, longitude, altitude, speed in knots
latitude = None
longitude = None
altitude = None
speed_knots = None
speed_over_grnd = None

enable_print = True  #Enable or disable printing of data
print_raw = False #Print raw nmea message



#Currently using GGA, GSA, GSV, RMC, and VTG NMEA sentences

#Get latitude, longitude, and altitude from GGA message
def read_GGA(msg): #Global Positioning System Fix Data
    if isinstance(msg, pynmea2.types.talker.GGA):
        if enable_print:
            print(f"Latitude: {msg.latitude}, Longitude: {msg.longitude}, Altitude: {msg.altitude}\n")
        global latitude, longitude, altitude #Update global variables
        latitude = msg.latitude
        longitude = msg.longitude
        altitude = msg.altitude

#Get DOP and active satellites from GSA message
def read_GSA(msg): #GNSS DOP and Active Satellites
    if isinstance(msg, pynmea2.types.talker.GSA):
        if enable_print:
            print(f"DOP: {msg.pdop}, Active Satellites: {msg.sv_id01},  {msg.sv_id01},  {msg.sv_id02},  {msg.sv_id03},  {msg.sv_id04}\n") #Can go up to 12

#Get number of satellites in view and their PRNs from GSV message
def read_GSV(msg): #GNSS Satellites in View
    if isinstance(msg, pynmea2.types.talker.GSV):
        if enable_print:
            print(f"Satellites in View: {msg.num_sv_in_view}, Satellite PRNs: {msg.sv_prn_num_1}, {msg.sv_prn_num_2}, {msg.sv_prn_num_3}, {msg.sv_prn_num_4}\n")

#Get speed over ground and true course from RMC message
def read_RMC(msg): #Recommended Minimum Specific GPS/Transit Data
    if isinstance(msg, pynmea2.types.talker.RMC):
        if enable_print:
            print(f"Speed: {msg.spd_over_grnd}, True Course: {msg.true_course}\n")
        global speed_over_grnd #Update global variable
        speed_over_grnd = msg.spd_over_grnd

#Get speed kilometers per hour and speed knots from VTG message
def read_VTG(msg): #Course Over Ground and Ground Speed
    if isinstance(msg, pynmea2.types.talker.VTG):
        if enable_print:
            print(f"Speed (m/h): {kph_to_mph(msg.spd_over_grnd_kmph)} Speed (km/h): {msg.spd_over_grnd_kmph}, Speed (knots): {msg.spd_over_grnd_kts}\n")
        global speed_knots #Update global variable
        speed_knots = msg.spd_over_grnd_kts

#Check talker ID, should be 'GP' for GPS
def get_talker_id(msg):
    return msg.talker

#Convert speed units
def knots_to_mph(knots):
    if knots:
        return knots * 1.15078
    return None
def kph_to_mph(kph):
    if kph:
        return kph * 0.621371
    return None


#Important Gets
def get_latitude():
    return latitude
def get_longitude():
    return longitude
def get_location(): #Returns formatted latitude and longitude
    return "{}, {}".format(latitude, longitude) 
def get_altitude():
    return altitude
def get_speed_knots():
    return speed_knots
def get_speed_mph():
    if speed_knots is not None:
        return knots_to_mph(speed_knots)
    return None


#Parse NMEA sentence and call appropriate functions
def parse_nmea_sentence(sentence):
    try:
        msg = pynmea2.parse(sentence)
        talker_id = get_talker_id(msg)
        if talker_id == 'GP':
            read_GGA(msg)
            read_GSA(msg)
            read_GSV(msg)
            read_RMC(msg)
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



"""
#Get speed over ground and true course from RMC message
def read_RMC(msg): #Recommended Minimum Specific GPS/Transit Data
    if isinstance(msg, pynmea2.types.talker.RMC):
        if enable_print:
            print(f"Speed: {msg.spd_over_grnd}, True Course: {msg.true_course}\n")
        global speed_over_grnd #Update global variable
        speed_over_grnd = msg.spd_over_grnd



parse_nmea_sentence(line)
try:
        msg = pynmea2.parse(sentence)
        talker_id = get_talker_id(msg)
        if talker_id == 'GP':
            read_RMC(msg)
    except pynmea2.ParseError as e:
        print("Parse error:", e)

while True:
    line = ser.readline().decode('ascii', errors='replace')

"""
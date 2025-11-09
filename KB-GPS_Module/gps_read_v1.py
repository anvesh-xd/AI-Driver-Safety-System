#Windows vscode powershell, activate venv using .venv\Scripts\Activate.ps1
import serial
import pynmea2

ser = serial.Serial('/dev/serial0', 9600, timeout=1) #Connect to GPS module via serial port [UART0, GPIO 14/15], 9600 baud rate


#Currently using GGA, GSA, GSV, RMC, and VTG NMEA sentences

#Get latitude, longitude, and altitude from GGA message
def read_GGA(msg): #Global Positioning System Fix Data
    if isinstance(msg, pynmea2.types.talker.GGA):
        print(f"Latitude: {msg.latitude}, Longitude: {msg.longitude}, Altitude: {msg.altitude}\n")

#Get DOP and active satellites from GSA message
def read_GSA(msg): #GNSS DOP and Active Satellites
    if isinstance(msg, pynmea2.types.talker.GSA):
        print(f"DOP: {msg.pdop}, Active Satellites: {msg.sv_id_1}, {msg.sv_id_2}, {msg.sv_id_3}, {msg.sv_id_4}, {msg.sv_id_5}, {msg.sv_id_6}, {msg.sv_id_7}, {msg.sv_id_8}, {msg.sv_id_9}, {msg.sv_id_10}, {msg.sv_id_11}, {msg.sv_id_12}\n")

#Get number of satellites in view and their PRNs from GSV message
def read_GSV(msg): #GNSS Satellites in View
    if isinstance(msg, pynmea2.types.talker.GSV):
        print(f"Satellites in View: {msg.num_sv_in_view}, Satellite PRNs: {msg.sv_prn_num_1}, {msg.sv_prn_num_2}, {msg.sv_prn_num_3}, {msg.sv_prn_num_4}, {msg.sv_prn_num_5}, {msg.sv_prn_num_6}, {msg.sv_prn_num_7}, {msg.sv_prn_num_8}\n")

#Get speed over ground and true course from RMC message
def read_RMC(msg): #Recommended Minimum Specific GPS/Transit Data
    if isinstance(msg, pynmea2.types.talker.RMC):
        print(f"Speed: {msg.spd_over_grnd}, True Course: {msg.true_course}\n")

#Get speed kilometers per hour and speed knots from VTG message
def read_VTG(msg): #Course Over Ground and Ground Speed
    if isinstance(msg, pynmea2.types.talker.VTG):
        print(f"Speed (m/h): {knots_to_mph(msg.spd_knots)}, Speed (km/h): {msg.spd_kmph}, Speed (knots): {msg.spd_knots}\n")

#Check talker ID, should be 'GP' for GPS
def get_talker_id(msg):
    return msg.talker

#Convert speed units
def knots_to_mph(knots):
    return knots * 1.15078
def kph_to_mph(kph):
    return kph * 0.621371


#Important Gets
def get_Lat_Long(msg): #Get Latitude and Longitude from GGA message
    if isinstance(msg, pynmea2.types.talker.GGA):
        return msg.latitude, msg.longitude
    return None, None
def get_Altitude(msg): #Get Altitude from GGA message
    if isinstance(msg, pynmea2.types.talker.GGA):
        return msg.altitude
    return None
def get_speed_knots(msg): #Get Speed in knots from RMC message
    if isinstance(msg, pynmea2.types.talker.RMC):
        return msg.spd_over_grnd
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
    print("NMEA Sentence:", line.strip(), "\n")
    parse_nmea_sentence(line)



import machine
import utime

uart = machine.UART(2, baudrate=9600, tx=17, rx=16)

def get_gps_data():
    while True:
        if uart.any():
            gps_data = uart.readline()
            if gps_data:
                try:
                    decoded = gps_data.decode('utf-8')
                    if "$GPGGA" in decoded or "$GPRMC" in decoded:
                        lat, lon = parse_gps(decoded)
                        if lat and lon:
                            print("Latitude:", lat, "Longitude:", lon)
                except UnicodeError:
                    pass
        utime.sleep(1)

def parse_gps(data):
    parts = data.split(',')
    if len(parts) > 5 and parts[2] and parts[4]:
        lat = convert_to_degrees(parts[2])
        lon = convert_to_degrees(parts[4])
        if parts[3] == 'S':
            lat = -lat
        if parts[5] == 'W':
            lon = -lon
        return lat, lon
    return None, None

def convert_to_degrees(raw_value):
    degrees = int(float(raw_value) / 100)
    minutes = float(raw_value) - (degrees * 100)
    return degrees + (minutes / 60)

get_gps_data()

import serial
import time

from src.bike import Bike

class GpsModule:

    def __init__(self, isRealData=False, bike=Bike):
        self.isRealData = isRealData
        self.serial_port = "/dev/ttyS0" 
        self.bike = bike
        if self.isRealData:
            self.ser = serial.Serial(self.serial_port, 9600, timeout=1)

    def send_at_command(self, command):
        command += '\r\n'
        self.ser.write(command.encode('utf-8'))
        time.sleep(1)
        self.print_serial_data()
        
    def send_at_command_no_response(self, command):
        command += '\r\n'
        self.ser.write(command.encode('utf-8'))
        time.sleep(2)

    def print_serial_data(self):
        while self.ser.in_waiting != 0:
            print(self.ser.read().decode('utf-8'), end='')
            
    def parse_gps_line(self):
        while self.ser.in_waiting != 0:
            gps_line = self.ser.readline().decode('utf-8')
            parts = gps_line.split(',')
            if len(parts) >= 8 and parts[0] == "$GPRMC" and parts[2] == 'A':
                # Latitude parsing
                latitude = float(parts[3][:2]) + float(parts[3][2:]) / 60
                if parts[4] == 'S':
                    latitude = -latitude

                # Longitude parsing
                longitude = float(parts[5][:3]) + float(parts[5][3:]) / 60
                if parts[6] == 'W':
                    longitude = -longitude

                # Save latitude and longitude to class attributes
                self.latitude = latitude
                self.longitude = longitude

                # Speed parsing
                speed_knots = float(parts[7])
                
                speed_kmh = speed_knots * 1.852
                self.speed = speed_kmh
            else:
                return None
            
        return None
    
    def run_sim808(self, useRealData):
        if useRealData:
            try:
                # Send AT command
                # print("AT command sent")

                self.send_at_command("AT")
                
                # print("power command sent")
                # Turn on GPS
                self.send_at_command("AT+CGPSPWR=1")
                
                self.send_at_command("AT+CGPSOUT=32")

                # Check GPS status
                self.send_at_command("AT+CGPSSTATUS?")
                
                while True:
                    self.parse_gps_line()
                    print(f"Latitude: {self.latitude}, Longitude: {self.longitude}, Speed: {self.speed}")
                    time.sleep(2)
                
                while False:
                    # send_at_command("AT+CGPSSTATUS?")
                    self.send_at_command("AT+CGPSINF=0")
                    
                    # response: +CGPSINF: 0,4100.511900,2839.235400,163.200000,20240204175023.000,0,10,0.166680,195.570007
                    # parse the response
                    response = self.ser.readline().decode('utf-8')
                    
                    if response.startswith("+CGPSINF:"):
                        response = response.split(',')
                        latitude = response[1]
                        longitude = response[2]
                        
                        # For latitude "4100.499800":

                        # Degrees: 41
                        # Minutes: 00.499800 (convert this to degrees by dividing by 60)
                        # So, the latitude in decimal degrees is 41 + (00.499800 / 60) = 41.008330 degrees.

                        # For longitude "2839.222800":

                        # Degrees: 28
                        # Minutes: 39.222800 (convert this to degrees by dividing by 60)
                        # So, the longitude in decimal degrees is 28 + (39.222800 / 60) = 28.653713 degrees.
                        
                        self.latitude = str(int(latitude[:2]) + (float(latitude[2:]) / 60))
                        self.longitude = str(int(longitude[:2]) + (float(longitude[2:]) / 60))
                        
                        print("Latitude: ", self.latitude)
                        print("Longitude: ", self.longitude)
                        
                        altitude = response[3]
                        gpsTime = response[4]
                        fixStatus = response[6]
                        hdop = response[7]
                        courseOverGround = response[8]
                        
                        
                        # print("Latitude: ", latitude)
                        # print("Longitude: ", longitude)
                        # print("Altitude: ", altitude)
                        # print("GPS Time: ", gpsTime)
                        # print("Fix Status: ", fixStatus)
                        # print("HDOP: ", hdop)
                        # print("Course Over Ground: ", courseOverGround)
                    else:
                        print(response)
                                                
            finally:
                self.ser.close()
        
        else:
            while True:
                # simulate movement
                self.bike.latitude = float(self.bike.latitude) + 0.001
                self.bike.longitude = float(self.bike.longitude) - 0.001
                if self.bike.speed < 30:
                    self.bike.speed = float(self.bike.speed) + 0.2
                print("bike speed: ", self.bike.speed)
                # self.speed = str(float(self.speed) + 0.2)
                print(f"Latitude: {self.bike.latitude}, Longitude: {self.bike.longitude}, Speed: {self.bike.speed}")           
                time.sleep(4)       

def main():
    gps_instance = GpsModule(isRealData=True)
    gps_instance.run_sim808(False)
    
if __name__ == "__main__":
    main()

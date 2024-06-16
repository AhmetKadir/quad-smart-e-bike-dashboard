from PyQt5.QtWidgets import QApplication
import sys
from threading import Thread
import time

from src.bike import Bike
from src.sim808_reader import GpsModule
from src.main_dashboard import dashboard
from src.communication import Communication

_useRealData = False
_useMap = False

def run_gps_module(gps_instance: GpsModule):
    time.sleep(5)
    gps_instance.run_sim808(_useRealData)
    
def send_data_to_server(bike: Bike):
    while True:
        time.sleep(2)
        if not bike.isLocked:
            Communication.send_data_to_server(bike.latitude, bike.longitude)
            bike.lightOn = Communication.GET_FLASH_LIGHT()
        
        bike.isLocked = Communication.read_is_locked()
        bike.hasInternetConnection = Communication.check_internet()
        
def demo1(bike : Bike):
    print("Demo 1 Running")
    bike.speed = 20
    bike.latitude = 40.808448
    bike.longitude = 29.356192
    bike.tripKm = 0.0
    bike.avg_speed = 20
    bike.rideStartTime = time.time()
    bike.batteryLevel = 60
    bike.isLocked = False
    bike.isConnected = False
    bike.hasInternetConnection = True
    bike.rightSignal = False
    bike.leftSignal = False
    bike.lightOn = False

def main():
    if len(sys.argv) != 3:
        print("Usage: python main.py <arg1> <arg2>")
        print("arg1: _useRealData, arg2: _useMap")
        print("Example: python main.py 0 0")
        sys.exit(1)
    
    _useRealData = sys.argv[1] == '1'
    _useMap = sys.argv[2] == '1'
    
    bike = Bike()
    if not _useRealData:
        demo1(bike)
    gps_instance = GpsModule(_useRealData, bike)
    
    # create thread for gps module
    gps_thread = Thread(target=run_gps_module, args=(gps_instance,))
    gps_thread.daemon = True
    gps_thread.start()
    
    # create thread for printing bike speed
    speed_thread = Thread(target=send_data_to_server, args=(bike,))
    speed_thread.daemon = True
    speed_thread.start()
    
    app = QApplication([])
    window = dashboard(bike)
    window.show()
    app.exec_()
    

if __name__ == "__main__":
    main()

    
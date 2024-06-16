import time
from math import floor


class Bike:
    def __init__(self):
        self.speed = 0
        self.latitude = 0.0
        self.longitude = 0.0
        self.tripKm = 0.0
        self.avg_speed = 0
        self.rideStartTime = time.time()
        self.batteryLevel = 0
        self.isLocked = False
        self.isConnected = False
        self.hasInternetConnection = True
        self.powerOn = True
        self.rightSignal = False
        self.leftSignal = False
        self.lightOn = False
    
    def getFormattedSpeed(self):
        return str(floor(self.speed))
    
    def getFormattedTrip(self):
        return str(round(self.tripKm, 1))
    
    def getFormattedAvgSpeed(self):
        return str(floor(self.avg_speed))
    
    def resetBike(self):
        self.speed = 0
        self.tripKm = 0
        self.avg_speed = 0
        self.rideStartTime = time.time()
        self.rightSignal = False
        self.leftSignal = False
        self.lightOn = False
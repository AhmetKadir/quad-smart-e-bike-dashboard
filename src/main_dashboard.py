from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtCore import QTimer, QTime, QDateTime, QTimeZone, QByteArray
from PyQt5 import QtGui, QtCore

import time
import os

from src.bike import Bike
from src.dashboard import Ui_MainWindow

from src.relay_module_rasp import RelayModule

folderPath = os.path.dirname(os.path.abspath(__file__))
parentDir = os.path.dirname(folderPath)
fontPath = os.path.join(parentDir, "Fonts")
iconPath = os.path.join(parentDir, "Icons")

myFontName = "RedditMono-VariableFont_wght"
fullDefaultFontPath = os.path.join(fontPath, myFontName + ".ttf")

speedFontName = "DS-DIGIT"
fullSpeedFontPath = os.path.join(fontPath, speedFontName + ".TTF")

statusOffStyleSheet = "background-color: black; border: 1px solid #A0A0A0;"
statusOnStyleSheet = "background-color: rgb(255, 255, 127); border: 1px solid #A0A0A0;"

# !!!!!!!! add timers array to store all timers

class dashboard(QMainWindow):
    def __init__(self, bike: Bike):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.showFullScreen()
        fontId = QFontDatabase.addApplicationFont(fullSpeedFontPath)
        if fontId < 0:
            print('font not loaded')
            exit()

        families = QFontDatabase.applicationFontFamilies(fontId)
        if not families:
            print('font not loaded')

        # Print the font family of speed_label
        # print(f"Speed label font family: {self.ui.speed_label.font().family()}")

        fontId2 = QFontDatabase.addApplicationFont(fullDefaultFontPath)
        if fontId2 < 0:
            print('font not loaded')
            exit()

        families2 = QFontDatabase.applicationFontFamilies(fontId2)
        if not families2:
            print('font not loaded')

        # speed stylesheet
        # self.ui.speed_label.setFont(QFont(families[0], 70))
        self.ui.speed_label.setStyleSheet(
            f"color: white; font-family: '{families[0]}'; font-size: 300px;")
        self.ui.speed_unit.setStyleSheet(
            f"font-family: '{families2[0]}'; color: #A0A0A0; font-size: 20px;")
        self.ui.speed_label.setText(bike.getFormattedSpeed())

        # brand and company name stylesheet
        self.ui.brandName.setStyleSheet(
            f"font-family: '{families2[0]}'; font-size: 30px; color: #A0A0A0;")
        self.ui.companyName.setStyleSheet(
            f"font-family: '{families2[0]}'; font-size: 15px; color: #A0A0A0;")

        # trip stylesheet
        self.ui.trip.setStyleSheet(
            f"font-family: '{families[0]}'; font-size: 150px;")
        self.ui.trip_header.setStyleSheet(
            f"font-family: '{families2[0]}'; font-size: 20px; color: #A0A0A0;")
        self.ui.trip_unit.setStyleSheet(
            f"font-family: '{families2[0]}'; font-size: 20px; color: #A0A0A0;")
        self.ui.trip.setText(bike.getFormattedTrip())

        # avg speed stylesheet
        self.ui.avg_speed.setStyleSheet(
            f"font-family: '{families[0]}'; font-size: 150px;")
        self.ui.avg_speed_header.setStyleSheet(
            f"font-family: '{families2[0]}'; font-size: 20px; color: #A0A0A0;")
        self.ui.avg_speed_unit.setStyleSheet(
            f"font-family: '{families2[0]}'; font-size: 20px; color: #A0A0A0;")
        self.ui.avg_speed.setText(bike.getFormattedAvgSpeed())

        # remaining time stylesheet
        self.ui.remainingTimeText.setStyleSheet(
            f"font-family: '{families2[0]}'; font-size: 50px; color: white;")

        self.ui.date.setStyleSheet(
            f"font-family: '{families2[0]}'; font-size: 20px; color: white;")
        self.ui.time.setStyleSheet(
            f"font-family: '{families2[0]}'; font-size: 30px; color: white;")
        self.updateDate()
        
        # timers array
        self.timers = []

        # update date and time every second
        timer1 = QTimer(self)
        timer1.timeout.connect(self.updateDate)
        timer1.start(1000)
        self.timers.append(timer1)

        # update speed every second
        timer2 = QTimer(self)
        timer2.timeout.connect(lambda: self.change_speed(bike))
        timer2.start(1000)
        self.timers.append(timer2)

        # update ride time every second
        timer = QTimer(self)
        timer.timeout.connect(lambda: self.updateRideTime(bike))
        timer.start(1000)

        # update trip every second
        timer = QTimer(self)
        timer.timeout.connect(lambda: self.updateTrip(bike))
        timer.start(1000)

        # update avg speed every second
        timer = QTimer(self)
        timer.timeout.connect(lambda: self.updateAvgSpeed(bike))
        timer.start(1000)

        timer = QTimer(self)
        timer.timeout.connect(lambda: self.checkInternetConnection(bike))
        timer.start(750)

        self.ui.lightsOnButton.clicked.connect(lambda: self.toggleLights(bike))

        timer = QTimer(self)
        timer.timeout.connect(lambda: self.checkLights(bike))
        timer.start(1000)

        blink_right_signal_timer = QTimer(self)
        blink_right_signal_timer.timeout.connect(
            lambda: self.blinkRightSignal())

        self.ui.rightArrow.clicked.connect(
            lambda: self.toggleRightSignal(bike, blink_right_signal_timer))

        # same for left signal
        blink_left_signal_timer = QTimer(self)
        blink_left_signal_timer.timeout.connect(
            lambda: self.blinkLeftSignal())

        self.ui.leftArrow.clicked.connect(
            lambda: self.toggleLeftSignal(bike, blink_left_signal_timer))

        timer = QTimer(self)
        timer.timeout.connect(lambda: self.checkIsLocked(bike))
        timer.start(1000)
        
        self.ui.pushButton.clicked.connect(lambda: self.honk())

    def honk(self):
        RelayModule.honk()

    def change_speed(self, bike: Bike):
        self.ui.speed_label.setText(bike.getFormattedSpeed())

    def updateDate(self):
        iana_id_bytes = QByteArray(b"Europe/Istanbul")
        current_utc_datetime = QDateTime.currentDateTimeUtc()
        turkey_time_zone = QTimeZone(iana_id_bytes)
        current_turkey_datetime = QDateTime(current_utc_datetime)
        current_turkey_datetime.setTimeZone(turkey_time_zone)
        self.ui.date.setText(current_turkey_datetime.toString("dd/MM/yyyy"))
        self.ui.time.setText(current_turkey_datetime.toString("HH:mm"))

    def updateRideTime(self, bike: Bike):
        rideTime = time.time() - bike.rideStartTime
        if rideTime < 3600:
            convertedRideTime = time.strftime("%M:%S", time.gmtime(rideTime))
        else:
            convertedRideTime = time.strftime(
                "%H:%M:%S", time.gmtime(rideTime))

        self.ui.remainingTimeText.setText(convertedRideTime)

    def updateTrip(self, bike: Bike):
        bike.tripKm = bike.tripKm + (bike.speed / 3600)
        self.ui.trip.setText(bike.getFormattedTrip())

    def updateAvgSpeed(self, bike: Bike):
        timeInterval = time.time() - bike.rideStartTime
        if timeInterval > 30:
            bike.avg_speed = (bike.tripKm / timeInterval) * 3600

        self.ui.avg_speed.setText(bike.getFormattedAvgSpeed())

    def checkInternetConnection(self, bike: Bike):
        if not bike.hasInternetConnection:
            if not "background-color: black;" in self.ui.internet_light.styleSheet():
                self.ui.internet_light.setStyleSheet(
                    "background-color: black;")
            else:
                self.ui.internet_light.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")
        else:
            if "background-color: black;" in self.ui.internet_light.styleSheet():
                self.ui.internet_light.setStyleSheet(
                    "background-color: rgb(255, 255, 127);")

    def toggleRightSignal(self, bike: Bike, blink_right_signal_timer: QTimer):
        if bike.rightSignal:
            blink_right_signal_timer.stop()
            bike.rightSignal = False
        else:
            blink_right_signal_timer.start(500)
            bike.rightSignal = True

    def blinkRightSignal(self):
        if self.ui.rightArrow.isVisible():
            self.ui.rightArrow.hide()
        else:
            self.ui.rightArrow.show()

    def toggleLeftSignal(self, bike: Bike, blink_left_signal_timer: QTimer):
        if bike.leftSignal:
            blink_left_signal_timer.stop()
            bike.leftSignal = False
        else:
            blink_left_signal_timer.start(500)
            bike.leftSignal = True

    def blinkLeftSignal(self):
        if self.ui.leftArrow.isVisible():
            self.ui.leftArrow.hide()
        else:
            self.ui.leftArrow.show()

    def toggleLights(self, bike: Bike):
        if bike.lightOn == False:
            bike.lightOn = True
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("Icons/light.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.lightsOnButton.setIcon(icon)
            self.ui.lightsOnButton.setIconSize(QtCore.QSize(100, 80))
        else:
            bike.lightOn = False
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("Icons/lightOff.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.lightsOnButton.setIcon(icon)
            self.ui.lightsOnButton.setIconSize(QtCore.QSize(100, 80))


    def checkLights(self, bike: Bike):
        if bike.lightOn:
            RelayModule.bike_light_on()
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("Icons/light.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.lightsOnButton.setIcon(icon)
            self.ui.lightsOnButton.setIconSize(QtCore.QSize(100, 80))

        else:
            RelayModule.bike_light_off()
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("Icons/lightOff.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.lightsOnButton.setIcon(icon)
            self.ui.lightsOnButton.setIconSize(QtCore.QSize(100, 80))

    def checkIsLocked(self, bike: Bike):
        if bike.isLocked:
            self.ui.unlocked_light.setStyleSheet(statusOffStyleSheet)
            # disable central widget
            self.ui.centralwidget.setEnabled(False)
            bike.resetBike()
            self.change_speed(bike)
            self.stopTimers()
        else:
            self.ui.centralwidget.setEnabled(True)
            self.ui.unlocked_light.setStyleSheet(statusOnStyleSheet)
            self.startTimers()
            
    
    def stopTimers(self):
        for timer in self.timers:
            timer.stop()        

    def startTimers(self):
        for timer in self.timers:
            timer.start()
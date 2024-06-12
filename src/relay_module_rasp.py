import RPi.GPIO as GPIO

class RelayModule:
    bike_light_pin = 19

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(bike_light_pin, GPIO.OUT)

    def bike_light_on():
        GPIO.output(bike_light_pin, GPIO.LOW)  # LOW to turn on for a low-level trigger relay

    def bike_light_off():
        GPIO.output(bike_light_pin, GPIO.HIGH)  # HIGH to turn off for a low-level trigger relay



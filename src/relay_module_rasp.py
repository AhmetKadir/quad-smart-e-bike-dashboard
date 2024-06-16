import RPi.GPIO as GPIO
import time

bike_light_pin = 19
honk_pin = 5

class RelayModule:

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(bike_light_pin, GPIO.OUT)
    GPIO.setup(honk_pin, GPIO.OUT)

    def bike_light_on():
        GPIO.output(bike_light_pin, GPIO.LOW)  # LOW to turn on for a low-level trigger relay

    def bike_light_off():
        GPIO.output(bike_light_pin, GPIO.HIGH)  # HIGH to turn off for a low-level trigger relaY
    
    def honk():
        GPIO.output(honk_pin, GPIO.LOW)
        time.sleep(0.5)
        GPIO.output(honk_pin, GPIO.HIGH)





import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
pin = 18
GPIO.setup(pin, GPIO.OUT)

# Turn on sound
GPIO.output(pin, GPIO.HIGH)
time.sleep(0.2)  # Beep for 0.2 seconds

# Turn off sound
GPIO.output(pin, GPIO.LOW)

GPIO.cleanup()

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

pin = 18
GPIO.setup(pin, GPIO.OUT)

# Create PWM at 1500 Hz (good loud frequency)
pwm = GPIO.PWM(pin, 1500)

# Start PWM at 90% duty cycle for a loud buzz
pwm.start(90)

# Buzz for 1 second
time.sleep(1)

# Stop
pwm.stop()
GPIO.cleanup()

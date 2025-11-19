
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
pin = 18
GPIO.setup(pin, GPIO.OUT)

try:
    while True:
        value = input("Type a number (or 'q' to quit): ")

        if value == "10":
            print("Beep!")
            GPIO.output(pin, GPIO.HIGH)
            time.sleep(0.3)  # Beep for 0.3 seconds
            GPIO.output(pin, GPIO.LOW)
        elif value.lower() == "q":
            print("Goodbye!")
            break
        else:
            print("No beep. You typed:", value)

finally:
    GPIO.cleanup()

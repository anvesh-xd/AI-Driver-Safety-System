import RPi.GPIO as GPIO
import time

# --- Setup ---
GPIO.setmode(GPIO.BCM)
pin = 18
GPIO.setup(pin, GPIO.OUT)

# --- Ask user for input ---
value = input("Type a number: ")

# --- Check if input is 10 ---
if value == "10":
    print("Beep!")
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(0.3)   # Beep for 0.3 seconds
    GPIO.output(pin, GPIO.LOW)
else:
    print("No beep. You typed:", value)

# --- Cleanup ---
GPIO.cleanup()

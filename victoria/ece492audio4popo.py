import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
pin = 18
GPIO.setup(pin, GPIO.OUT)

pwm = GPIO.PWM(pin, 440)  # starting frequency (A4 note)
pwm.start(80)             # loud duty cycle

try:
    while True:
        # Rising tone (440 Hz → 1000 Hz)
        for f in range(440, 1000, 10):
            pwm.ChangeFrequency(f)
            time.sleep(0.005)

        # Falling tone (1000 Hz → 440 Hz)
        for f in range(1000, 440, -10):
            pwm.ChangeFrequency(f)
            time.sleep(0.005)

except KeyboardInterrupt:
    pass

pwm.stop()
GPIO.cleanup()


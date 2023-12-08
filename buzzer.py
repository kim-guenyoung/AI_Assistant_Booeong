import RPi.GPIO as GPIO
import time

bz_pin = 18

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(bz_pin, GPIO.OUT)

p = GPIO.PWM(bz_pin, 100)

Frq = [262, 330, 392, 330, 262, 1]

speed = 0.5

try:
    # Wait for 3 seconds silently
    time.sleep(3)

    # Start the alarm loop
    p.start(10)

    while 1:
        for fr in Frq:
            p.ChangeFrequency(fr)
            print("I'm running")
            time.sleep(0.5)

        # Pause for 2 seconds between Frq sequences
        time.sleep(1)

except KeyboardInterrupt:
    pass

p.stop()
GPIO.cleanup()

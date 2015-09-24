import RPi.GPIO as GPIO
import time

print "Set mode BCM"
GPIO.setmode(GPIO.BCM)

motors = [6, 13, 19, 26]

for pin in motors:
    print "Setup output port", pin
    GPIO.setup(pin, GPIO.OUT)


for i in range(50):
    for pin in motors:
        print "Switch", pin
        GPIO.output(pin, 1)
        time.sleep(0.01)
        GPIO.output(pin, 0)


GPIO.cleanup()

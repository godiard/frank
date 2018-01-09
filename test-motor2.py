import RPi.GPIO as GPIO
import time

print "Set mode BCM"
GPIO.setmode(GPIO.BCM)

motors = [2, 3, 4, 17]

for pin in motors:
    print "Setup output port", pin
    GPIO.setup(pin, GPIO.OUT)


for i in range(500):
    for pin in motors:
        print "Switch", pin
        GPIO.output(pin, 1)
        time.sleep(0.5)
        GPIO.output(pin, 0)


GPIO.cleanup()

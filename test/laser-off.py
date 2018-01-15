import RPi.GPIO as GPIO
import time

print "Set mode BCM"
GPIO.setmode(GPIO.BCM)

pin = 5

print "Setup output port", pin
GPIO.setup(pin, GPIO.OUT)


print "Switch", pin
GPIO.output(pin, 0)

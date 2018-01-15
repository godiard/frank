import RPi.GPIO as GPIO


class Laser:

    def __init__(self, pin):
        print "Setup laser output port", pin
        GPIO.setup(pin, GPIO.OUT)
        self.pin = pin

    def on(self):
        GPIO.output(self.pin, 1)

    def off(self):
        GPIO.output(self.pin, 0)

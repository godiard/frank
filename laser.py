import RPi.GPIO as GPIO


class Laser:

    def __init__(self, pin):
        print "Setup laser output port", pin
        GPIO.setup(pin, GPIO.OUT)
        self.pin = pin
        self._is_on = False

    def on(self):
        print "Laser ON"
        GPIO.output(self.pin, 1)
        self._is_on = True

    def off(self):
        print "Laser OFF"
        GPIO.output(self.pin, 0)
        self._is_on = False

    def is_on(self):
        return self._is_on

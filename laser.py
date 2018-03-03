try:
    import RPi.GPIO as GPIO
except:
    print 'RPi.GIO not available, only emulation mode allowed'


class Laser:

    def __init__(self, pin, emulator = None):
        print "Setup laser output port", pin
        self._emulator = emulator
        if self._emulator is None:
            GPIO.setup(pin, GPIO.OUT)
        self.pin = pin
        self._is_on = False

    def on(self):
        print "Laser ON"
        if self._emulator is not None:
            self._emulator.on()
        else:
            GPIO.output(self.pin, 1)
        self._is_on = True

    def off(self):
        print "Laser OFF"
        if self._emulator is not None:
            self._emulator.off()
        else:
            GPIO.output(self.pin, 0)
        self._is_on = False

    def is_on(self):
        return self._is_on

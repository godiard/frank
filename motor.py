try:
    import RPi.GPIO as GPIO
except:
    print 'RPi.GIO not available, only emulation mode allowed'

import time

class Motor:
    RIGHT = 1
    LEFT  = -1

    def __init__(self, pins, emulator = None):
        self.delay = 0.005
        self.pins  = pins
        #self.move_table = [[1, 1, 0, 0], [0, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 0],
        #                   [0, 0, 1, 1], [0, 0, 0, 1], [1, 0, 0, 1], [1, 0, 0, 0]]
        #self.move_table = [[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 1], [1, 0, 0, 1]]
        self.move_table = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]

        self._emulator = emulator
        if self._emulator is None:
            for pin in self.pins:
              print "Setup output port", pin
              GPIO.setup(pin, GPIO.OUT)

    # direction can be 1 or -1
    def moveTo(self, direction, fast=False):
        step = 0
        for i in range(4):
            for pin in range(4):
                GPIO.output(self.pins[pin], self.move_table[step][pin])

            step += direction

            if direction == Motor.RIGHT:
                if step == len(self.move_table):
                    step = 0
            if direction == Motor.LEFT:
                if step < 0:
                    step = len(self.move_table) - 1
            if fast:
                time.sleep(self.delay / 2)
            else:
                time.sleep(self.delay)

    def off(self):
        if self._emulator is None:
            for pin in self.pins:
              print "Setup output port", pin
              GPIO.output(pin, 0)

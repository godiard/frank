import RPi.GPIO as GPIO
import time

class Motor:
    RIGHT = 1
    LEFT  = -1

    def __init__(self, pins):
        self.delay = 0.005
        self.pins  = pins
        #self.move_table = [[1, 1, 0, 0], [0, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 0],
        #                   [0, 0, 1, 1], [0, 0, 0, 1], [1, 0, 0, 1], [1, 0, 0, 0]]
        #self.move_table = [[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 1], [1, 0, 0, 1]]
        self.move_table = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]

        for pin in self.pins:
          print "Setup output port", pin
          GPIO.setup(pin, GPIO.OUT)

    # direction can be 1 or -1
    def moveTo(self, direction):
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
            time.sleep(self.delay)

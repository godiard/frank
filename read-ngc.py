#!/usr/bin/env python

try:
    import RPi.GPIO as GPIO
except:
    print 'RPi.GIO not available, only emulation mode allowed'
import json
import sys
from laser import Laser
from motor import Motor
from cairoemulator import Emulator


class MotorCommander:

    def __init__(self, motor, steps, direction):
        self.motor = motor
        self.steps = steps
        self.direction = direction


class NgcReader:

    MOVE_FAST = 'G00'
    MOVE_LINEAR = 'G01'
    LASER_ON = 'M03'
    LASER_OFF = 'M05'

    def __init__(self, filename, scale=1.0, margin=None, emulate=False):
        self.filename = filename
        self._emulator = None
        self._scale = scale
        self._x_min = 0
        self._y_min = 0
        self._x_max = 0
        self._y_max = 0
        self._margin = 0
        if margin is not None:
            self._margin = margin
        self.preprocess()
        if emulate:
            print "CAIRO EMUL x_max %f y_max %f SCALE %f MARGIN %f" % (
                self._x_max, self._y_max, self._scale, self._margin)
            self._emulator = Emulator(
                (self._x_max - self._x_min) * self._scale + self._margin,
                (self._y_max - self._y_min) * self._scale + self._margin)
        self.init()
        self.process()

    def init(self):
        print "Set mode BCM"
        config = json.load(open("config.json"))
        if self._emulator is None:
            GPIO.setmode(GPIO.BCM)
        self.motorX = Motor(config["motor_x"]["pins"], self._emulator)
        self.motorX.axis = "X"
        self.motorX.delay = config["motor_x"]["delay"]
        self.motorX.steps_by_mm = config["motor_x"]["steps_by_mm"]

        self.motorY = Motor(config["motor_y"]["pins"], self._emulator)
        self.motorY.axis = "Y"
        self.motorY.delay = config["motor_y"]["delay"]
        self.motorY.steps_by_mm = config["motor_y"]["steps_by_mm"]

        self.laser = Laser(config["laser"]["pin"], self._emulator)
        self.laser.off()
        self.motorX.off()
        self.motorY.off()

    def preprocess(self):
        # get min and max values
        x_min = sys.maxint
        y_min = sys.maxint
        x_max = 0
        y_max = 0

        for line in open(self.filename):
            parameters = line.split()
            if parameters:
                command = parameters[0]
                if command == self.MOVE_FAST or command == self.MOVE_LINEAR:
                    x = None
                    y = None
                    for parameter in parameters:
                        if parameter.startswith('X'):
                            x = float(parameter[1:])
                        if parameter.startswith('Y'):
                            y = float(parameter[1:])
                    if x is not None and y is not None and x > 0 and y > 0:
                        x_min = min(x_min, x)
                        y_min = min(y_min, y)
                        x_max = max(x_max, x)
                        y_max = max(y_max, y)

        print "X_MIN %f Y_MIN %f X_MAX %f Y_MAX %f" % (x_min, y_min,
                                                       x_max, y_max)
        self._x_min = x_min
        self._y_min = y_min
        self._x_max = x_max
        self._y_max = y_max

    def process(self):
        self.x = 0
        self.y = 0
        for line in open(self.filename):
            print line
            parameters = line.split()
            if parameters:
                command = parameters[0]
                if command == self.LASER_ON:
                    self.laser.on()
                elif command == self.LASER_OFF:
                    self.laser.off()
                elif command == self.MOVE_FAST or command == self.MOVE_LINEAR:
                    x = None
                    y = None
                    z = None
                    for parameter in parameters:
                        if parameter.startswith('X'):
                            x = float(parameter[1:])
                        if parameter.startswith('Y'):
                            y = float(parameter[1:])
                        if parameter.startswith('Z'):
                            z = float(parameter[1:])
                    if y is not None and x is not None:
                        fast = (command == self.MOVE_FAST)
                        self.goto(
                            (x - self._x_min) * self._scale + self._margin,
                            (y - self._y_min) * self._scale + self._margin,
                            fast)

        self.laser.off()
        self.motorX.off()
        self.motorY.off()
        if self._emulator is not None:
            self._emulator.save()

    def _get_direction(self, delta):
        if delta < 0:
            return Motor.RIGHT
        else:
            return Motor.LEFT

    def goto(self, x, y, fast):
        # if self._emulator is not None:
        #    self._emulator.move_to(x, y)
        #    self.x = x
        #    self.y = y
        #    return

        print 'ACTUAL %f %f ' % (self.x, self.y)
        print 'GOTO %f %f ' % (x, y)
        # distance in mm
        delta_x = self.x - x
        delta_y = self.y - y
        x_direction = self._get_direction(delta_x)
        y_direction = self._get_direction(delta_y)

        steps_x = abs(float(delta_x) * self.motorX.steps_by_mm)
        steps_y = abs(float(delta_y) * self.motorY.steps_by_mm)
        if fast:
            for n in range(0, int(steps_x)):
                self.motorX.moveTo(x_direction)

            for n in range(0, int(steps_y)):
                self.motorY.moveTo(y_direction)
        else:
            # select motor with bigger distance
            if steps_x > steps_y:
                commander_1 = MotorCommander(
                    self.motorX, steps_x, x_direction)
                commander_2 = MotorCommander(
                    self.motorY, steps_y, y_direction)
            else:
                commander_2 = MotorCommander(
                    self.motorX, steps_x, x_direction)
                commander_1 = MotorCommander(
                    self.motorY, steps_y, y_direction)

            m = 0
            for n in range(0, int(round(commander_1.steps))):
                commander_1.motor.moveTo(commander_1.direction)
                d2 = commander_2.steps / commander_1.steps * n
                if (d2 - m) > 0.5:
                    commander_2.motor.moveTo(commander_2.direction)
                    # m = m + 1
                    m = d2

        self.x = x
        self.y = y

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print "Usage read-ngc.py file_name [scale] [margin]"
        exit(0)

    ngc_file_name = sys.argv[1]
    margin = None
    scale = 1.0
    if len(sys.argv) > 2:
        try:
            scale = float(sys.argv[2])
        except:
            print "Scale parameter should be a float (ex: 1.5)"

    if len(sys.argv) > 3:
        try:
            margin = int(sys.argv[3])
        except:
            print "Margin should be a intger"

    emulate = '--emulate' in sys.argv

    ngc_reader = NgcReader(ngc_file_name, scale, margin, emulate)

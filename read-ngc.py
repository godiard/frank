#!/usr/bin/env python

try:
    import RPi.GPIO as GPIO
except:
    print 'RPi.GIO not available, only emulation mode allowed'
import json
import sys
from laser import Laser
from motor import Motor


class NgcReader:

    MOVE_FAST = 'G00'
    MOVE_LINEAR = 'G01'
    LASER_ON = 'M03'
    LASER_OFF = 'M05'

    def __init__(self, filename, scale = 1.0, margin = None):
        self.filename = filename
        self.init()
        self.scale = scale
        self.x_min = 0
        self.y_min = 0
        if margin == 0:
            self.preprocess()
        self.process()

    def init(self):
        print "Set mode BCM"
        config = json.load(open("config.json"))
        GPIO.setmode(GPIO.BCM)
        self.motorX = Motor(config["motor_x"]["pins"])
        self.motorX.name = "X"
        self.motorX.delay = config["motor_x"]["delay"]
        self.motorX.steps_by_mm = config["motor_x"]["steps_by_mm"]

        self.motorY = Motor(config["motor_y"]["pins"])
        self.motorY.name = "Y"
        self.motorY.delay = config["motor_y"]["delay"]
        self.motorY.steps_by_mm = config["motor_y"]["steps_by_mm"]

        self.laser = Laser(config["laser"]["pin"])
        self.laser.off()
        self.motorX.off()
        self.motorY.off()

    def preprocess(self):
        # get min and max values
        self.x_min = sys.maxint
        self.y_min = sys.maxint

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
                        if self.x_min > x:
                            self.x_min = x
                        if self.y_min > y:
                            self.y_min = y

        print "X_MIN %f Y_MIN %f" % (self.x_min, self.y_min)

    def process(self):
        self.x = 0
        self.y = 0
        for line in open(self.filename):
            print line
            parameters = line.split()
            if parameters:
                command = parameters[0]
                # Ignoro comando para prender y apagar el laser
                # porque se prende antes de tiempo
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
                        self.goto((x - self.x_min) * self.scale,
                                  (y - self.y_min) * self.scale, fast)
                    # Ignoro lineas que no tienen x para que no prenda el
                    # laser antes de tiempo
                    #if z is not None and x is not None:
                    #    if z < 0:
                    #        if not self.laser.is_on():
                    #            self.laser.on()
                    #    else:
                    #        if self.laser.is_on():
                    #            self.laser.off()

        self.laser.off()
        self.motorX.off()
        self.motorY.off()

    def goto(self, x, y, fast):
        print 'ACTUAL %f %f ' % (self.x, self.y)
        print 'GOTO %f %f ' % (x, y)
        # distance in mm
        delta_x = self.x - x
        if delta_x < 0:
            x_direction = Motor.RIGHT
        else:
            x_direction = Motor.LEFT

        delta_y = self.y - y
        if delta_y < 0:
            y_direction = Motor.RIGHT
        else:
            y_direction = Motor.LEFT

        #print "delta_x %f delta_y %f" % (delta_x, delta_y)
        steps_x = abs(delta_x * self.motorX.steps_by_mm)
        steps_y = abs(delta_y * self.motorY.steps_by_mm)
        if fast:
            for n in range(0, int(steps_x)):
                self.motorX.moveTo(x_direction)

            for n in range(0, int(steps_y)):
                self.motorY.moveTo(y_direction)
        else:
            #print "steps_x %f steps_y %f" % (steps_x, steps_y)
            # select motor with bigger distance
            if steps_x > steps_y:
                #print "MOTOR1 = X"
                motor_1 = self.motorX
                motor_2 = self.motorY
                steps_1 = steps_x
                steps_2 = steps_y
                direction_1 = x_direction
                direction_2 = y_direction
            else:
                #print "MOTOR1 = Y"
                motor_1 = self.motorY
                motor_2 = self.motorX
                steps_1 = steps_y
                steps_2 = steps_x
                direction_1 = y_direction
                direction_2 = x_direction

            m = 0
            for n in range(0, int(steps_1)):
                motor_1.moveTo(direction_1)
                d2 = steps_2 / steps_1 * n
                if (d2 - m) > 0.5:
                    motor_2.moveTo(direction_2)
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

    ngc_reader = NgcReader(ngc_file_name, scale, margin)

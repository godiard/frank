#!/usr/bin/env python

import RPi.GPIO as GPIO
import json
import sys
from laser import Laser
from motor import Motor


class NgcReader:

    MOVE_FAST = 'G00'
    MOVE_LINEAR = 'G01'
    LASER_ON = 'M03'
    LASER_OFF = 'M05'

    def __init__(self, filename):
        self.filename = filename
        self.init()
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

    def process(self):
        size = 50
        self.x = 0
        self.y = 0
        for line in open(self.filename):
            print line
            parameters = line.split()
            if parameters:
                command = parameters[0]
                if command == self.LASER_ON:
                    print 'Laser ON'
                    self.laser.on()
                elif command == self.LASER_OFF:
                    print 'Laser OFF'
                    self.laser.off()
                elif command == self.MOVE_FAST or command == self.MOVE_LINEAR:
                    x_param = None
                    y_param = None
                    for parameter in parameters:
                        if parameter.startswith('X'):
                            x_param = float(parameter[1:])
                        if parameter.startswith('Y'):
                            y_param = float(parameter[1:])
                    if x_param is not None and y_param is not None:
                        self.goto(x_param, y_param)

        self.laser.off()
        self.motorX.off()
        self.motorY.off()

    def goto(self, x, y):
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

        print "delta_x %f delta_y %f" % (delta_x, delta_y)
        steps_x = abs(delta_x * self.motorX.steps_by_mm)
        steps_y = abs(delta_y * self.motorY.steps_by_mm)
        print "steps_x %f steps_y %f" % (steps_x, steps_y)
        # select motor with bigger distance
        if steps_x > steps_y:
            print "MOTOR1 = X"
            motor_1 = self.motorX
            motor_2 = self.motorY
            steps_1 = steps_x
            steps_2 = steps_y
            direction_1 = x_direction
            direction_2 = y_direction
        else:
            print "MOTOR1 = Y"
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
            if (d2 - m) > 1:
                motor_2.moveTo(direction_2)
                m = m + 1

        self.x = x
        self.y = y

    def move(self, motor, direction, size):
        print "motor %s %d %d" % (motor.name, direction, size * motor.steps_by_mm)
        for x in range(0, size * motor.steps_by_mm):
            motor.moveTo(direction)


if __name__ == "__main__":
    if len(sys.argv) < 1:
        print "Usage read-ngc.py file_name"
        exit(0)

    ngc_file_name = sys.argv[1]
    ngc_reader = NgcReader(ngc_file_name)

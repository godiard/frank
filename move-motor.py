#!/usr/bin/env python

import RPi.GPIO as GPIO
import json
import sys
from motor import Motor

if len(sys.argv) < 4:
    print "Usage move-motor.py motor(x or y) direction(l or r) distance"
    exit(0)

motor_leter = sys.argv[1]
if not motor_leter in ['x', 'y']:
    print "Motor should be 'x or 'y'"
    exit(0)

direction = sys.argv[2]
if not direction in ['l', 'r']:
    print "Direction should be 'l' or 'r'"
    exit(0)

try:
    distance = int(sys.argv[3])
except ValueError:
    print "Distance should be a integer"
    exit(0)

print "Motor " + motor_leter
print "Direccion " + direction
print "Distance %d" % distance

print "Set mode BCM"
config = json.load(open("config.json"))
GPIO.setmode(GPIO.BCM)
motor = Motor(config["motor_" + motor_leter]["pins"])
motor.delay = config["motor_" + motor_leter]["delay"]
motor.step_size = config["motor_" + motor_leter]["step_size"]

dir = Motor.RIGHT
if direction == 'l':
    dir = Motor.LEFT

for x in range(0, int(distance * motor.step_size)):
    motor.moveTo(dir)

#!/usr/bin/env python

import RPi.GPIO as GPIO

print "Set mode BCM"
GPIO.setmode(GPIO.BCM)

laser_pin = 5

print "Setup output port", laser_pin
GPIO.setup(laser_pin, GPIO.OUT)

print "Switch laser off", laser_pin
GPIO.output(laser_pin, 0)

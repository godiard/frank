#!/usr/bin/env python

# from https://howchoo.com/g/mwnlytk3zmm/how-to-add-a-power-button-to-your-raspberry-pi

import RPi.GPIO as GPIO
import subprocess


shutdown_pin = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(shutdown_pin , GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.wait_for_edge(shutdown_pin , GPIO.FALLING)

subprocess.call(['shutdown', '-h', 'now'], shell=False)


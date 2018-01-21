import RPi.GPIO as GPIO
import json
from motor import Motor
from laser import Laser

class Square:

    def __init__(self):
        print "Set mode BCM"
        config = json.load(open("config.json"))
        GPIO.setmode(GPIO.BCM)
        self.motorX = Motor(config["motor_x"]["pins"])
        self.motorX.name = "X"
        self.motorX.delay = config["motor_x"]["delay"]
        self.motorX.step_size = config["motor_x"]["step_size"]

        self.motorY = Motor(config["motor_y"]["pins"])
        self.motorY.name = "Y"
        self.motorY.delay = config["motor_y"]["delay"]
        self.motorY.step_size = config["motor_y"]["step_size"]

        self.laser = Laser(config["laser"]["pin"])

    def start(self):
        size = 50
        self.laser.on()
        self.move(self.motorX, Motor.RIGHT, size)
        self.move(self.motorY, Motor.RIGHT, size)
        self.move(self.motorX, Motor.LEFT, size)
        self.move(self.motorY, Motor.LEFT, size)
        self.laser.off()
        self.motorX.off()
        self.motorY.off()

    def move(self, motor, direction, size):
        print "motor %s %d %d" % (motor.name, direction, size * motor.step_size)
        for x in range(0, size * motor.step_size):
            motor.moveTo(direction)


    def cleanUp(self):
        GPIO.cleanup()


Square().start()

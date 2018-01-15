import RPi.GPIO as GPIO
from motor import Motor
from laser import Laser

class Square:

    def __init__(self):
        print "Set mode BCM"
        GPIO.setmode(GPIO.BCM)
        self.motorX = Motor([6, 13, 19, 26])
        self.motorX.delay = 0.1
        self.motorY = Motor([2, 3, 4, 17])
        self.motorY.delay = 0.1
        self.laser = Laser(5)

    def start(self):
        size = 50
        mult = 30
        self.laser.on()
        for x in range(0, size):
            self.motorX.moveTo(Motor.RIGHT)
        for x in range(0, size * mult):
            self.motorY.moveTo(Motor.RIGHT)
        for x in range(0, size):
            self.motorX.moveTo(Motor.LEFT)
        for x in range(0, size * mult):
            self.motorY.moveTo(Motor.LEFT)
        self.laser.off()

    def cleanUp(self):
        GPIO.cleanup()


Square().start()

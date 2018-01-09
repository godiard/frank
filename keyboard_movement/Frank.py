import RPi.GPIO as GPIO
import curses
from motor import Motor

class Frank:

    def __init__(self):
        print "Set mode BCM"
        GPIO.setmode(GPIO.BCM)
        self.motorX = Motor([6, 13, 19, 26])
        #self.motorY = Motor([])
        #self.sensor = Sensor(4) 
        self.setUpScreen()

    def setUpScreen(self):
        self.screen = curses.initscr()
        # turn off input echoing
        curses.noecho()
        # respond to keys immediately (don't wait for enter)
        curses.cbreak()
        # map arrow keys to special values
        self.screen.keypad(True)

    def isArrowKey(self, char):
        return char in [curses.KEY_RIGHT,curses.KEY_LEFT, curses.KEY_UP, curses.KEY_DOWN]

    def start(self):
        try:
            char = self.screen.getch()
            while True :
                
                while self.isArrowKey():
                    if char == curses.KEY_RIGHT:
                        print 'right'
                        self.motorX.moveTo(Motor.RIGHT)
                    elif char == curses.KEY_LEFT:
                        print 'left '
                        self.motorX.moveTo(Motor.LEFT)
                    elif char == curses.KEY_UP :
                        print 'up'
                    elif char == curses.KEY_DOWN :
                        print 'down'
                    char = self.screen.getch()
                if char == ord('q'):
                    self.cleanUp()
                    break
                else:
                    char = self.screen.getch()

        finally:
            # shut down cleanly
            curses.nocbreak(); self.screen.keypad(0); curses.echo()
            curses.endwin()

    def cleanUp(self):
        GPIO.cleanup()


Frank().start()

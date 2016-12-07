import RPi.GPIO as GPIO
import curses
from motorModule import Motor

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

    def start(self):
        try:
            char = self.screen.getch()
            while True :
                
                while char == curses.KEY_RIGHT or char == curses.KEY_LEFT:
                    if char == curses.KEY_RIGHT:
                      # print doesn't work with curses, use addstr instead
                        print 'right'
                        self.motorX.moveTo(Motor.RIGHT)
                    elif char == curses.KEY_LEFT:
                        print 'left '
                        self.motorX.moveTo(Motor.LEFT)
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
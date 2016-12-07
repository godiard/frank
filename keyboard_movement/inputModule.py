import curses
from motorModule import Motor

# get the curses screen window
motor  = Motor()
screen = curses.initscr()

# turn off input echoing
curses.noecho()

# respond to keys immediately (don't wait for enter)
curses.cbreak()

# map arrow keys to special values
screen.keypad(True)

try:
    char = screen.getch()
    while True :
        if char == ord('q'):
            motor.cleanUp()
            break
      else:
          while char == curses.KEY_RIGHT or char == curses.KEY_LEFT:
              if char == curses.KEY_RIGHT:
                # print doesn't work with curses, use addstr instead
                  print 'right'
                  motor.moveTo(motor.RIGHT)
              elif char == curses.KEY_LEFT:
                  print 'left '
                  motor.moveTo(motor.LEFT)
              char = screen.getch()
        
finally:
    # shut down cleanly
    curses.nocbreak(); screen.keypad(0); curses.echo()
    curses.endwin()

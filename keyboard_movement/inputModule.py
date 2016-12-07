import curses
from motorModule import MotorModule

# get the curses screen window
motor = MotorModule()
screen = curses.initscr()

# turn off input echoing
curses.noecho()

# respond to keys immediately (don't wait for enter)
curses.cbreak()

# map arrow keys to special values
screen.keypad(True)


try:
  while True:
    char = screen.getch()
    if char == ord('q'):
      motor.cleanUp()
      break
    elif char == curses.KEY_RIGHT:
      # print doesn't work with curses, use addstr instead
      print 'right'
      motor.moveTo(1)
    elif char == curses.KEY_LEFT:
      print 'left '
      motor.moveTo(-1)
    elif char == curses.KEY_UP:
      print 'up'
    elif char == curses.KEY_DOWN:
      print 'down'
finally:
  # shut down cleanly
  curses.nocbreak(); screen.keypad(0); curses.echo()
  curses.endwin()


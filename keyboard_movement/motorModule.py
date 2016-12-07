import RPi.GPIO as GPIO
import time

class Motor:

  def __init__(self):
      self.delay = 0.01
      self.pins  = [6, 13, 19, 26]
      self.move_table = [[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 1], [1, 0, 0, 1]]
          
      self.RIGHT = 1
      self.LEFT  = -1

      print "Set mode BCM"
      GPIO.setmode(GPIO.BCM)

      for pin in self.pins:
          print "Setup output port", pin
          GPIO.setup(pin, GPIO.OUT)

  # direction can be 1 or -1
  def moveTo(self, direction):
      step = 0
      for i in range(500):
          for pin in range(4):
              GPIO.output(self.pins[pin], self.move_table[step][pin])
            
          step += direction

          if direction == 1:
              if step == len(self.move_table):
                  step = 0
          if direction == -1:
              if step < 0:
                  step = len(self.move_table) - 1
          time.sleep(self.delay)

  def cleanUp(self):
      GPIO.cleanup()
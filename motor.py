import RPi.GPIO as GPIO
import time

print "Set mode BCM"
GPIO.setmode(GPIO.BCM)

pins = [6, 13, 19, 26]

move_table = [[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 1], [1, 0, 0, 1]]

delay = 0.01
for pin in pins:
    print "Setup output port", pin
    GPIO.setup(pin, GPIO.OUT)

move = 0

# direction can be 1 or -1
direction = -1

for i in range(500):
    for pin in range(4):
        GPIO.output(pins[pin], move_table[move][pin])
        # print pins[pin], move_table[move][pin]
    move = move + direction

    if direction == 1:
        if move == len(move_table):
            move = 0

    if direction == -1:
        if move < 0:
            move = len(move_table) - 1

    time.sleep(delay)
    # print


GPIO.cleanup()

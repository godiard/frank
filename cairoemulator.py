# movements emulator in a cairo canvas

import cairo

SCALE = 10


class Emulator:

    def __init__(self, width, height):
        print "CAIRO CANVAS %f x %f" % (width, height)
        self._surface = cairo.ImageSurface(cairo.FORMAT_ARGB32,
                                           int(width * SCALE),
                                           int(height * SCALE))
        self._ctx = cairo.Context(self._surface)
        self._ctx.set_source_rgba(1, 0, 0, 1)
        self._ctx.set_line_width(1.0)
        self._on = False
        self._x = 0.0
        self._y = 0.0

    def on(self):
        self._on = True

    def off(self):
        self._on = False

    def moveTo(self, direction, axis, steps_by_mm):
        increment = float(direction) / steps_by_mm * SCALE
        print "directtion %f steps_by_mm %f increment %f" % (
            float(direction), steps_by_mm, increment)
        if axis == 'X':
            self._x = self._x + increment
        else:
            self._y = self._y + increment

        if self._on:
            self._ctx.line_to(self._x, self._y)
            self._ctx.stroke()
            self._ctx.move_to(self._x, self._y)
        else:
            self._ctx.move_to(self._x, self._y)
        print "X %f Y %f" % (self._x, self._y)

    def save(self):
        self._surface.flush()
        self._surface.write_to_png("output.png")

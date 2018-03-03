# movements emulator in a cairo canvas

import cairo

SCALE = 10

class Emulator:

    def __init__(self, width, height):
        print "CAIRO CANVAS %f x %f" % (width, height)
        self._surface = cairo.ImageSurface(cairo.FORMAT_ARGB32,
                                           int(width * SCALE), int(height * SCALE))
        self._ctx = cairo.Context(self._surface)
        self._ctx.set_source_rgba(1, 0, 0, 1)
        self._ctx.set_line_width(0.2)
        self._ctx.scale(10.0, 10.0)
        self._on = False

    def on(self):
        self._on = True

    def off(self):
        self._on = False

    def move_to(self, x, y):
        if self._on:
            print "CAIRO LINE_TO %f %f" % (x, y)
            #self._ctx.new_path()
            self._ctx.line_to(x, y)
            self._ctx.stroke()
            self._ctx.move_to(x, y)
        else:
            print "CAIRO MOVE_TO %f %f" % (x, y)
            self._ctx.move_to(x, y)

    def save(self):
        self._surface.flush()
        self._surface.write_to_png("output.png")

from rit_window import *

class CGIengine:
    def __init__(self, myWindow, defaction):
        self.w_width = myWindow.width
        self.w_height = myWindow.height;
        self.win = myWindow
        self.keypressed = 1
        self.default_action = defaction


    def rasterizeLine(self, x0, y0, x1, y1, r, g, b):
        dx = abs(x1 - x0) # midpoint method
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy  # error

        while True:
            # give (x0, y0) to color
            self.win.set_pixel(x0, y0, r, g, b)
            # Check end point
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    def rasterizeInterpolatedLines(self, vertices, colors, n):
        # vertices array of vertex position
        # color array of color
        # n number of line
        for i in range(n):
            x0, y0 = vertices[i * 4], vertices[i * 4 + 1]
            x1, y1 = vertices[i * 4 + 2], vertices[i * 4 + 3]
            r0, g0, b0 = colors[i * 6], colors[i * 6 + 1], colors[i * 6 + 2]
            r1, g1, b1 = colors[i * 6 + 3], colors[i * 6 + 4], colors[i * 6 + 5]
            # Bresenham's line algorithm with color interpolation
            dx = abs(x1 - x0)
            dy = abs(y1 - y0)
            sx = 1 if x0 < x1 else -1
            sy = 1 if y0 < y1 else -1
            err = dx - dy
            # total number of steps (for interpolation)
            steps = max(dx, dy) + 1
            # color increments per step
            dr = (r1 - r0) / steps if steps > 0 else 0
            dg = (g1 - g0) / steps if steps > 0 else 0
            db = (b1 - b0) / steps if steps > 0 else 0
            r, g, b = r0, g0, b0  # Start with the initial color
            while True:
                self.win.set_pixel(x0, y0, r, g, b)

                if x0 == x1 and y0 == y1:
                    break
                e2 = 2 * err
                if e2 > -dy:
                    err -= dy
                    x0 += sx
                if e2 < dx:
                    err += dx
                    y0 += sy

                r += dr
                g += dg
                b += db

    # go is called on every update of the window display loop
    # have your engine draw stuff in the window.
    def go(self):
        if (self.keypressed == 1):
            # default scene
            self.default_action()

        if (self.keypressed == 2):
            # clear the framebuffer
            self.win.clearFB(0, 0, 0)  # clear with black

        # push the window's framebuffer to the window
        self.win.applyFB()

    def keyboard(self, key):
        if (key == '1'):
            self.keypressed = 1
            self.go()
        if (key == '2'):
            self.keypressed = 2
            self.go()
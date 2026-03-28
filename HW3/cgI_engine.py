from rit_window import *
from vertex import *

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
    def edgeFunction(self, v0, v1, p):
        return (v1.y - v0.y) * (p.x - v0.x) - (v1.x - v0.x) * (p.y - v0.y)

    def rasterizeTriangle(self, p0, p1, p2):
        # Bounding box four coors
        # p are class Vertex
        min_x = max(min(p0.x, p1.x, p2.x), 0)
        max_x = min(max(p0.x, p1.x, p2.x), self.w_width - 1)
        min_y = max(min(p0.y, p1.y, p2.y), 0)
        max_y = min(max(p0.y, p1.y, p2.y), self.w_height - 1)

        # Precompute edge functions
        area = self.edgeFunction(p0, p1, p2)
        if area == 0:
            return

        # Loop over every pixel in the bounding box
        for y in range(int(min_y), int(max_y) + 1):
            for x in range(int(min_x), int(max_x) + 1):
                p = Vertex(x, y, 0, 0, 0)

                # Calculate edge functions
                w0 = self.edgeFunction(p1, p2, p)
                w1 = self.edgeFunction(p2, p0, p)
                w2 = self.edgeFunction(p0, p1, p)

                # Check if the point is inside the triangle
                if w0 >= 0 and w1 >= 0 and w2 >= 0:  # Inside test for clockwise order
                    # Barycentric coordinates
                    alpha = w0 / area
                    beta = w1 / area
                    gamma = w2 / area

                    # Interpolated color
                    r = alpha * p0.r + beta * p1.r + gamma * p2.r
                    g = alpha * p0.g + beta * p1.g + gamma * p2.g
                    b = alpha * p0.b + beta * p1.b + gamma * p2.b

                    # Draw
                    self.win.set_pixel(x, y, r, g, b)

    def drawTriangles(self, vertex_data, colors, indices):
        # vertex_pos – array of vertex positions
        # colors – array of color values (attached to each vertex)
        # indices – array of indexes that define triangles
        for i in range(0, len(indices), 3):
            # Get the indices for the vertices of the triangle
            idx0, idx1, idx2 = indices[i], indices[i + 1], indices[i + 2]

            # Get vertex positions
            x0, y0 = vertex_data[idx0 * 2], vertex_data[idx0 * 2 + 1]
            x1, y1 = vertex_data[idx1 * 2], vertex_data[idx1 * 2 + 1]
            x2, y2 = vertex_data[idx2 * 2], vertex_data[idx2 * 2 + 1]

            # Get vertex colors
            r0, g0, b0 = colors[idx0 * 3], colors[idx0 * 3 + 1], colors[idx0 * 3 + 2]
            r1, g1, b1 = colors[idx1 * 3], colors[idx1 * 3 + 1], colors[idx1 * 3 + 2]
            r2, g2, b2 = colors[idx2 * 3], colors[idx2 * 3 + 1], colors[idx2 * 3 + 2]

            # Create Vertices
            p0 = Vertex(x0, y0, r0, g0, b0)
            p1 = Vertex(x1, y1, r1, g1, b1)
            p2 = Vertex(x2, y2, r2, g2, b2)

            self.rasterizeTriangle(p0, p1, p2)
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
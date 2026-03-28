from rit_window import *
from vertex import *
import numpy as np


class CGIengine:
    def __init__(self, myWindow, defaction):
        self.w_width = myWindow.width
        self.w_height = myWindow.height
        self.win = myWindow
        self.default_action = defaction
        self.matrix_stack = []  # Initialize the matrix stack

    def go(self):
        self.default_action()
        self.win.applyFB()

    def clearFB(self, r, g, b):
        self.win.clearFB(r, g, b)

    def pushMatrix(self, matrix):
        if len(self.matrix_stack) > 0:
            top_matrix = self.matrix_stack[-1]
            # Multiply the top of the stack with the new matrix and push the result
            self.matrix_stack.append(np.dot(top_matrix, matrix))
        else:
            # If stack is empty, push the matrix as the first item
            self.matrix_stack.append(matrix)

    def popMatrix(self):
        if len(self.matrix_stack) > 0:
            self.matrix_stack.pop()
        else:
            print("Error: Matrix stack is empty!")

    def getCurrentMatrix(self):
        if len(self.matrix_stack) > 0:
            return self.matrix_stack[-1]
        else:
            return self.identity()  # Return identity if stack is empty

    def identity(self):
        return np.eye(3)

    def translate(self, x, y):
        return np.array([[1, 0, x],
                         [0, 1, y],
                         [0, 0, 1]])

    def scale(self, sx, sy):
        return np.array([[sx, 0, 0],
                         [0, sy, 0],
                         [0, 0, 1]])

    def rotate(self, angle):
        rad = np.deg2rad(angle)
        cos_a, sin_a = np.cos(rad), np.sin(rad)
        return np.array([[cos_a, -sin_a, 0],
                         [sin_a, cos_a, 0],
                         [0, 0, 1]])

    def normalize(self, t, b, r, l):
        # Create a 3x3 normalization matrix to map from world coordinates to normalized device coordinates [-1, 1]
        return np.array([
            [2 / (r - l), 0, -(r + l) / (r - l)],  # Normalize X to [-1, 1]
            [0, 2 / (t - b), -(t + b) / (t - b)],  # Normalize Y to [-1, 1]
            [0, 0, 1]  # Identity for homogeneous coordinate
        ])

    def defineViewWindow(self, t, b, r, l):
        self.view_h = t - b
        self.view_w = r - l
        self.sx = self.view_w / 2
        self.sy = self.view_h / 2
        self.ox = l + self.view_w / 2
        self.oy = b + self.view_h / 2

        # Construct the transformation matrix (3x3)
        self.view_window = np.array([
            [self.sx, 0, self.ox],  # Scale X and apply offset
            [0, self.sy, self.oy],  # Scale Y and apply offset
            [0, 0, 1]  # Homogeneous coordinate
        ])

    def clipLine(self, P0, P1, top, bottom, right, left):
        # Define region codes
        INSIDE, LEFT, RIGHT, BOTTOM, TOP = 0, 1, 2, 4, 8

        def computeOutCode(x, y):
            code = INSIDE
            if x < left:
                code |= LEFT
            elif x > right:
                code |= RIGHT
            if y < bottom:
                code |= BOTTOM
            elif y > top:
                code |= TOP
            return code

        x0, y0 = P0.x, P0.y
        x1, y1 = P1.x, P1.y
        outcode0 = computeOutCode(x0, y0)
        outcode1 = computeOutCode(x1, y1)

        while True:
            if outcode0 == 0 and outcode1 == 0:  # Trivially accept
                return [P0, P1]
            elif outcode0 & outcode1 != 0:  # Trivially reject
                return []
            else:
                outcode_out = outcode0 if outcode0 != 0 else outcode1
                if outcode_out & TOP:
                    x = x0 + (x1 - x0) * (top - y0) / (y1 - y0)
                    y = top
                elif outcode_out & BOTTOM:
                    x = x0 + (x1 - x0) * (bottom - y0) / (y1 - y0)
                    y = bottom
                elif outcode_out & RIGHT:
                    y = y0 + (y1 - y0) * (right - x0) / (x1 - x0)
                    x = right
                elif outcode_out & LEFT:
                    y = y0 + (y1 - y0) * (left - x0) / (x1 - x0)
                    x = left

                if outcode_out == outcode0:
                    x0, y0 = x, y
                    outcode0 = computeOutCode(x0, y0)
                else:
                    x1, y1 = x, y
                    outcode1 = computeOutCode(x1, y1)

    def clipPoly(self, vertices, top, bottom, right, left):


        # Clip against the top edge
        retPoly = self.shpc(vertices, 0, top)

        if len(retPoly) > 0:
            # Clip against the bottom edge
            retPoly = self.shpc(retPoly, 1, bottom)

        if len(retPoly) > 0:
            # Clip against the right edge
            retPoly = self.shpc(retPoly, 2, right)

        if len(retPoly) > 0:
            # Clip against the left edge
            retPoly = self.shpc(retPoly, 3, left)

        if len(retPoly) > 0:
            # Convert the clipped polygon to triangles
            retPoly = self.polyToTriangles(retPoly)
        else:
            print("Polygon fully clipped. No triangles left.")

        return retPoly

    def shpc(self, vertices, edge, boundary):

        def inside(v):
            if edge == 0:  # Top edge
                return v.y <= boundary
            elif edge == 1:  # Bottom edge
                return v.y >= boundary
            elif edge == 2:  # Right edge
                return v.x <= boundary
            elif edge == 3:  # Left edge
                return v.x >= boundary

        def intersect(v1, v2, boundary, edge):

            if edge == 0:  # Top edge
                t = (boundary - v1.y) / (v2.y - v1.y)
                x = v1.x + t * (v2.x - v1.x)
                y = boundary
            elif edge == 1:  # Bottom edge
                t = (boundary - v1.y) / (v2.y - v1.y)
                x = v1.x + t * (v2.x - v1.x)
                y = boundary
            elif edge == 2:  # Right edge
                t = (boundary - v1.x) / (v2.x - v1.x)
                x = boundary
                y = v1.y + t * (v2.y - v1.y)
            elif edge == 3:  # Left edge
                t = (boundary - v1.x) / (v2.x - v1.x)
                x = boundary
                y = v1.y + t * (v2.y - v1.y)

            # Interpolate color values based on the t value
            r = v1.r + t * (v2.r - v1.r)
            g = v1.g + t * (v2.g - v1.g)
            b = v1.b + t * (v2.b - v1.b)

            return Vertex(x, y, r, g, b)

        clipped = []
        prev_vertex = vertices[-1]
        prev_inside = inside(prev_vertex)

        for curr_vertex in vertices:
            curr_inside = inside(curr_vertex)

            if curr_inside:
                if not prev_inside:
                    # Add intersection point
                    intersection = intersect(prev_vertex, curr_vertex, boundary, edge)
                    clipped.append(intersection)
                # Add current vertex
                clipped.append(curr_vertex)
            elif prev_inside:
                # Add intersection point
                intersection = intersect(prev_vertex, curr_vertex, boundary, edge)
                clipped.append(intersection)

            prev_vertex = curr_vertex
            prev_inside = curr_inside

        return clipped



    def polyToTriangles(self, vertices):

        triangles = []
        if len(vertices) < 3:
            return triangles  # Not enough vertices to form a triangle

        # Fan triangulation: triangle (0, 1, 2), (0, 2, 3), ..., (0, n-2, n-1)
        for i in range(1, len(vertices) - 1):
            triangles.append([vertices[0], vertices[i], vertices[i + 1]])

        return triangles


    def drawClippedLine(self, P0, P1, top, bottom, right, left, r, g, b):
        clipped_line = self.clipLine(P0, P1, top, bottom, right, left)
        if len(clipped_line) > 0:
            # Draw the clipped line if any part of it remains visible
            self.rasterizeLine(clipped_line[0].x, clipped_line[0].y, clipped_line[1].x, clipped_line[1].y, r, g, b)

    def rasterizeLine(self, x0, y0, x1, y1, r, g, b):
        # Implement Bresenham's line algorithm or DDA for rasterization
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy

        while True:
            # Set the pixel at the current position
            self.win.set_pixel(int(x0), int(y0), r, g, b)

            # Break when the end point is reached
            if x0 == x1 and y0 == y1:
                break

            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    def drawTriangles(self, vertex_data, color_data, index_data, modelT, normT, global_pixels_set):
        transformed_triangles = []  # To store the transformed vertices

        for i in range(0, len(index_data), 3):
            idx0 = index_data[i]
            idx1 = index_data[i + 1]
            idx2 = index_data[i + 2]

            # Apply model transformations to the vertices
            p0 = np.array([vertex_data[idx0 * 2], vertex_data[idx0 * 2 + 1], 1])
            p1 = np.array([vertex_data[idx1 * 2], vertex_data[idx1 * 2 + 1], 1])
            p2 = np.array([vertex_data[idx2 * 2], vertex_data[idx2 * 2 + 1], 1])

            # Apply model and normalization transforms
            p0 = np.dot(modelT, p0)
            p1 = np.dot(modelT, p1)
            p2 = np.dot(modelT, p2)

            # Apply normalization to bring coordinates into [-1, 1] range
            p0 = np.dot(normT, p0)
            p1 = np.dot(normT, p1)
            p2 = np.dot(normT, p2)

            # Apply the view window transform to convert to screen space
            p0 = np.dot(self.view_window, p0)
            p1 = np.dot(self.view_window, p1)
            p2 = np.dot(self.view_window, p2)

            # Create vertex objects and store the transformed vertices
            v0 = Vertex(p0[0], p0[1], color_data[idx0 * 3], color_data[idx0 * 3 + 1], color_data[idx0 * 3 + 2])
            v1 = Vertex(p1[0], p1[1], color_data[idx1 * 3], color_data[idx1 * 3 + 1], color_data[idx1 * 3 + 2])
            v2 = Vertex(p2[0], p2[1], color_data[idx2 * 3], color_data[idx2 * 3 + 1], color_data[idx2 * 3 + 2])

            transformed_triangles.append((v0, v1, v2))  # Store the transformed vertices

            # self.rasterizeTriangle(v0, v1, v2, global_pixels_set)

        return transformed_triangles  # Return the transformed vertices

    def rasterizeTriangle(self, p0, p1, p2, global_pixels_set):
        min_x = max(0, int(min(p0.x, p1.x, p2.x)))
        max_x = min(self.w_width - 1, int(max(p0.x, p1.x, p2.x)))
        min_y = max(0, int(min(p0.y, p1.y, p2.y)))
        max_y = min(self.w_height - 1, int(max(p0.y, p1.y, p2.y)))

        def edgeFunction(v0, v1, p):
            return (p[0] - v0.x) * (v1.y - v0.y) - (p[1] - v0.y) * (v1.x - v0.x)

        area = edgeFunction(p0, p1, [p2.x, p2.y])

        if abs(area) < 1e-7:
            return  # Degenerate triangle, skip

        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                p = [x, y]
                w0 = edgeFunction(p1, p2, p)
                w1 = edgeFunction(p2, p0, p)
                w2 = edgeFunction(p0, p1, p)

                if w0 >= 0 and w1 >= 0 and w2 >= 0:
                    # Normalize weights by area to get barycentric coordinates
                    lambda0 = w0 / area
                    lambda1 = w1 / area
                    lambda2 = w2 / area

                    # Interpolate colors using barycentric coordinates
                    r = lambda0 * p0.r + lambda1 * p1.r + lambda2 * p2.r
                    g = lambda0 * p0.g + lambda1 * p1.g + lambda2 * p2.g
                    b = lambda0 * p0.b + lambda1 * p1.b + lambda2 * p2.b

                    # Avoid setting the same pixel across the entire scene
                    if (x, y) not in global_pixels_set:
                        global_pixels_set.add((x, y))
                        self.win.set_pixel(x, y, r, g, b)

    def keyboard(self, key):
        if key == '1':
            self.keypressed = 1
            self.go()
        if key == '2':
            self.keypressed = 2
            self.go()

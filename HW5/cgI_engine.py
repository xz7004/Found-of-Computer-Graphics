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
        #self.view_window = None  # Initialize the view window to None

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

    def drawTriangles(self, vertex_data, color_data, index_data, modelT, normT, global_pixels_set):

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

            # Create vertex objects and rasterize
            v0 = Vertex(p0[0], p0[1], color_data[idx0 * 3], color_data[idx0 * 3 + 1], color_data[idx0 * 3 + 2])
            v1 = Vertex(p1[0], p1[1], color_data[idx1 * 3], color_data[idx1 * 3 + 1], color_data[idx1 * 3 + 2])
            v2 = Vertex(p2[0], p2[1], color_data[idx2 * 3], color_data[idx2 * 3 + 1], color_data[idx2 * 3 + 2])

            self.rasterizeTriangle(v0, v1, v2, global_pixels_set)

    def rasterizeTriangle(self, p0, p1, p2, global_pixels_set):
        min_x = max(0, int(min(p0.x, p1.x, p2.x)))
        max_x = min(self.w_width - 1, int(max(p0.x, p1.x, p2.x)))
        min_y = max(0, int(min(p0.y, p1.y, p2.y)))
        max_y = min(self.w_height - 1, int(max(p0.y, p1.y, p2.y)))

        def edgeFunction(v0, v1, p):
            return (p[0] - v0.x) * (v1.y - v0.y) - (p[1] - v0.y) * (v1.x - v0.x)

        area = edgeFunction(p0, p1, [p2.x, p2.y])

        if abs(area) < 1e-5:
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
        if (key == '1'):
            self.keypressed = 1
            self.go()
        if (key == '2'):
            self.keypressed = 2
            self.go()

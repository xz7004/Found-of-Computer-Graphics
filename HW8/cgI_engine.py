from rit_window import *
from vertex import *
import numpy as np


class CGIengine:
    def __init__(self, myWindow, defaction):
        self.w_width = myWindow.width
        self.w_height = myWindow.height
        self.win = myWindow
        self.default_action = defaction
        self.matrix_stack = [np.identity(4)]
        self.drawn_pixels = set()
        # Z-buffer
        self.z_buffer = np.full((self.w_width, self.w_height), np.inf)

    def go(self):
        self.drawn_pixels.clear()
        self.z_buffer.fill(np.inf)
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
        if len(self.matrix_stack) > 1:
            self.matrix_stack.pop()
        else:
            print("Error: Matrix stack is empty or only contains the identity matrix!")

    def getCurrentMatrix(self):
        if len(self.matrix_stack) > 0:
            return self.matrix_stack[-1]
        else:
            return np.eye(4)  # Return identity if stack is empty

    def identity3D(self):
        return np.eye(4)

    def translate3D(self, tx, ty, tz):
        return np.array([
            [1, 0, 0, tx],
            [0, 1, 0, ty],
            [0, 0, 1, tz],
            [0, 0, 0, 1]
        ])

    def scale3D(self, sx, sy, sz):
        return np.array([
            [sx, 0, 0, 0],
            [0, sy, 0, 0],
            [0, 0, sz, 0],
            [0, 0, 0, 1]
        ])

    def rotateX(self, angle_degrees):
        angle = np.radians(angle_degrees)  # degrees to radians
        cos_theta = np.cos(angle)
        sin_theta = np.sin(angle)
        return np.array([
            [1, 0, 0, 0],
            [0, cos_theta, -sin_theta, 0],
            [0, sin_theta, cos_theta, 0],
            [0, 0, 0, 1]
        ])

    def rotateY(self, angle_degrees):
        angle = np.radians(angle_degrees)
        cos_theta = np.cos(angle)
        sin_theta = np.sin(angle)
        return np.array([
            [cos_theta, 0, sin_theta, 0],
            [0, 1, 0, 0],
            [-sin_theta, 0, cos_theta, 0],
            [0, 0, 0, 1]
        ])

    def rotateZ(self, angle_degrees):
        angle = np.radians(angle_degrees)
        cos_theta = np.cos(angle)
        sin_theta = np.sin(angle)
        return np.array([
            [cos_theta, -sin_theta, 0, 0],
            [sin_theta, cos_theta, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

    def ortho3D(self, l, r, b, t, n, f):
        # Check for any invalid or zero divisions in the ranges, and adjust if necessary
        if n == f:
            f += 1e-5

        if l == r:
            r += 1e-5

        if b == t:
            t += 1e-5
        # orthographic projection matrix
        return np.array([
            [2 / (r - l), 0, 0, -(r + l) / (r - l)],
            [0, 2 / (t - b), 0, -(t + b) / (t - b)],
            [0, 0, -2 / (f - n), -(f + n) / (f - n)],
            [0, 0, 0, 1]
        ])

    def frustum3D(self, l, r, b, t, n, f):
        return np.array([
            [(2 * n) / (r - l), 0, (r + l) / (r - l), 0],
            [0, (2 * n) / (t - b), (t + b) / (t - b), 0],
            [0, 0, -(f + n) / (f - n), -(2 * f * n) / (f - n)],
            [0, 0, -1, 0]
        ])

    def lookAt(self, eye, lookat, up):
        n = np.array(eye) - np.array(lookat)
        n = n / np.linalg.norm(n)
        u = np.cross(up, n)
        u = u / np.linalg.norm(u)
        v = np.cross(n, u)

        # Rotation matrix for the camera
        rotation = np.array([
            [u[0], u[1], u[2], 0],
            [v[0], v[1], v[2], 0],
            [n[0], n[1], n[2], 0],
            [0, 0, 0, 1]
        ])

        # Translation matrix for the camera
        translation = np.array([
            [1, 0, 0, -eye[0]],
            [0, 1, 0, -eye[1]],
            [0, 0, 1, -eye[2]],
            [0, 0, 0, 1]
        ])

        # Combine rotation and translation matrices to generate the view matrix
        view_matrix = rotation @ translation
        return view_matrix

    def defineViewWindow(self, t, b, r, l):
        self.view_window = np.array([
            [(r - l) / 2.0, 0, 0, (r + l) / 2.0],
            [0, (t - b) / 2.0, 0, (t + b) / 2.0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

    def drawTriangles3D(self, vertex_data, index_data, modelT, viewT, projectionT, r, g, b, wr=None, wg=None, wb=None):
        for i in range(0, len(index_data), 3):
            idx0, idx1, idx2 = index_data[i], index_data[i + 1], index_data[i + 2]

            p0 = np.array([vertex_data[idx0 * 3], vertex_data[idx0 * 3 + 1], vertex_data[idx0 * 3 + 2], 1])
            p1 = np.array([vertex_data[idx1 * 3], vertex_data[idx1 * 3 + 1], vertex_data[idx1 * 3 + 2], 1])
            p2 = np.array([vertex_data[idx2 * 3], vertex_data[idx2 * 3 + 1], vertex_data[idx2 * 3 + 2], 1])

            p0 = np.dot(projectionT, np.dot(viewT, np.dot(modelT, p0)))
            p1 = np.dot(projectionT, np.dot(viewT, np.dot(modelT, p1)))
            p2 = np.dot(projectionT, np.dot(viewT, np.dot(modelT, p2)))

            p0 /= p0[3]
            p1 /= p1[3]
            p2 /= p2[3]

            p0 = np.dot(self.view_window, p0)
            p1 = np.dot(self.view_window, p1)
            p2 = np.dot(self.view_window, p2)

            v0 = Vertex(p0[0], p0[1], p0[2], r, g, b)
            v1 = Vertex(p1[0], p1[1], p1[2], r, g, b)
            v2 = Vertex(p2[0], p2[1], p2[2], r, g, b)

            self.rasterizeTriangle(v0, v1, v2, r, g, b, wr, wg, wb)

    def rasterizeTriangle(self, v0, v1, v2, fill_r, fill_g, fill_b, edge_r=None, edge_g=None, edge_b=None):

        min_x = max(0, int(min(v0.x, v1.x, v2.x)))
        max_x = min(self.w_width - 1, int(max(v0.x, v1.x, v2.x)))
        min_y = max(0, int(min(v0.y, v1.y, v2.y)))
        max_y = min(self.w_height - 1, int(max(v0.y, v1.y, v2.y)))

        # Barycentric coordinates
        def edgeFunction(v0, v1, p):
            return (p[0] - v0.x) * (v1.y - v0.y) - (p[1] - v0.y) * (v1.x - v0.x)

        area = edgeFunction(v0, v1, [v2.x, v2.y])

        if abs(area) < 1e-7:
            return
        edge_threshold = 0.01  #  0.01-0.05

        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                p = [x, y]
                w0 = edgeFunction(v1, v2, p)
                w1 = edgeFunction(v2, v0, p)
                w2 = edgeFunction(v0, v1, p)

                if w0 >= 0 and w1 >= 0 and w2 >= 0:
                    lambda0 = w0 / area
                    lambda1 = w1 / area
                    lambda2 = w2 / area

                    z = lambda0 * v0.z + lambda1 * v1.z + lambda2 * v2.z

                    if z < self.z_buffer[x, y]:
                        self.z_buffer[x, y] = z

                        if edge_r is not None and (
                                abs(lambda0) < edge_threshold or
                                abs(lambda1) < edge_threshold or
                                abs(lambda2) < edge_threshold
                        ):

                            self.win.set_pixel(x, y, edge_r, edge_g, edge_b)
                        else:
                            color_r = lambda0 * v0.r + lambda1 * v1.r + lambda2 * v2.r
                            color_g = lambda0 * v0.g + lambda1 * v1.g + lambda2 * v2.g
                            color_b = lambda0 * v0.b + lambda1 * v1.b + lambda2 * v2.b
                            self.win.set_pixel(x, y, color_r, color_g, color_b)

    def drawTriangles3Dwireframe(self, vertex_data, index_data, modelT, viewT, projectionT, r, g, b, wr, wg, wb):

        for i in range(0, len(index_data), 3):
            idx0, idx1, idx2 = index_data[i], index_data[i + 1], index_data[i + 2]

            p0 = np.array([vertex_data[idx0 * 3], vertex_data[idx0 * 3 + 1], vertex_data[idx0 * 3 + 2], 1])
            p1 = np.array([vertex_data[idx1 * 3], vertex_data[idx1 * 3 + 1], vertex_data[idx1 * 3 + 2], 1])
            p2 = np.array([vertex_data[idx2 * 3], vertex_data[idx2 * 3 + 1], vertex_data[idx2 * 3 + 2], 1])

            p0 = np.dot(projectionT, np.dot(viewT, np.dot(modelT, p0)))
            p1 = np.dot(projectionT, np.dot(viewT, np.dot(modelT, p1)))
            p2 = np.dot(projectionT, np.dot(viewT, np.dot(modelT, p2)))

            p0 /= p0[3]
            p1 /= p1[3]
            p2 /= p2[3]

            p0 = np.dot(self.view_window, p0)
            p1 = np.dot(self.view_window, p1)
            p2 = np.dot(self.view_window, p2)

            v0 = Vertex(p0[0], p0[1], p0[2], r, g, b)
            v1 = Vertex(p1[0], p1[1], p1[2], r, g, b)
            v2 = Vertex(p2[0], p2[1], p2[2], r, g, b)

            self.rasterizeTriangleWithWireframe(v0, v1, v2, r, g, b, wr, wg, wb)

    def rasterizeTriangleWithWireframe(self, v0, v1, v2, fill_r, fill_g, fill_b, edge_r, edge_g, edge_b):

        min_x = max(0, int(min(v0.x, v1.x, v2.x)))
        max_x = min(self.w_width - 1, int(max(v0.x, v1.x, v2.x)))
        min_y = max(0, int(min(v0.y, v1.y, v2.y)))
        max_y = min(self.w_height - 1, int(max(v0.y, v1.y, v2.y)))

        def edgeFunction(v0, v1, p):
            return (p[0] - v0.x) * (v1.y - v0.y) - (p[1] - v0.y) * (v1.x - v0.x)

        area = edgeFunction(v0, v1, [v2.x, v2.y])

        if abs(area) < 1e-7:
            return

        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                p = [x, y]
                w0 = edgeFunction(v1, v2, p)
                w1 = edgeFunction(v2, v0, p)
                w2 = edgeFunction(v0, v1, p)

                if w0 >= 0 and w1 >= 0 and w2 >= 0:

                    lambda0 = w0 / area
                    lambda1 = w1 / area
                    lambda2 = w2 / area

                    z = lambda0 * v0.z + lambda1 * v1.z + lambda2 * v2.z

                    if z < self.z_buffer[x, y]:
                        self.z_buffer[x, y] = z

                        edge_threshold = 0.1

                        if (abs(lambda0) < edge_threshold or
                                abs(lambda1) < edge_threshold or
                                abs(lambda2) < edge_threshold):
                            self.win.set_pixel(x, y, edge_r, edge_g, edge_b)
                        else:
                            # Pixel is inside the triangle, draw with fill color
                            color_r = lambda0 * v0.r + lambda1 * v1.r + lambda2 * v2.r
                            color_g = lambda0 * v0.g + lambda1 * v1.g + lambda2 * v2.g
                            color_b = lambda0 * v0.b + lambda1 * v1.b + lambda2 * v2.b
                            self.win.set_pixel(x, y, color_r, color_g, color_b)

    def keyboard(self, key):
        if key == '1':
            self.keypressed = 1
            self.go()
        if key == '2':
            self.keypressed = 2
            self.go()

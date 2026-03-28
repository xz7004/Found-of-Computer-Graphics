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
            self.matrix_stack.append(np.dot(top_matrix, matrix))
        else:

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
        if n == f:
            f += 1e-5
        if l == r:
            r += 1e-5
        if b == t:
            t += 1e-5
        return np.array([
            [2 / (r - l), 0, 0, -(r + l) / (r - l)],
            [0, 2 / (t - b), 0, -(t + b) / (t - b)],
            [0, 0, -2 / (f - n), -(f + n) / (f - n)],
            [0, 0, 0, 1]
        ])

    def lookAt(self, eye, lookat, up):
        n = np.array(eye) - np.array(lookat)
        n = n / np.linalg.norm(n)
        u = np.cross(up, n)
        u = u / np.linalg.norm(u)
        v = np.cross(n, u)

        rotation = np.array([
            [u[0], u[1], u[2], 0],
            [v[0], v[1], v[2], 0],
            [n[0], n[1], n[2], 0],
            [0, 0, 0, 1]
        ])

        translation = np.array([
            [1, 0, 0, -eye[0]],
            [0, 1, 0, -eye[1]],
            [0, 0, 1, -eye[2]],
            [0, 0, 0, 1]
        ])
        view_matrix = rotation @ translation
        return view_matrix

    def defineViewWindow(self, t, b, r, l):
        self.view_window = np.array([
            [(r - l) / 2.0, 0, 0, (r + l) / 2.0],
            [0, (t - b) / 2.0, 0, (t + b) / 2.0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

    def drawTrianglesTextures(self, vertex_pos, indices, uv, im, modelT, viewT, projectionT):

        texture = np.asarray(im) / 255.0  # Normalize the image to [0, 1]
        tex_h, tex_w, _ = texture.shape

        for i in range(0, len(indices), 3):
            idx0, idx1, idx2 = indices[i], indices[i + 1], indices[i + 2]

            p0 = np.array([vertex_pos[idx0 * 3], vertex_pos[idx0 * 3 + 1], vertex_pos[idx0 * 3 + 2], 1])
            p1 = np.array([vertex_pos[idx1 * 3], vertex_pos[idx1 * 3 + 1], vertex_pos[idx1 * 3 + 2], 1])
            p2 = np.array([vertex_pos[idx2 * 3], vertex_pos[idx2 * 3 + 1], vertex_pos[idx2 * 3 + 2], 1])

            p0 = projectionT @ viewT @ modelT @ p0
            p1 = projectionT @ viewT @ modelT @ p1
            p2 = projectionT @ viewT @ modelT @ p2

            p0 /= p0[3]
            p1 /= p1[3]
            p2 /= p2[3]

            p0[0] = int((p0[0] + 1) * 0.5 * self.w_width)
            p0[1] = int((p0[1] + 1) * 0.5 * self.w_height)  # Fix: Adjust Y-axis mapping
            p1[0] = int((p1[0] + 1) * 0.5 * self.w_width)
            p1[1] = int((p1[1] + 1) * 0.5 * self.w_height)  # Fix: Adjust Y-axis mapping
            p2[0] = int((p2[0] + 1) * 0.5 * self.w_width)
            p2[1] = int((p2[1] + 1) * 0.5 * self.w_height)  # Fix: Adjust Y-axis mapping

            uv0 = [uv[idx0 * 2], uv[idx0 * 2 + 1]]
            uv1 = [uv[idx1 * 2], uv[idx1 * 2 + 1]]
            uv2 = [uv[idx2 * 2], uv[idx2 * 2 + 1]]

            self.rasterizeTriangle(p0, p1, p2, uv0, uv1, uv2, texture, tex_w, tex_h)

    def rasterizeTriangle(self, p0, p1, p2, uv0, uv1, uv2, texture, tex_w, tex_h):
        min_x = max(0, int(min(p0[0], p1[0], p2[0])))
        max_x = min(self.w_width - 1, int(max(p0[0], p1[0], p2[0])))
        min_y = max(0, int(min(p0[1], p1[1], p2[1])))
        max_y = min(self.w_height - 1, int(max(p0[1], p1[1], p2[1])))

        def edgeFunction(v0, v1, p):
            return (p[0] - v0[0]) * (v1[1] - v0[1]) - (p[1] - v0[1]) * (v1[0] - v0[0])

        area = edgeFunction(p0, p1, p2)

        if abs(area) < 1e-7:
            #print("Triangle has zero area; skipping.")
            return

        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                p = [x, y]
                w0 = edgeFunction(p1, p2, p)
                w1 = edgeFunction(p2, p0, p)
                w2 = edgeFunction(p0, p1, p)

                if w0 >= 0 and w1 >= 0 and w2 >= 0:

                    w0 /= area
                    w1 /= area
                    w2 /= area

                    z = w0 * p0[2] + w1 * p1[2] + w2 * p2[2]

                    if z < self.z_buffer[x, y]:
                        self.z_buffer[x, y] = z

                        u = w0 * uv0[0] + w1 * uv1[0] + w2 * uv2[0]
                        v = w0 * uv0[1] + w1 * uv1[1] + w2 * uv2[1]

                        tex_x = int(u * (tex_w - 1))
                        tex_y = int(v * (tex_h - 1))

                        tex_x = np.clip(tex_x, 0, tex_w - 1)
                        tex_y = np.clip(tex_y, 0, tex_h - 1)

                        color = texture[tex_y, tex_x]
                        #print(f"Pixel ({x}, {y}): Z={z}, Color={color}")

                        self.win.set_pixel(x, y, color[0], color[1], color[2])


    def drawTrianglesCheckerboard(self, vertex_pos, indices, uvs, color1, color2, checksize, modelT, viewT,
                                  projectionT):

        for i in range(0, len(indices), 3):

            idx0, idx1, idx2 = indices[i], indices[i + 1], indices[i + 2]

            p0 = np.array([vertex_pos[idx0 * 3], vertex_pos[idx0 * 3 + 1], vertex_pos[idx0 * 3 + 2], 1])
            p1 = np.array([vertex_pos[idx1 * 3], vertex_pos[idx1 * 3 + 1], vertex_pos[idx1 * 3 + 2], 1])
            p2 = np.array([vertex_pos[idx2 * 3], vertex_pos[idx2 * 3 + 1], vertex_pos[idx2 * 3 + 2], 1])

            p0 = projectionT @ viewT @ modelT @ p0
            p1 = projectionT @ viewT @ modelT @ p1
            p2 = projectionT @ viewT @ modelT @ p2

            p0 /= p0[3]
            p1 /= p1[3]
            p2 /= p2[3]

            p0[0] = int((p0[0] + 1) * 0.5 * self.w_width)
            p0[1] = int((p0[1] + 1) * 0.5 * self.w_height)
            p1[0] = int((p1[0] + 1) * 0.5 * self.w_width)
            p1[1] = int((p1[1] + 1) * 0.5 * self.w_height)
            p2[0] = int((p2[0] + 1) * 0.5 * self.w_width)
            p2[1] = int((p2[1] + 1) * 0.5 * self.w_height)

            uv0 = [uvs[idx0 * 2], uvs[idx0 * 2 + 1]]
            uv1 = [uvs[idx1 * 2], uvs[idx1 * 2 + 1]]
            uv2 = [uvs[idx2 * 2], uvs[idx2 * 2 + 1]]

            self.rasterizeTriangleCheckerboard(p0, p1, p2, uv0, uv1, uv2, color1, color2, checksize)

    def rasterizeTriangleCheckerboard(self, p0, p1, p2, uv0, uv1, uv2, color1, color2, checksize):
        min_x = max(0, int(min(p0[0], p1[0], p2[0])))
        max_x = min(self.w_width - 1, int(max(p0[0], p1[0], p2[0])))
        min_y = max(0, int(min(p0[1], p1[1], p2[1])))
        max_y = min(self.w_height - 1, int(max(p0[1], p1[1], p2[1])))

        def edgeFunction(v0, v1, p):
            return (p[0] - v0[0]) * (v1[1] - v0[1]) - (p[1] - v0[1]) * (v1[0] - v0[0])

        area = edgeFunction(p0, p1, p2)

        if abs(area) < 1e-7:
            return

        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                p = [x, y]
                w0 = edgeFunction(p1, p2, p)
                w1 = edgeFunction(p2, p0, p)
                w2 = edgeFunction(p0, p1, p)

                if w0 >= 0 and w1 >= 0 and w2 >= 0:

                    w0 /= area
                    w1 /= area
                    w2 /= area

                    u = w0 * uv0[0] + w1 * uv1[0] + w2 * uv2[0]
                    v = w0 * uv0[1] + w1 * uv1[1] + w2 * uv2[1]

                    if checksize > 0:
                        urow = int(u / checksize) % 2
                        vrow = int(v / checksize) % 2

                        color = color1 if urow == vrow else color2

                        self.win.set_pixel(x, y, color[0], color[1], color[2])

    def drawTrianglesGeneral(self, vertex_pos, indices, normals, uvs, uniforms, v_shader, f_shader):

        for i in range(0, len(indices), 3):

            idx0, idx1, idx2 = indices[i], indices[i + 1], indices[i + 2]

            vertex_input = [
                {"pos": vertex_pos[idx0 * 3:idx0 * 3 + 3], "normal": normals[idx0 * 3:idx0 * 3 + 3],
                 "uv": uvs[idx0 * 2:idx0 * 2 + 2]},
                {"pos": vertex_pos[idx1 * 3:idx1 * 3 + 3], "normal": normals[idx1 * 3:idx1 * 3 + 3],
                 "uv": uvs[idx1 * 2:idx1 * 2 + 2]},
                {"pos": vertex_pos[idx2 * 3:idx2 * 3 + 3], "normal": normals[idx2 * 3:idx2 * 3 + 3],
                 "uv": uvs[idx2 * 2:idx2 * 2 + 2]},
            ]

            v0 = v_shader(vertex_input[0], uniforms)
            v1 = v_shader(vertex_input[1], uniforms)
            v2 = v_shader(vertex_input[2], uniforms)

            self.rasterizeTriangleGeneral(v0["pos"], v1["pos"], v2["pos"], v0["varyings"], v1["varyings"],
                                          v2["varyings"], f_shader, uniforms)

    def rasterizeTriangleGeneral(self, p0, p1, p2, vary0, vary1, vary2, f_shader, uniforms):

        p0[0] = int((p0[0] + 1) * 0.5 * self.w_width)
        p0[1] = int((p0[1] + 1) * 0.5 * self.w_height)
        p1[0] = int((p1[0] + 1) * 0.5 * self.w_width)
        p1[1] = int((p1[1] + 1) * 0.5 * self.w_height)
        p2[0] = int((p2[0] + 1) * 0.5 * self.w_width)
        p2[1] = int((p2[1] + 1) * 0.5 * self.w_height)
        # Compute bounding box
        min_x = max(0, int(min(p0[0], p1[0], p2[0])))
        max_x = min(self.w_width - 1, int(max(p0[0], p1[0], p2[0])))
        min_y = max(0, int(min(p0[1], p1[1], p2[1])))
        max_y = min(self.w_height - 1, int(max(p0[1], p1[1], p2[1])))

        def edgeFunction(v0, v1, p):
            return (p[0] - v0[0]) * (v1[1] - v0[1]) - (p[1] - v0[1]) * (v1[0] - v0[0])

        area = edgeFunction(p0, p1, p2)
        if abs(area) < 1e-7:
            return

        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                p = [x, y]
                w0 = edgeFunction(p1, p2, p)
                w1 = edgeFunction(p2, p0, p)
                w2 = edgeFunction(p0, p1, p)

                if w0 >= 0 and w1 >= 0 and w2 >= 0:
                    w0 /= area
                    w1 /= area
                    w2 /= area

                    varyings = {
                        key: w0 * np.array(vary0[key]) + w1 * np.array(vary1[key]) + w2 * np.array(vary2[key])
                        for key in vary0
                    }

                    z = w0 * p0[2] + w1 * p1[2] + w2 * p2[2]

                    if z < self.z_buffer[x, y]:
                        self.z_buffer[x, y] = z
                        color = f_shader(varyings, uniforms)
                        self.win.set_pixel(x, y, color[0], color[1], color[2])

    def keyboard(self, key):
        if key == '1':
            self.keypressed = 1
            self.go()
        if key == '2':
            self.keypressed = 2
            self.go()

from rit_window import *
from vertex import *
import numpy as np
import glm

class CGIengine:
    def __init__(self, myWindow, defaction):
        self.w_width = myWindow.width
        self.w_height = myWindow.height
        self.win = myWindow
        self.default_action = defaction
        self.matrix_stack = [np.identity(4)]
        self.drawn_pixels = set()
        # Z-buffer
        self.z_buffer = np.full((self.w_width, self.w_height), np.inf)  # Initialize z-buffer to infinity


    def go(self):
        self.drawn_pixels.clear()
        self.z_buffer.fill(np.inf)
        self.default_action()
        self.win.applyFB()

    def clearFB(self, r, g, b):
        self.win.clearFB(r, g, b)

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
        eye = np.array(eye)
        lookat = np.array(lookat)
        up = np.array(up)
        n = lookat - eye
        n = n / np.linalg.norm(n)
        u = np.cross(n, up)
        u = u / np.linalg.norm(u)
        v = np.cross(u, n)
        rotation = np.array([
            [u[0], u[1], u[2], 0],
            [v[0], v[1], v[2], 0],
            [-n[0], -n[1], -n[2], 0],
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

    def transform_vertex(self, vertex, modelT, viewT, projectionT):
        vertex_h = np.append(vertex, 1)
        transformed = projectionT @ viewT @ modelT @ vertex_h
        transformed /= transformed[3]
        return transformed[:3]


    def compute_normal(self, v0, v1, v2):
        edge1 = v1 - v0
        edge2 = v2 - v0
        normal = np.cross(edge1, edge2)
        return normal / np.linalg.norm(normal)

    def drawTrianglesPhong(self, vertex_pos, indices, normals, modelT, viewT, projectionT, ocolor, scolor, k, exponent,
                           lightpos, lightcolor, amb_color, doGouraud):

        lightpos_view = viewT @ np.append(lightpos, 1.0)
        lightpos_view = lightpos_view[:3] / lightpos_view[3]  # Normalize

        transformed_vertices = []
        transformed_normals = []
        gouraud_colors = []

        for i in range(0, len(vertex_pos), 3):
            vertex = np.array([vertex_pos[i], vertex_pos[i + 1], vertex_pos[i + 2]])
            normal = np.array([normals[i], normals[i + 1], normals[i + 2]])

            # vertex to world and view space
            world_pos = modelT @ np.append(vertex, 1.0)
            view_pos = viewT @ world_pos
            view_pos = view_pos[:3] / view_pos[3]

            # vertex to clip space for rasterization
            clip_pos = projectionT @ np.append(view_pos, 1.0)
            clip_pos /= clip_pos[3]

            # Transform to view space
            view_normal = viewT[:3, :3] @ (modelT[:3, :3] @ normal)
            view_normal /= np.linalg.norm(view_normal)  # Normalize

            # Gouraud shading
            if doGouraud:
                view_dir = -view_pos / np.linalg.norm(view_pos)
                color = self.phong_shading(view_pos, view_normal, view_dir, ocolor, scolor, k, exponent, lightpos_view,
                                           lightcolor, amb_color)
                gouraud_colors.append(color)

            transformed_vertices.append((clip_pos[:3], view_pos))
            transformed_normals.append(view_normal)

        # Rasterize each triangle
        for i in range(0, len(indices), 3):
            idx0, idx1, idx2 = indices[i], indices[i + 1], indices[i + 2]
            #print(f"Processing triangle indices: {idx0}, {idx1}, {idx2}")

            # Extract transformed data
            p0, v0_view = transformed_vertices[idx0]
            p1, v1_view = transformed_vertices[idx1]
            p2, v2_view = transformed_vertices[idx2]

            n0 = transformed_normals[idx0]
            n1 = transformed_normals[idx1]
            n2 = transformed_normals[idx2]

            # screen space
            p0 = np.dot(self.view_window, np.append(p0, 1))
            p1 = np.dot(self.view_window, np.append(p1, 1))
            p2 = np.dot(self.view_window, np.append(p2, 1))

            if doGouraud:
                c0, c1, c2 = gouraud_colors[idx0], gouraud_colors[idx1], gouraud_colors[idx2]
                v0 = Vertex(p0[0], p0[1], p0[2], c0[0], c0[1], c0[2])
                v1 = Vertex(p1[0], p1[1], p1[2], c1[0], c1[1], c1[2])
                v2 = Vertex(p2[0], p2[1], p2[2], c2[0], c2[1], c2[2])
            else:
                v0 = Vertex(p0[0], p0[1], p0[2], 0, 0, 0)
                v1 = Vertex(p1[0], p1[1], p1[2], 0, 0, 0)
                v2 = Vertex(p2[0], p2[1], p2[2], 0, 0, 0)

            self.rasterizeTriangle(v0, v1, v2, ocolor, scolor, k, exponent, lightpos_view, lightcolor, amb_color,
                                   doGouraud, n0, n1, n2, v0_view, v1_view, v2_view)

    def rasterizeTriangle(self, v0, v1, v2, ocolor, scolor, k, exponent, lightpos_view, lightcolor, amb_color,
                          doGouraud, n0, n1, n2, v0_view, v1_view, v2_view):

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

                        if doGouraud:

                            color_r = lambda0 * v0.r + lambda1 * v1.r + lambda2 * v2.r
                            color_g = lambda0 * v0.g + lambda1 * v1.g + lambda2 * v2.g
                            color_b = lambda0 * v0.b + lambda1 * v1.b + lambda2 * v2.b
                        else:
                            interp_normal = lambda0 * n0 + lambda1 * n1 + lambda2 * n2
                            interp_normal /= np.linalg.norm(interp_normal)

                            #view space
                            fragment_pos_view = (
                                    lambda0 * v0_view +
                                    lambda1 * v1_view +
                                    lambda2 * v2_view
                            )

                            view_dir = -fragment_pos_view  # View direction
                            view_dir /= np.linalg.norm(view_dir)

                            color = self.phong_shading(
                                fragment_pos_view, interp_normal, view_dir,
                                ocolor, scolor, k, exponent, lightpos_view, lightcolor, amb_color
                            )

                            color_r, color_g, color_b = np.clip(color, 0.0, 1.0)

                        self.win.set_pixel(x, y, color_r, color_g, color_b)

    def phong_shading(self, pos, normal, view_dir, ocolor, scolor, k, exponent, lightpos, lightcolor, amb_color):
        normal = np.array(normal)
        normal /= np.linalg.norm(normal)

        view_dir = np.array(view_dir)
        view_dir /= np.linalg.norm(view_dir)

        light_dir = np.array(lightpos) - np.array(pos)
        light_dir /= np.linalg.norm(light_dir)

        ambient = k[0] * np.array(amb_color) * np.array(ocolor)

        ndotl = max(np.dot(normal, light_dir), 0.0)  # Ensure no negative contribution
        diffuse = k[1] * ndotl * np.array(lightcolor) * np.array(ocolor)

        reflect_dir = 2 * np.dot(light_dir, normal) * normal - light_dir
        reflect_dir /= np.linalg.norm(reflect_dir)
        rdotv = max(np.dot(reflect_dir, view_dir), 0.0)  # Reflect-View dot product
        specular = k[2] * (rdotv ** exponent) * np.array(scolor) * np.array(lightcolor)

        final_color = ambient + diffuse + specular
        return np.clip(final_color, 0.0, 1.0)  # Clamp the result to ensure valid RGB values

    def keyboard(self, key):
        if key == '1':
            self.keypressed = 1
            self.go()
        if key == '2':
            self.keypressed = 2
            self.go()

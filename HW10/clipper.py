from vertex import Vertex


class Clipper:
    def clipLine(self, P0, P1, top, bottom, right, left, near, far):
        # Cohen-Sutherland line clipping in 3D
        INSIDE, LEFT, RIGHT, BOTTOM, TOP, NEAR, FAR = 0, 1, 2, 4, 8, 16, 32

        def computeOutCode(x, y, z):
            # Compute the region code for a point (x, y, z)
            code = INSIDE
            if x < left:
                code |= LEFT
            elif x > right:
                code |= RIGHT
            if y < bottom:
                code |= BOTTOM
            elif y > top:
                code |= TOP
            if z < near:
                code |= NEAR
            elif z > far:
                code |= FAR
            return code

        # Start and end points
        x0, y0, z0 = P0.x, P0.y, P0.z
        x1, y1, z1 = P1.x, P1.y, P1.z
        outcode0 = computeOutCode(x0, y0, z0)
        outcode1 = computeOutCode(x1, y1, z1)

        while True:
            if outcode0 == 0 and outcode1 == 0:
                # Both points inside
                return [P0, P1]
            elif outcode0 & outcode1 != 0:
                # Both points outside, no line to draw
                return []
            else:
                # At least one point is outside
                outcode_out = outcode0 if outcode0 != 0 else outcode1
                if outcode_out & TOP:
                    t = (top - y0) / (y1 - y0)
                    x = x0 + t * (x1 - x0)
                    y = top
                    z = z0 + t * (z1 - z0)
                elif outcode_out & BOTTOM:
                    t = (bottom - y0) / (y1 - y0)
                    x = x0 + t * (x1 - x0)
                    y = bottom
                    z = z0 + t * (z1 - z0)
                elif outcode_out & RIGHT:
                    t = (right - x0) / (x1 - x0)
                    x = right
                    y = y0 + t * (y1 - y0)
                    z = z0 + t * (z1 - z0)
                elif outcode_out & LEFT:
                    t = (left - x0) / (x1 - x0)
                    x = left
                    y = y0 + t * (y1 - y0)
                    z = z0 + t * (z1 - z0)
                elif outcode_out & NEAR:
                    t = (near - z0) / (z1 - z0)
                    x = x0 + t * (x1 - x0)
                    y = y0 + t * (y1 - y0)
                    z = near
                elif outcode_out & FAR:
                    t = (far - z0) / (z1 - z0)
                    x = x0 + t * (x1 - x0)
                    y = y0 + t * (y1 - y0)
                    z = far

                # Replace the outside point with the new intersection point
                if outcode_out == outcode0:
                    P0 = Vertex(x, y, z, P0.r, P0.g, P0.b)
                    x0, y0, z0 = x, y, z
                    outcode0 = computeOutCode(x0, y0, z0)
                else:
                    P1 = Vertex(x, y, z, P1.r, P1.g, P1.b)
                    x1, y1, z1 = x, y, z
                    outcode1 = computeOutCode(x1, y1, z1)

    def clipPoly(self, vertices, top, bottom, right, left, near, far):
        # Clip polygon against all 6 edges: top, bottom, right, left, near, far
        retPoly = self.shpc(vertices, 0, top)
        if len(retPoly) > 0:
            retPoly = self.shpc(retPoly, 1, bottom)
        if len(retPoly) > 0:
            retPoly = self.shpc(retPoly, 2, right)
        if len(retPoly) > 0:
            retPoly = self.shpc(retPoly, 3, left)
        if len(retPoly) > 0:
            retPoly = self.shpc(retPoly, 4, near)
        if len(retPoly) > 0:
            retPoly = self.shpc(retPoly, 5, far)

        if len(retPoly) > 0:
            # If there's anything left, convert to triangles
            retPoly = self.polyToTriangles(retPoly)
        else:
            print("Polygon fully clipped. No triangles left.")

        return retPoly

    def shpc(self, vertices, edge, boundary):
        # Clip a polygon against a specific edge (0=top, 1=bottom, 2=right, 3=left, 4=near, 5=far)

        def inside(v):
            # Check if vertex is inside the clip boundary
            if edge == 0:  # Top
                return v.y <= boundary
            elif edge == 1:  # Bottom
                return v.y >= boundary
            elif edge == 2:  # Right
                return v.x <= boundary
            elif edge == 3:  # Left
                return v.x >= boundary
            elif edge == 4:  # Near
                return v.z >= boundary
            elif edge == 5:  # Far
                return v.z <= boundary

        def intersect(v1, v2, boundary, edge):
            # Find where the edge intersects the boundary
            if edge == 0:  # Top
                t = (boundary - v1.y) / (v2.y - v1.y)
                x = v1.x + t * (v2.x - v1.x)
                y = boundary
                z = v1.z + t * (v2.z - v1.z)
            elif edge == 1:  # Bottom
                t = (boundary - v1.y) / (v2.y - v1.y)
                x = v1.x + t * (v2.x - v1.x)
                y = boundary
                z = v1.z + t * (v2.z - v1.z)
            elif edge == 2:  # Right
                t = (boundary - v1.x) / (v2.x - v1.x)
                x = boundary
                y = v1.y + t * (v2.y - v1.y)
                z = v1.z + t * (v2.z - v1.z)
            elif edge == 3:  # Left
                t = (boundary - v1.x) / (v2.x - v1.x)
                x = boundary
                y = v1.y + t * (v2.y - v1.y)
                z = v1.z + t * (v2.z - v1.z)
            elif edge == 4:  # Near
                t = (boundary - v1.z) / (v2.z - v1.z)
                x = v1.x + t * (v2.x - v1.x)
                y = v1.y + t * (v2.y - v1.y)
                z = boundary
            elif edge == 5:  # Far
                t = (boundary - v1.z) / (v2.z - v1.z)
                x = v1.x + t * (v2.x - v1.x)
                y = v1.y + t * (v2.y - v1.y)
                z = boundary

            # Return the new vertex at the intersection
            r = v1.r + t * (v2.r - v1.r)
            g = v1.g + t * (v2.g - v1.g)
            b = v1.b + t * (v2.b - v1.b)

            return Vertex(x, y, z, r, g, b)

        clipped = []
        prev_vertex = vertices[-1]
        prev_inside = inside(prev_vertex)

        # Loop through vertices and clip against the boundary
        for curr_vertex in vertices:
            curr_inside = inside(curr_vertex)

            if curr_inside:
                if not prev_inside:
                    # Add intersection point before entering
                    intersection = intersect(prev_vertex, curr_vertex, boundary, edge)
                    clipped.append(intersection)
                # Add current vertex since it's inside
                clipped.append(curr_vertex)
            elif prev_inside:
                # Add intersection point when leaving
                intersection = intersect(prev_vertex, curr_vertex, boundary, edge)
                clipped.append(intersection)

            prev_vertex = curr_vertex
            prev_inside = curr_inside

        return clipped

    def polyToTriangles(self, vertices):
        # Convert the polygon to a set of triangles using a fan pattern

        triangles = []
        if len(vertices) < 3:
            return triangles  # No triangle can be formed

        # Fan triangulation: split polygon into triangles
        for i in range(1, len(vertices) - 1):
            triangles.append([vertices[0], vertices[i], vertices[i + 1]])

        return triangles

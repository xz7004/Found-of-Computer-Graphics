class Vertex:
    def __init__(self, x, y, z, r=0, g=0, b=0, attributes=None):

        self.x, self.y, self.z = x, y, z
        self.r, self.g, self.b = r, g, b
        self.attributes = attributes or {}

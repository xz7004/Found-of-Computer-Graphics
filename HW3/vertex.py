class Vertex:
    def __init__(self, x, y, r, g, b):
        self.x = x
        self.y = y
        self.r = r
        self.g = g
        self.b = b

    def __repr__(self):
        return f"Vertex(x={self.x}, y={self.y}, r={self.r}, g={self.g}, b={self.b})"

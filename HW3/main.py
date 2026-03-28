from rit_window import *
from cgI_engine import *
from vertex import Vertex
import numpy as np


def default_action ():
    myEngine.win.clearFB (0, 0, 0)
    P0 = Vertex (100, 100, 1.0, 0, 0)
    P1 = Vertex (300, 300, 0, 1.0, 0)
    P2 = Vertex (400, 100, 0, 0, 1.0)
    myEngine.rasterizeTriangle (P0, P1, P2)
    
    P0 = Vertex (500, 200, 1.0, 0, 0)
    P2 = Vertex (600, 150, 0.5, 0.5, 0)
    P1 = Vertex (600, 400, 0.196, 0, 0.196)
    myEngine.rasterizeTriangle (P0, P1, P2)
    
    P0 = Vertex (100, 500, 0, 1.0, 0)
    P1 = Vertex (300, 700, 0, 0.784, 0)
    P2 = Vertex (400, 500, 0, 0.392, 0)
    myEngine.rasterizeTriangle (P0, P1, P2)
    
    
window = RitWindow(800, 800)
myEngine = CGIengine (window, default_action)

def main():
    window.run (myEngine)
    



if __name__ == "__main__":
    main()

from rit_window import *
from cgI_engine import *
from vertex import Vertex
import numpy as np

vertex_data = np.array ([100, 100, 300, 300, 400, 100, 500, 200, 600, 150, 600, 400, 100, 500, 300, 700, 400, 500])
index_data = np.array ([0, 1, 2, 3, 5, 4, 6, 7, 8])
color_data = np.array ([1.0, 0, 0, 0, 1.0, 0, 0, 0, 1.0, 1.0, 0, 0, 0.5, 0.5, 0, 0.2, 0, 0.2, 0, 1.0, 0, 0, 0.8, 0, 0, 0.4, 0])


def default_action ():
    myEngine.win.clearFB (0, 0, 0)
    
    myEngine.drawTriangles (vertex_data, color_data, index_data)
    
    
window = RitWindow(800, 800)
myEngine = CGIengine (window, default_action)

def main():
    window.run (myEngine)
    



if __name__ == "__main__":
    main()

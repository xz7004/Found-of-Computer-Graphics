from rit_window import *
from cgI_engine import *
import numpy as np

vertex_positions = np.array([100, 100, 500, 500, 100, 500, 500, 100, 100, 300, 500, 300, 300, 100, 300, 500])

vertex_colors = np.array ([1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.25, 0.25, 0.25, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0])

def default_action():
    myEngine.win.clearFB (0.0, 0.0, 0.0)
    myEngine.rasterizeInterpolatedLines (vertex_positions, vertex_colors, 4)

window = RitWindow(800, 800)
myEngine = CGIengine (window, default_action)

def main():
    window.run (myEngine)

if __name__ == "__main__":
    main()

from rit_window import *
from cgI_engine import *


def default_action():
    myEngine.win.clearFB(0.0, 0.0, 0.0) # change this code
    myEngine.rasterizeLine (100, 100, 500, 500, 1.0, 0.0, 0.0)
    myEngine.rasterizeLine (100, 200, 500, 400, 0.0, 1.0, 0.0)
    myEngine.rasterizeLine (100, 300, 500, 300, 0.0, 0.0, 1.0)
    myEngine.rasterizeLine (100, 400, 500, 200, 1.0, 1.0, 0.0)
    myEngine.rasterizeLine (100, 500, 500, 100, 0.0, 1.0, 1.0)
    myEngine.rasterizeLine (200, 500, 400, 100, 1.0, 0.0, 1.0)
    myEngine.rasterizeLine (300, 500, 300, 100, 1.0, 1.0, 1.0)
    myEngine.rasterizeLine (400, 500, 200, 100, 0.5, 1.0, 1.0)
    myEngine.rasterizeLine (500, 450, 100, 150, 0.13, 0.784,0.039)
    myEngine.rasterizeLine (450, 100, 150, 500, 0.13, 0.784, 0.549)

window = RitWindow(800, 800)
myEngine = CGIengine (window, default_action)

def main():
    window.run (myEngine)

if __name__ == "__main__":
    main()

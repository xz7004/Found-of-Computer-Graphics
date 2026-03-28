from rit_window import *
from cgI_engine import *
from vertex import *
from clipper import *
from shapes import *
import numpy as np

tri1= [5.0, -2.0, -5.0, -1.0, 4.0, -2.0, -1.5, 3.0, -2.0] #red
tri2= [5.0, 2.0, -1.0, -1.0, -3.0, -1.0, -1.5, -5.0, -1.0] #green
tri3= [0.0, 5.0, -4.0, -1.0, 3.0, -4.0, 0.0, -5.0, 0.0] #blue

tris_idx = [0, 2, 1]


def default_action ():
    # clear the FB
    myEngine.win.clearFB (0, 0, 0)
    myEngine.defineViewWindow (800, 0, 800, 0)
    
    # draw
    modelT = myEngine.identity3D()
    viewT = myEngine.identity3D()
    projectionT = myEngine.ortho3D (-6.0, 6.0, -6.0, 6.0, 0.0, 5.0)
    myEngine.drawTriangles3D (tri1, tris_idx, modelT, viewT, projectionT, 1.0, 0, 0)
    myEngine.drawTriangles3D (tri2, tris_idx, modelT, viewT, projectionT, 0, 1.0, 0)
    myEngine.drawTriangles3D (tri3, tris_idx, modelT, viewT, projectionT, 0, 0, 1.0)
    
window = RitWindow(800, 800)
myEngine = CGIengine (window, default_action)

def main():
    window.run (myEngine)
    



if __name__ == "__main__":
    main()

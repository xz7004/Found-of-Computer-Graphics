from rit_window import *
from cgI_engine import *
from vertex import *
from clipper import *
from shapes import *
import numpy as np


def default_action ():
    # clear the FB
    myEngine.win.clearFB (0, 0, 0)
    myEngine.defineViewWindow (800, 0, 800, 0)

    viewT = myEngine.identity3D()
    projectionT = myEngine.ortho3D (-4.0, 4.0, -4.0, 4.0, 4.0, 4.0)


    # draw a cube
    modelT = (myEngine.translate3D (-2.0, 1.5, 0.0) @
              myEngine.rotateZ (-30.0) @
              myEngine.rotateY (-15.0) @
              myEngine.rotateX (-30.0) @
              myEngine.scale3D (1.5, 1.5, 1.5))
    myEngine.drawTriangles3Dwireframe (cube, cube_idx, modelT, viewT, projectionT, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0)

    # draw a cylinder
    modelT = (myEngine.translate3D (2.0, 1.5, 0.0) @
              myEngine.rotateZ (-30.0) @
              myEngine.rotateY (-15.0) @
              myEngine.rotateX (-30.0) @
              myEngine.scale3D (1.5, 1.5, 1.5))
    myEngine.drawTriangles3Dwireframe (cylinder, cylinder_idx, modelT, viewT, projectionT, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0)

    # draw a sphere
    modelT = (myEngine.translate3D (-2.0, -1.5, 0.0) @
              myEngine.rotateZ (-30.0) @
              myEngine.rotateY (-15.0) @
              myEngine.rotateX (-30.0) @
              myEngine.scale3D (2.0, 2.0, 2.0))
    myEngine.drawTriangles3Dwireframe (sphere, sphere_idx, modelT, viewT, projectionT, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0)

    # draw a cone
    modelT = (myEngine.translate3D (2.0, -1.5, 0.0) @
              myEngine.rotateZ (-30.0) @
              myEngine.rotateY (-15.0) @
              myEngine.rotateX (30.0) @
              myEngine.scale3D (1.5, 1.5, 1.5))
    myEngine.drawTriangles3Dwireframe (cone, cone_idx, modelT, viewT, projectionT, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0)


window = RitWindow(800, 800)
myEngine = CGIengine (window, default_action)

def main():
    window.run (myEngine)




if __name__ == "__main__":
    main()

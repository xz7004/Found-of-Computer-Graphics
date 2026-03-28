from rit_window import *
from cgI_engine import *
from shapes import *  # Import cube and cylinder shapes
import numpy as np

def default_action():
    myEngine.clearFB(0, 0, 0)
    myEngine.defineViewWindow(800, 0, 800, 0)

    viewT = myEngine.identity3D()
    projectionT = myEngine.ortho3D(-3.0, 3.0, -3.0, 3.0, 1.0, 10.0)

    myEngine.pushMatrix(myEngine.identity3D())

    # Bottom red cube
    myEngine.pushMatrix(
        myEngine.translate3D(0, -2.0, -4) @
        myEngine.scale3D(1.0, 0.3, 1.5)
    )
    myEngine.drawTriangles3Dwireframe(cube, cube_idx, myEngine.getCurrentMatrix(), viewT, projectionT, 1, 0, 0, 0, 0,
                                      0)  # Black wireframe
    myEngine.popMatrix()

    # Middle yellow cylinder
    myEngine.pushMatrix(
        myEngine.translate3D(0, -0.5, -4) @
        myEngine.scale3D(0.7, 2.7, 0.7)
    )
    myEngine.drawTriangles3Dwireframe(cylinder, cylinder_idx, myEngine.getCurrentMatrix(), viewT, projectionT, 1, 1, 0,
                                      1, 0, 0)  # Red wireframe
    myEngine.popMatrix()

    # Top red cube
    myEngine.pushMatrix(
        myEngine.translate3D(0, 1, -4) @
        myEngine.scale3D(1.0, 0.3, 1.5)
    )
    myEngine.drawTriangles3Dwireframe(cube, cube_idx, myEngine.getCurrentMatrix(), viewT, projectionT, 1, 0, 0, 0, 0,
                                      0)  # Black wireframe
    myEngine.popMatrix()

    # Top green cube
    myEngine.pushMatrix(
        myEngine.translate3D(0, 1.6, -4) @
        myEngine.rotateX(45) @
        myEngine.rotateY(45) @
        myEngine.rotateZ(0) @
        myEngine.scale3D(0.5, 0.5, 0.5)
    )
    myEngine.drawTriangles3Dwireframe(cube, cube_idx, myEngine.getCurrentMatrix(), viewT, projectionT, 0, 1, 0, 0, 0,
                                      0)  # Black wireframe
    myEngine.popMatrix()

window = RitWindow(800, 800)
myEngine = CGIengine(window, default_action)

def main():
    window.run(myEngine)

if __name__ == "__main__":
    main()

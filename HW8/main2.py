from rit_window import *
from cgI_engine import *
from shapes import *
import numpy as np

def create_pedestal(myEngine, position, viewT, projectionT):
    base_transform = myEngine.translate3D(position[0], position[1], position[2])

    # Bottom red cube
    myEngine.pushMatrix(base_transform @
                        myEngine.scale3D(0.7, 0.1, 1.0))
    myEngine.drawTriangles3Dwireframe(cube, cube_idx, myEngine.getCurrentMatrix(), viewT, projectionT, 1, 0, 0, 0, 0, 0)  # Black wireframe
    myEngine.popMatrix()

    # Middle yellow cylinder
    myEngine.pushMatrix(base_transform @
                        myEngine.translate3D(0, 0.8, 0) @
                        myEngine.scale3D(0.4, 1.6, 0.4))
    myEngine.drawTriangles3Dwireframe(cylinder, cylinder_idx, myEngine.getCurrentMatrix(), viewT, projectionT, 1, 1, 0, 1, 0, 0)  # Red wireframe
    myEngine.popMatrix()

    # Top red cube
    myEngine.pushMatrix(base_transform @
                        myEngine.translate3D(0, 1.6, 0)
                        @ myEngine.scale3D(0.7, 0.10, 1.0))
    myEngine.drawTriangles3Dwireframe(cube, cube_idx, myEngine.getCurrentMatrix(), viewT, projectionT, 1, 0, 0, 0, 0, 0)  # Black wireframe
    myEngine.popMatrix()

    # Top green cube
    myEngine.pushMatrix(base_transform @
                        myEngine.translate3D(0, 2.0, 0) @
                        myEngine.rotateX(45) @
                        myEngine.rotateY(45) @
                        myEngine.rotateZ(0) @
                        myEngine.scale3D(0.3, 0.3, 0.3))
    myEngine.drawTriangles3Dwireframe(cube, cube_idx, myEngine.getCurrentMatrix(), viewT, projectionT, 0, 1, 0, 0, 0, 0)  # Black wireframe
    myEngine.popMatrix()

def default_action ():
    # clear the FB
    myEngine.clearFB (0, 0, 0)
    myEngine.defineViewWindow (800, 0, 800, 0)

    eye = [0.0, 1.0, 4.0]
    lookat = [0.0, 0.0, 0.0]
    up = [0.0, 1.0, 0.0]
    viewT = myEngine.lookAt(eye, lookat, up)

    # Orthographic projection
    projectionT = myEngine.ortho3D(-4.0, 4.0, -4.0, 4.0, 1.0, 10.0)

    # Create the first pedestal at (2.0, 0.0, -3.0)
    create_pedestal(myEngine, [2.0, 0.0, -3.0], viewT, projectionT)

    # Create the second pedestal at (-2.0, 0.0, -5.0)
    create_pedestal(myEngine, [-2.0, 0.0, -5.0], viewT, projectionT)
    
    

    
window = RitWindow(800, 800)
myEngine = CGIengine (window, default_action)

def main():
    window.run (myEngine)
    



if __name__ == "__main__":
    main()

from rit_window import *
from cgI_engine import *
from shapes import *
import numpy as np


def default_action():
    # Clear the framebuffer
    myEngine.clearFB(0, 0, 0.5)
    myEngine.defineViewWindow(800, 0, 800, 0)

    eye = [0.0, 2.0, -4.0]
    lookat = [0.0, 0.0, -10.0]
    up = [0.0, 1.0, 0.0]
    viewT = myEngine.lookAt(eye, lookat, up)

    projectionT = myEngine.frustum3D(-6, 6, -6, 6, 8.0, 15.0)

    positions = [[1.0, 1.0, -10.0], [-1.0, 1.0, -15.0]]

    # Draw each pedestal
    for position in positions:
        base_transform = myEngine.translate3D(position[0], position[1], position[2])

        # Bottom red cube
        myEngine.pushMatrix(base_transform @
                            myEngine.scale3D(0.7, 0.1, 1.0))
        myEngine.drawTriangles3Dwireframe(cube, cube_idx, myEngine.getCurrentMatrix(), viewT, projectionT, 1, 0, 0, 0,
                                          0, 0)  # Black wireframe
        myEngine.popMatrix()

        # Middle yellow cylinder
        myEngine.pushMatrix(base_transform @
                            myEngine.translate3D(0, 0.8, 0) @
                            myEngine.scale3D(0.4, 1.6, 0.4))
        myEngine.drawTriangles3Dwireframe(cylinder, cylinder_idx, myEngine.getCurrentMatrix(), viewT, projectionT, 1, 1,
                                          0, 1, 0, 0)  # Red wireframe
        myEngine.popMatrix()

        # Top red cube
        myEngine.pushMatrix(base_transform @
                            myEngine.translate3D(0, 1.6, 0)
                            @ myEngine.scale3D(0.7, 0.10, 1.0))
        myEngine.drawTriangles3Dwireframe(cube, cube_idx, myEngine.getCurrentMatrix(), viewT, projectionT, 1, 0, 0, 0,
                                          0, 0)  # Black wireframe
        myEngine.popMatrix()

        # Top green cube
        myEngine.pushMatrix(base_transform @
                            myEngine.translate3D(0, 2.0, 0) @
                            myEngine.rotateX(45) @
                            myEngine.rotateY(45) @
                            myEngine.rotateZ(0) @
                            myEngine.scale3D(0.3, 0.3, 0.3))
        myEngine.drawTriangles3Dwireframe(cube, cube_idx, myEngine.getCurrentMatrix(), viewT, projectionT, 0, 1, 0, 0,
                                          0, 0)  # Black wireframe
        myEngine.popMatrix()


window = RitWindow(800, 800)
myEngine = CGIengine(window, default_action)


def main():
    window.run(myEngine)


if __name__ == "__main__":
    main()

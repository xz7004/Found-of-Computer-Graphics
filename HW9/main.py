from rit_window import *
from cgI_engine import *
from vertex import *
from clipper import *
from shapes import *
import numpy as np


def default_action():
    # Clear the framebuffer
    myEngine.win.clearFB(0.25, 0.25, 0.75)
    myEngine.defineViewWindow(800, 0, 800, 0)
    # Set up your camera
    eye = [0.0, 0.0, 0.0]
    lookat = [0.0, 0.0, -20.0]
    up = [0.0, 1.0, 0.0]
    viewT = myEngine.lookAt(eye, lookat, up)
    projectionT = myEngine.ortho3D(-3.0, 3.0, -3.0, 3.0, 0, 30.0)


    # Draw a sphere
    modelT = (myEngine.translate3D(0.0, 0.0, -5.0) @
              myEngine.scale3D(2.0, 2.0, 2.0))
    myEngine.drawTrianglesPhong(sphere, sphere_idx, sphere_normals, modelT, viewT, projectionT, [1.0, 0.0, 0.0],
                                [1.0, 1.0, 1.0], [0.2, 0.4, 0.4], 10.0, [-2.0, 3.0, -2.0], [1.0, 1.0, 1.0],
                                [1.0, 1.0, 1.0], True)


window = RitWindow(800, 800)
myEngine = CGIengine(window, default_action)


def main():
    window.run(myEngine)


if __name__ == "__main__":
    main()

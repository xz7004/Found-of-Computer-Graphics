from rit_window import *
from cgI_engine import *
from vertex import *
from clipper import *
from shapes import *
import numpy as np
from PIL import Image


def default_action ():
    # clear the FB
    myEngine.win.clearFB (.15, .15, .45)

    # set up your camera
    eye = [0.0, 0.0, 0.0]
    lookat = [0.0, 0.0, -20.0]
    up = [0.0, 1.0, 0.0]

    # Create the view matrix
    viewT = myEngine.lookAt(eye, lookat, up)
    #print(f"viewT:\n{viewT}")
    projectionT = myEngine.ortho3D(-3.0, 3.0, -3.0, 3.0, 0, 16.0)
    #print(f"projectionT:\n{projectionT}")

    # get your texture image
    im = Image.open("1_earth_16k.jpg")  # Replace with your texture path

    #draw a textured cube
    modelT = (
            myEngine.translate3D(1.0, 1.0, -5.0) @
            myEngine.rotateY(30) @
            myEngine.rotateX(30) @
            myEngine.scale3D(1.2, 1.2, 1.2))
    myEngine.drawTrianglesTextures (cube, cube_idx, cube_uv, im, modelT, viewT, projectionT)
    
    
    #draw a textured sphere
    modelT = (
            myEngine.translate3D (-1.5, 1.0, -5.0) @
            myEngine.scale3D (1.5, 1.5, 1.5))
    myEngine.drawTrianglesTextures (sphere, sphere_idx, sphere_uv, im, modelT, viewT, projectionT)
    
    #draw a textured cylinder
    modelT = (
            myEngine.translate3D (0.0, -1.0, -5.0) @
            myEngine.rotateY (30) @
            myEngine.rotateX (-30) @
            myEngine.scale3D (1.5, 1.5, 1.5))
    myEngine.drawTrianglesTextures (cylinder, cylinder_idx, cylinder_uv, im, modelT, viewT, projectionT)


window = RitWindow(800, 800)
myEngine = CGIengine (window, default_action)

def main():
    window.run (myEngine)
    



if __name__ == "__main__":
    main()

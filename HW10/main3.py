from rit_window import *
from cgI_engine import *
from vertex import *
from clipper import *
from shapes import *
import numpy as np
from PIL import Image

def texture_v(input, uniforms):
    modelT = uniforms["modelT"]
    viewT = uniforms["viewT"]
    projectionT = uniforms["projectionT"]
    pos = projectionT @ viewT @ modelT @ np.array([*input["pos"], 1])
    varyings = {"uv": input["uv"]}
    return {"pos": pos, "varyings": varyings}


def texture_check_f(varyings, uniforms):
    uv = varyings["uv"]
    checksize = uniforms["checksize"]
    color1 = uniforms["color1"]
    color2 = uniforms["color2"]
    urow = int(uv[0] / checksize) % 2
    vrow = int(uv[1] / checksize) % 2
    return color1 if urow == vrow else color2


def default_action():

    myEngine.win.clearFB(0.15, 0.15, 0.45)

    eye = [0.0, 0.0, 0.0]
    lookat = [0.0, 0.0, -20.0]
    up = [0.0, 1.0, 0.0]
    viewT = myEngine.lookAt(eye, lookat, up)
    projectionT = myEngine.ortho3D(-3.0, 3.0, -3.0, 3.0, 0, 15.0)

    uniforms = {
        "projectionT": projectionT,
        "viewT": viewT,
        "color1": [1.0, 0.0, 0.0],
        "color2": [1.0, 1.0, 0.0],
        "checksize": 0.1,
    }

    modelT = (
            myEngine.translate3D(1.0, 1.0, -5.0)
            @ myEngine.rotateY(30)
            @ myEngine.rotateX(30)
            @ myEngine.scale3D(1.2, 1.2, 1.2)
    )
    uniforms["modelT"] = modelT
    myEngine.drawTrianglesGeneral(cube, cube_idx, cube_normals, cube_uv, uniforms, texture_v, texture_check_f)

    modelT = (
            myEngine.translate3D(-1.5, 1.0, -5.0)
            @ myEngine.scale3D(1.5, 1.5, 1.5)
    )
    uniforms["modelT"] = modelT
    myEngine.drawTrianglesGeneral(sphere, sphere_idx, sphere_normals, sphere_uv, uniforms, texture_v, texture_check_f)

    modelT = (
            myEngine.translate3D(0.0, -1.0, -5.0)
            @ myEngine.rotateY(30)
            @ myEngine.rotateX(-30)
            @ myEngine.scale3D(1.5, 1.5, 1.5)
    )
    uniforms["modelT"] = modelT
    myEngine.drawTrianglesGeneral(cylinder, cylinder_idx, cylinder_normals, cylinder_uv, uniforms, texture_v,
                                  texture_check_f)

window = RitWindow(800, 800)
myEngine = CGIengine (window, default_action)

def main():
    window.run (myEngine)

if __name__ == "__main__":
    main()

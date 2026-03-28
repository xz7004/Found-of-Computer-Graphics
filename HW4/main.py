from rit_window import *
from cgI_engine import *
from vertex import *
import numpy as np


house_data = np.array ([0.0, 0.0,  0.0, 50.0,  50.0, 50.0,  50.0, 0.0 , 0.0, 50.0, 25.0, 75.0,  50.0, 50.0])
house_index_data = np.array ([0, 1, 2, 0, 2, 3, 4, 5, 6])
house_color_data = np.array ([1.0, 0, 0, 1.0, 0, 0, 1.0, 0, 0, 1.0, 0, 0, 0, 1.0, 0,  0, 1.0, 0,  0, 1.0, 0])


def default_action ():
    # clear the FB
    myEngine.clearFB (0, 0, 0)

    # our current model and normalization transform
    modelTransform = myEngine.identity()
    normTransform = myEngine.normalize (800.0, 0.0, 800.0, 0.0)

    #define a standard view window
    myEngine.defineViewWindow (800, 0, 800, 0)

    #draw the untransformed house
    myEngine.drawTriangles (house_data, house_color_data, house_index_data, modelTransform, normTransform)

    # translate the house
    modelTransform = myEngine.translate (100.0, 500.0)
    myEngine.drawTriangles (house_data, house_color_data, house_index_data, modelTransform, normTransform)

    # scale then translate
    modelTransform = np.dot(myEngine.translate(300.0, 400.0), myEngine.scale(3.5, 4.1))
    myEngine.drawTriangles (house_data, house_color_data, house_index_data, modelTransform, normTransform)

    # rotate then translate
    modelTransform = myEngine.translate(600.0, 400.0) @ myEngine.rotate(60.0)
    # Ensure you use matrix multiplication with the correct order


    myEngine.drawTriangles (house_data, house_color_data, house_index_data, modelTransform, normTransform)

    # zoom in on translated house and then stretch on bottom of screen
    modelTransform = myEngine.translate (100.0, 500.0)
    normTransform = myEngine.normalize (576.0, 499.0, 151.0, 100.0)
    myEngine.defineViewWindow (200, 50, 750, 150)
    myEngine.drawTriangles (house_data, house_color_data, house_index_data, modelTransform, normTransform)

window = RitWindow(800, 800)
myEngine = CGIengine (window, default_action)

def main():
    window.run (myEngine)




if __name__ == "__main__":
    main()

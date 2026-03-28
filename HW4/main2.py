from rit_window import *
from cgI_engine import *
import numpy as np

# House data: vertex positions, colors, and indices
house_data = np.array([0.0, 0.0, 0.0, 50.0, 50.0, 50.0, 50.0, 0.0, 0.0, 50.0, 25.0, 75.0, 50.0, 50.0])
house_index_data = np.array([0, 1, 2, 0, 2, 3, 4, 5, 6])
house_color_data = np.array([1.0, 0, 0, 1.0, 0, 0, 1.0, 0, 0, 1.0, 0, 0, 0, 1.0, 0, 0, 1.0, 0, 0, 1.0, 0])


def default_action():
    # Clear the framebuffer
    myEngine.clearFB(0, 0, 0)

    # Define view window
    myEngine.defineViewWindow(800, 0, 800, 0)

    # Identity matrix (no transformation)
    modelTransform = myEngine.identity()
    normTransform = myEngine.normalize(800.0, 0.0, 800.0, 0.0)

    # First row of houses
    for i in range(8):  # Three houses in the first row
        # Translate houses along the x-axis
        modelTransform = myEngine.translate(50 * i, 200)
        myEngine.drawTriangles(house_data, house_color_data, house_index_data, modelTransform, normTransform)

    # Second row of houses
    for i in range(8):  # Three houses in the second row
        modelTransform = myEngine.translate(50 * i,400)
        myEngine.drawTriangles(house_data, house_color_data, house_index_data, modelTransform, normTransform)


# Set up the window and engine
window = RitWindow(800, 800)
myEngine = CGIengine(window, default_action)


def main():
    window.run(myEngine)


if __name__ == "__main__":
    main()

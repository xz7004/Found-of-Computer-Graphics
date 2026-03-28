from rit_window import *
from cgI_engine import *
from vertex import *
import numpy as np

# a 10 x 10 square
square_data = np.array ([0.0, 0.0,  10.0, 0.0,  10.0, 10.0,  0.0, 10.0 ])
square_index_data = np.array ([0, 3, 2, 0, 2, 1])

# a 10 x 10 traingle
triangle_data = np.array ([0.0, 0.0,  10.0, 0.0,  5.0, 10.0])
triangle_index_data = np.array ([0, 2, 1])

red_color_data = np.array ([1.0, 0, 0, 1.0, 0, 0, 1.0, 0, 0, 1.0, 0, 0])
green_color_data = np.array ([0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0])
blue_color_data = np.array ([0.0, 0, 1.0, 0.0, 0, 1.0, 0.0, 0, 1.0, 0.0, 0.0, 1.0])


def default_action():
    myEngine.clearFB(0.0, 0.0, 0.0)  # Clear the framebuffer with black
    # Define view window
    #myEngine.defineViewWindow(1, -1, 1, -1)  # Set the view window from normalized to screen space
    global_pixels_set = set()

    # 1. Draw base (A)
    myEngine.pushMatrix(myEngine.translate(0, 0))  # Move the base part
    myEngine.pushMatrix(myEngine.scale(8, 1.5))  # Scale base appropriately
    myEngine.drawTriangles(square_data, red_color_data, square_index_data, myEngine.getCurrentMatrix(), myEngine.identity(), global_pixels_set)
    myEngine.popMatrix()  # Pop the base transformation

    # 2. Draw arm B (relative to base A)
    myEngine.pushMatrix(myEngine.translate(35, 15))  # Move the arm part up from the base
    myEngine.pushMatrix(myEngine.rotate(0))  # Rotate arm B
    myEngine.pushMatrix(myEngine.scale(0.8, 4))  # Scale arm appropriately
    myEngine.drawTriangles(square_data, green_color_data, square_index_data, myEngine.getCurrentMatrix(), myEngine.identity(), global_pixels_set)
    myEngine.popMatrix()  # Pop the arm B transformation

    # 3. Draw arm C (relative to arm B)
    myEngine.pushMatrix(myEngine.translate(0, 35))  # Move arm C up from arm B
    myEngine.pushMatrix(myEngine.rotate(45))  # Rotate arm C
    myEngine.pushMatrix(myEngine.scale(0.8, 4))  # Scale arm C appropriately
    myEngine.drawTriangles(square_data, green_color_data, square_index_data, myEngine.getCurrentMatrix(), myEngine.identity(), global_pixels_set)
    myEngine.popMatrix()  # Pop arm C transformation

    # 4. Draw arm D (relative to arm C)
    myEngine.pushMatrix(myEngine.translate(0, 40))  # Move arm D up from arm C
    myEngine.pushMatrix(myEngine.rotate(-90))  # Rotate arm D
    myEngine.pushMatrix(myEngine.scale(0.8, 4))  # Scale arm D appropriately
    myEngine.drawTriangles(square_data, green_color_data, square_index_data, myEngine.getCurrentMatrix(), myEngine.identity(), global_pixels_set)
    myEngine.popMatrix()  # Pop arm D transformation

    # 5. Draw head E (relative to arm D)
    myEngine.pushMatrix(myEngine.translate(0, 40))  # Move head E up from arm D
    myEngine.pushMatrix(myEngine.rotate(0))  # Rotate head E slightly back
    myEngine.pushMatrix(myEngine.scale(8, 8))  # Scale head appropriately
    myEngine.drawTriangles(triangle_data, blue_color_data, triangle_index_data, myEngine.getCurrentMatrix(), myEngine.identity(), global_pixels_set)
    myEngine.popMatrix()  # Pop the head transformation

    # Finally, pop the world-to-model transformation for Luxo as a whole
    myEngine.popMatrix()



# Initialize the window and engine
window = RitWindow(800, 800)
myEngine = CGIengine (window, default_action)
myEngine.defineViewWindow(1, -1, 1, -1)




def main():
    window.run(myEngine)

if __name__ == "__main__":
    main()

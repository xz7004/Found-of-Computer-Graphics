from rit_window import *
from cgI_engine import *
from vertex import *
import numpy as np


# a 10 x 10 square
square_data = np.array ([0.0, 0.0,  10.0, 0.0,  10.0, 10.0,  0.0, 10.0 ])
square_index_data = np.array ([0, 3, 2, 0, 2, 1])

# a 10 x 10 equalateral traingle
triangle_data = np.array ([0.0, 0.0,  10.0, 0.0,  5.0, 10.0])
triangle_index_data = np.array ([0, 2, 1])

red_color_data = np.array ([1.0, 0, 0, 1.0, 0, 0, 1.0, 0, 0, 1.0, 0, 0])
green_color_data = np.array ([0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0])
blue_color_data = np.array ([0.0, 0, 1.0, 0.0, 0, 1.0, 0.0, 0, 1.0, 0.0, 0.0, 1.0])



def draw_luxo(myEngine, scale, tx, ty):
    # Create a set to collect pixel data
    global_pixels_set = set()

    # Start with an identity matrix, push it onto the stack
    identity_matrix = myEngine.identity()
    myEngine.pushMatrix(identity_matrix)  # Push the identity matrix to start transformations

    # Translate to the desired position and scale for the whole Luxo
    translation_matrix = myEngine.translate(tx, ty)
    scaling_matrix = myEngine.scale(scale, scale)
    myEngine.pushMatrix(np.dot(translation_matrix, scaling_matrix))  # Combine transformations and push

    # Draw base (A)

    base_scale_matrix = myEngine.scale(8, 1.5)
    myEngine.pushMatrix(base_scale_matrix)  # Push base scaling transformation
    myEngine.drawTriangles(square_data, red_color_data, square_index_data, myEngine.getCurrentMatrix(), myEngine.identity(), global_pixels_set)
    myEngine.popMatrix()  # Pop base transformation

    # Draw arm B
    arm_B_transform = np.dot(myEngine.translate(35, 15), myEngine.scale(0.8, 4))
    myEngine.pushMatrix(arm_B_transform)  # Combine and push transformations for arm B
    myEngine.drawTriangles(square_data, green_color_data, square_index_data, myEngine.getCurrentMatrix(), myEngine.identity(), global_pixels_set)
    myEngine.popMatrix()  # Pop arm B transformation

    # Draw arm C
    arm_C_transform = np.dot(np.dot(myEngine.translate(35, 55), myEngine.rotate(45)), myEngine.scale(0.8, 4))
    myEngine.pushMatrix(arm_C_transform)  # Combine and push transformations for arm C
    myEngine.drawTriangles(square_data, green_color_data, square_index_data, myEngine.getCurrentMatrix(), myEngine.identity(), global_pixels_set)
    myEngine.popMatrix()  # Pop arm C transformation

    # Draw arm D
    arm_D_transform = np.dot(np.dot(myEngine.translate(5, 85), myEngine.rotate(-45)), myEngine.scale(0.8, 4))
    myEngine.pushMatrix(arm_D_transform)  # Combine and push transformations for arm D
    myEngine.drawTriangles(square_data, green_color_data, square_index_data, myEngine.getCurrentMatrix(), myEngine.identity(), global_pixels_set)
    myEngine.popMatrix()  # Pop arm D transformation

    # Draw head E
    head_transform = np.dot(np.dot(myEngine.translate(30, 115), myEngine.rotate(-45)), myEngine.scale(8, 8))
    #head_transform = np.dot(myEngine.translate(35, 40),myEngine.rotate(-45), myEngine.scale(8, 8))
    myEngine.pushMatrix(head_transform)  # Combine and push transformations for head E
    myEngine.drawTriangles(triangle_data, blue_color_data, triangle_index_data, myEngine.getCurrentMatrix(), myEngine.identity(), global_pixels_set)
    myEngine.popMatrix()  # Pop head transformation

    # Reset to the original transformation after each Luxo is drawn
    myEngine.popMatrix()  # Pop the initial translation and scaling
    myEngine.popMatrix()  # Pop the identity matrix to clean up


def default_action():
    myEngine.clearFB(0.0, 0.0, 0.0)  # Clear the framebuffer with black

    # original size Luxo at bottom left
    draw_luxo(myEngine, 1, 0, 0)

    # smaller Luxo in the middle of the window
    draw_luxo(myEngine, 0.5, 400, 400)

    # smallest Luxo in the top right of the window
    draw_luxo(myEngine, 0.25, 700, 700)

window = RitWindow(800, 800)
myEngine = CGIengine (window, default_action)
myEngine.defineViewWindow(1, -1, 1, -1)


def main():
    window.run (myEngine)


if __name__ == "__main__":
    main()

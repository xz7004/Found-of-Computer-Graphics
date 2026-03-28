from rit_window import *
from cgI_engine import *
from math import sin, cos, pi

def draw_spiral(center_x, center_y, turns, spacing, color):
    # I want to a spiral around
    angle = 0
    for i in range(turns * 360):
        angle_radians = angle * (pi / 180)  # degrees to radians
        x = int(center_x + spacing * angle_radians * cos(angle_radians))
        y = int(center_y + spacing * angle_radians * sin(angle_radians))
        if 0 <= x < window.width and 0 <= y < window.height:
            window.set_pixel(x, y, *color)
        angle += 1  # Increase angle to draw the spiral

def default_action():
    # Clear the screen with a blue background
    window.clearFB(0, 0.2, 0.6)  # Blue background

    # Draw a white spiral in the center of the window
    center_x, center_y = window.width // 2, window.height // 2
    draw_spiral(center_x, center_y, turns=10, spacing=5, color=(1.0, 1.0, 1.0))  # white

# Set up window and engine
window = RitWindow(800, 800)
myEngine = CGIengine(window, default_action)

def main():
    window.run(myEngine)

if __name__ == "__main__":
    main()

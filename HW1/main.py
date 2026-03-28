from rit_window import *
from cgI_engine import *


def default_action():
    window.clearFB (0, 0.2, 0.4)
    for x in range(50, 100):
        for y in range(800):
            window.set_pixel (x, y, 1.0, 0, 0)

window = RitWindow(800, 800)
myEngine = CGIengine (window, default_action)

def main():
    window.run (myEngine)

if __name__ == "__main__":
    main()

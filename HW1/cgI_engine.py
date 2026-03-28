from rit_window import *

class CGIengine:
    def __init__(self, myWindow, defaction):
        self.w_width = myWindow.width
        self.w_height = myWindow.height;
        self.win = myWindow
        self.keypressed = 1
        self.default_action = defaction
        
    # go is called on every update of the window display loop
    # have your engine draw stuff in the window.
    def go(self):
        if (self.keypressed == 1):
            # default scene
            self.default_action()
        
        if (self.keypressed == 2):
            # clear the framebuffer
            self.win.clearFB (0, 0, 0) #clear with black
            
        
        # push the window's framebuffer to the window
        self.win.applyFB()
        
    def keyboard (self, key) :
        if (key == '1'):
            self.keypressed = 1
            self.go()
        if (key == '2'):
            self.keypressed = 2
            self.go()

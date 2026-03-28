from rit_window import *
from cgI_engine import *
from vertex import *
import numpy as np

line1 = [25, 50, 20, 150];
line2 = [75, 100, 100, 75];
line3 = [25, 175, 100, 180];
line4 = [200, 175, 275, 100];
line5 = [175,230, 275, 200];
line6 = [25,280,280, 10];


def drawClippedLine (E, cL, r, g, b):
    P0 = Vertex (round(cL[0].x), round(cL[0].y), r, g, b)
    P1 = Vertex (round(cL[1].x), round(cL[1].y), r, g, b)
    E.rasterizeLine (P0.x, P0.y, P1.x, P1.y, r, g, b)

def default_action ():
    # clear the FB
    myEngine.win.clearFB (0, 0, 0)
    
    # draw the clip window
    myEngine.win.drawRect (250,50, 225, 50, 1.0, 1.0, 1.0)
    
    # first line: totally outside
    P0 = Vertex (line1[0], line1[1], 1.0, 1.0, 1.0)
    P1 = Vertex (line1[2], line1[3], 1.0, 1.0, 1.0)
    myEngine.rasterizeLine (P0.x, P0.y, P1.x, P1.y, 1.0, 1.0, 1.0)
    clippedLine = myEngine.clipLine (P0, P1, 250,50, 225, 50);
    if len(clippedLine) > 0:
        drawClippedLine (myEngine, clippedLine, 1.0, 0, 0)
        
  
    #  second line: totally inside
    P0 = Vertex (line2[0], line2[1], 1.0, 1.0, 1.0)
    P1 = Vertex (line2[2], line2[3], 1.0, 1.0, 1.0)
    myEngine.rasterizeLine (P0.x, P0.y, P1.x, P1.y, 1.0, 1.0, 1.0)
    clippedLine = myEngine.clipLine (P0, P1, 250,50, 225, 50);
    if len(clippedLine) > 0:
        drawClippedLine (myEngine, clippedLine, 0, 1.0, 0)
        
    
  
    #  third line: outside on left
    P0 = Vertex (line3[0], line3[1], 1.0, 1.0, 1.0)
    P1 = Vertex (line3[2], line3[3], 1.0, 1.0, 1.0)
    myEngine.rasterizeLine (P0.x, P0.y, P1.x, P1.y, 1.0, 1.0, 1.0)
    clippedLine = myEngine.clipLine (P0, P1, 250,50, 225, 50);
    if len(clippedLine) > 0:
        drawClippedLine (myEngine, clippedLine, 0, 0, 1.0)
        

  
    #fourth line: outside on right
    P0 = Vertex (line4[0], line4[1], 1.0, 1.0, 1.0)
    P1 = Vertex (line4[2], line4[3], 1.0, 1.0, 1.0)
    myEngine.rasterizeLine (P0.x, P0.y, P1.x, P1.y, 1.0, 1.0, 1.0)
    clippedLine = myEngine.clipLine (P0, P1, 250,50, 225, 50);
    if len(clippedLine) > 0:
        drawClippedLine (myEngine, clippedLine, 1.0, 0, 1.0)
        
  
    #  fifth line: outside on right and left
    P0 = Vertex (line5[0], line5[1], 1.0, 1.0, 1.0)
    P1 = Vertex (line5[2], line5[3], 1.0, 1.0, 1.0)
    myEngine.rasterizeLine (P0.x, P0.y, P1.x, P1.y, 1.0, 1.0, 1.0)
    clippedLine = myEngine.clipLine (P0, P1, 250,50, 225, 50);
    if len(clippedLine) > 0:
        drawClippedLine (myEngine, clippedLine, 0, 1.0, 1.0)
        
  
    #  sixth line: cut on all sides
    P0 = Vertex (line6[0], line6[1], 1.0, 1.0, 1.0)
    P1 = Vertex (line6[2], line6[3], 1.0, 1.0, 1.0)
    myEngine.rasterizeLine (P0.x, P0.y, P1.x, P1.y, 1.0, 1.0, 1.0)
    clippedLine = myEngine.clipLine (P0, P1, 250,50, 225, 50);
    if len(clippedLine) > 0: 
        drawClippedLine (myEngine, clippedLine, 1.0, 1.0, 0)
        

    
window = RitWindow(400, 400)
myEngine = CGIengine (window, default_action)

def main():
    window.run (myEngine)
    



if __name__ == "__main__":
    main()

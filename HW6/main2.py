from rit_window import *
from cgI_engine import *
from vertex import *
import numpy as np



# A simple routine to rasterize a set of triangles
def drawClippedPoly (vertices):
    nverts = len(vertices)
    if nverts < 3:
        return
        
    if (nverts % 3) != 0:
        print ("Bad number of verticies to define a set of triangles ", nverts, " Must be a multiple of 3")
        return
        
    # simply go through sets of 3 vertices and do raterization
    startidx = 0;
    while startidx < nverts:
        global_pixels_set = set()
        myEngine.rasterizeTriangle(vertices[startidx], vertices[startidx+1], vertices[startidx+2], global_pixels_set)

        startidx = startidx+ 3
        

def default_action ():
    myEngine.win.clearFB (0, 0, 0)
    
    # 1 -- all in -- no clipping
    myEngine.win.drawRect (775, 625, 175, 25, 1.0, 1.0, 1.0)
    P0 = Vertex (50, 650, 1.0, 0, 0)
    P1 = Vertex (100, 750, 1.0, 0, 0)
    P2 = Vertex (150, 650, 1.0, 0, 0)
    Poly = [P0, P1, P2]
    cP = myEngine.clipPoly (Poly, 775, 625, 175, 25)

    print("Clipped Polygon (cP):", cP)  # To check the structure of cP

    if len(cP) > 0:
        # Flatten the list
        cP = [v for sublist in cP for v in sublist]
        drawClippedPoly(cP)

    # 2 -- one out -- top - green
    myEngine.win.drawRect (775, 625, 350, 225, 1.0, 1.0, 1.0)
    P0 = Vertex (250, 650, 0, 1.0, 0)
    P1 = Vertex (300, 800, 0, 1.0, 0)
    P2 = Vertex (325, 650, 0, 1.0, 0)
    Poly = [P0, P1, P2]
    cP = myEngine.clipPoly (Poly, 775, 625, 350, 225)
    if len(cP) > 0:
        # Flatten the list
        cP = [v for sublist in cP for v in sublist]
        drawClippedPoly(cP)

    # 3 -- one out -- bottom -- blue
    myEngine.win.drawRect (775, 625, 550, 425, 1.0, 1.0, 1.0)
    P0 = Vertex (450, 700, 0, 0, 1.0)
    P1 = Vertex (500, 130, 0, 0, 1.0)
    P2 = Vertex (525, 700, 0, 0, 1.0)
    Poly = [P0, P2, P1]
    cP = myEngine.clipPoly (Poly, 775, 625, 550, 425)
    if len(cP) > 0:
        # Flatten the list
        cP = [v for sublist in cP for v in sublist]
        drawClippedPoly(cP)

    # 4 -- one out -- right -- cyan
    myEngine.win.drawRect (775, 625, 750, 625, 1.0, 1.0, 1.0)
    P0 = Vertex (650, 650, 0, 1.0, 1.0)
    P1 = Vertex (650, 725, 0, 1.0, 1.0)
    P2 = Vertex (900, 700, 0, 1.0, 1.0)
    Poly = [P0, P1, P2]
    cP = myEngine.clipPoly (Poly, 775, 625, 750, 625)
    if len(cP) > 0:
        # Flatten the list
        cP = [v for sublist in cP for v in sublist]
        drawClippedPoly(cP)

    # 5 -- one out -- left -- magenta
    myEngine.win.drawRect (575, 425, 150, 25, 1.0, 1.0, 1.0)
    P0 = Vertex (100, 550, 1.0, 0, 1.0)
    P1 = Vertex (100, 450, 1.0, 0, 1.0)
    P2 = Vertex (10, 500, 1.0, 0, 1.0)
    Poly = [P0, P1, P2]
    cP = myEngine.clipPoly (Poly, 575, 425, 150, 25)
    if len(cP) > 0:
        # Flatten the list
        cP = [v for sublist in cP for v in sublist]
        drawClippedPoly(cP)

    # 6 -- two out -- right/right -- yello
    myEngine.win.drawRect (575, 425, 350, 225, 1.0, 1.0, 1.0)
    P0 = Vertex (450, 550, 1.0, 1.0, 0)
    P1 = Vertex (550, 450, 1.0, 1.0, 0)
    P2 = Vertex (300, 500, 1.0, 1.0, 0)
    Poly = [P0, P1, P2]
    cP = myEngine.clipPoly (Poly, 575, 425, 350, 225)
    if len(cP) > 0:
        # Flatten the list
        cP = [v for sublist in cP for v in sublist]
        drawClippedPoly(cP)

    # 7 -- two out -- right/left-- light red
    myEngine.win.drawRect (575, 425, 550, 425, 1.0, 1.0, 1.0)
    P0 = Vertex (400, 550, 0.5, 0, 0)
    P1 = Vertex (600, 550, 0.5, 0, 0)
    P2 = Vertex (500, 500, 0.5, 0, 0)
    Poly = [P0, P1, P2]
    cP = myEngine.clipPoly (Poly, 575, 425, 550, 425)
    if len(cP) > 0:
        # Flatten the list
        cP = [v for sublist in cP for v in sublist]
        drawClippedPoly(cP)

    # 8 -- two out -- right/top-- light green
    myEngine.win.drawRect (575, 425, 750, 625, 1.0, 1.0, 1.0)
    P0 = Vertex (800, 550, 0, 0.5, 0)
    P1 = Vertex (675, 650, 0, 0.5, 0)
    P2 = Vertex (650, 590, 0, 0.5, 0)
    Poly = [P0, P2, P1]
    cP = myEngine.clipPoly (Poly, 575, 425, 750, 625)
    if len(cP) > 0:
        # Flatten the list
        cP = [v for sublist in cP for v in sublist]
        drawClippedPoly(cP)

    #  9 -two out -- right/bottom-- light blue
    myEngine.win.drawRect (375, 225, 175, 25, 1.0, 1.0, 1.0)
    P0 = Vertex (220, 350, 0, 0, 0.5)
    P1 = Vertex (150, 200, 0, 0, 0.5)
    P2 = Vertex (150, 300, 0, 0, 0.5)
    Poly = [P0, P1, P2]
    cP = myEngine.clipPoly (Poly, 375, 225, 175, 25)
    if len(cP) > 0:
        # Flatten the list
        cP = [v for sublist in cP for v in sublist]
        drawClippedPoly(cP)

    # 10 -- two out -- left / left -- light cyan
    myEngine.win.drawRect (375, 225, 375, 225, 1.0, 1.0, 1.0)
    P0 = Vertex (200, 300, 0, 0.5, 0.5)
    P1 = Vertex (190, 250, 0, 0.5, 0.5)
    P2 = Vertex (300, 300, 0, 0.5, 0.5)
    Poly = [P0, P2, P1]
    cP = myEngine.clipPoly (Poly, 375, 225, 375, 225)
    if len(cP) > 0:
        # Flatten the list
        cP = [v for sublist in cP for v in sublist]
        drawClippedPoly(cP)

    # 11 -- two out -- left / top -- light magenta
    myEngine.win.drawRect (375, 225, 575, 425, 1.0, 1.0, 1.0)
    P0 = Vertex (400, 300, 0.5, 0, 0.5)
    P1 = Vertex (450, 450, 0.5, 0, 0.5)
    P2 = Vertex (500, 300, 0.5, 0, 0.5)
    Poly = [P0, P1, P2]
    cP = myEngine.clipPoly (Poly, 375, 225, 575, 425)
    if len(cP) > 0:
        # Flatten the list
        cP = [v for sublist in cP for v in sublist]
        drawClippedPoly(cP)

    # 12 -- two out -- left / bottom -- light yellow
    myEngine.win.drawRect (375, 225, 775, 625, 1.0, 1.0, 1.0)
    P0 = Vertex (600, 300, 0.5, 0.5, 0)
    P1 = Vertex (550, 100, 0.5, 0.5, 0)
    P2 = Vertex (700, 300, 0.5, 0.5, 0)
    Poly = [P0, P2, P1]
    cP = myEngine.clipPoly (Poly, 375, 225, 775, 625)
    if len(cP) > 0:
        # Flatten the list
        cP = [v for sublist in cP for v in sublist]
        drawClippedPoly(cP)

    # 13 -- two out -- top / bottom -- lighter red
    myEngine.win.drawRect (175, 25, 175, 25, 1.0, 1.0, 1.0)
    P0 = Vertex (50, 200, 0.25, 0, 0)
    P1 = Vertex (150, 210, 0.25, 0, 0)
    P2 = Vertex (70, 100, 0.25, 0, 0)
    Poly = [P0, P1, P2]
    cP = myEngine.clipPoly (Poly, 175, 25, 175, 25)
    if len(cP) > 0:
        # Flatten the list
        cP = [v for sublist in cP for v in sublist]
        drawClippedPoly(cP)

    # 14 -- three out -- left / top / bottom -- lighter green
    myEngine.win.drawRect (175, 25, 375, 225, 1.0, 1.0, 1.0)
    P0 = Vertex (175, 150, 0, 0.25, 0)
    P1 = Vertex (250, 210, 0, 0.25,  0)
    P2 = Vertex (270, 10, 0, 0.25, 0)
    Poly = [P0, P1, P2]
    cP = myEngine.clipPoly (Poly, 175, 25, 375, 225)
    if len(cP) > 0:
        # Flatten the list
        cP = [v for sublist in cP for v in sublist]
        drawClippedPoly(cP)

    # 15 -- all out -- left / top / bottom -- lighter blue
    myEngine.win.drawRect (175, 25, 575, 425, 1.0, 1.0, 1.0)
    P0 = Vertex (425, 200, 0, 0, 0.25)
    P1 = Vertex (575, 200, 0, 0,  0.25)
    P2 = Vertex (450, 300, 0, 0, 0.25)
    Poly = [P0, P2, P1]
    cP = myEngine.clipPoly (Poly, 175, 25, 575, 425)
    if len(cP) > 0:
        # Flatten the list
        cP = [v for sublist in cP for v in sublist]
        drawClippedPoly(cP)

    # 16 -- all consuming  -- light grey
    myEngine.win.drawRect (175, 25, 775, 625, 1.0, 1.0, 1.0)
    P0 = Vertex (600, 0, 0.5, 0.5, 0.5)
    P1 = Vertex (700, 800, 0.5, 0.5, 0.5)
    P2 = Vertex (800, 0, 0.5, 0.5, 0.5)
    Poly = [P0, P1, P2]
    cP = myEngine.clipPoly (Poly, 175, 25, 775, 625)
    if len(cP) > 0:
        # Flatten the list
        cP = [v for sublist in cP for v in sublist]
        drawClippedPoly(cP)


window = RitWindow(800, 800)
myEngine = CGIengine (window, default_action)

def main():
    window.run (myEngine)
    



if __name__ == "__main__":
    main()

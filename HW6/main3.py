from rit_window import *
from cgI_engine import *
from vertex import *
import numpy as np
#from cgI_engine import clipPoly


# Triangles and colors definitions
tri1 = [50, 650, 100, 750, 150, 650]
tri2 = [250, 650, 300, 885, 325, 650]
tri3 = [450, 700, 500, 130, 525, 700]
tri4 = [650, 650, 650, 725, 900, 700]
tri5 = [100, 550, 100, 450, 10, 500]
tri6 = [450, 550, 550, 450, 300, 500]
tri7 = [400, 550, 600, 550, 500, 500]
tri8 = [800, 550, 675, 650, 650, 590]
tri9 = [220, 350, 150, 200, 150, 300]
tri10 = [200, 300, 190, 250, 300, 300]
tri11 = [400, 300, 450, 450, 500, 300]
tri12 = [600, 300, 550, 100, 700, 300]
tri13 = [50, 200, 150, 210, 70, 100]
tri14 = [175, 150, 250, 210, 270, 10]
tri15 = [425, 200, 575, 200, 450, 300]
tri16 = [600, 0, 700, 800, 800, 0]

color1 = [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0]
color2 = [0.5, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.5]
color3 = [1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0]
color4 = [0.5, 0.5, 0.0, 0.0, 0.5, 0.5, 0.5, 0.0, 0.5]

index_data = [0, 1, 2]
index_data2 = [0, 2, 1]


def default_action():
    myEngine.win.clearFB(0, 0, 0)

    modelTransform = myEngine.identity()
    global_pixels_set = set()

    # 1 -- all in -- no clipping
    normTransform = myEngine.normalize(775, 625, 175, 25)
    myEngine.defineViewWindow(775, 625, 175, 25)
    myEngine.win.drawRect(775, 625, 175, 25, 1.0, 1.0, 1.0)
    transformed_triangles = myEngine.drawTriangles(tri1, color1, index_data, modelTransform, normTransform,
                                                   global_pixels_set)
    # Clip each triangle from the transformed vertices
    for tri in transformed_triangles:
        v0, v1, v2 = tri
        clipped_triangles = myEngine.clipPoly([v0, v1, v2], top=775, bottom=625, right=175, left=25)
        # Rasterize
        for clipped_triangle in clipped_triangles:
            myEngine.rasterizeTriangle(clipped_triangle[0], clipped_triangle[1], clipped_triangle[2], global_pixels_set)

    # 2 -- one out -- top - green
    normTransform = myEngine.normalize(775, 625, 350, 225)
    myEngine.defineViewWindow(775, 625, 350, 225)
    myEngine.win.drawRect(775, 625, 350, 225, 1.0, 1.0, 1.0)
    transformed_triangles = myEngine.drawTriangles(tri2, color1, index_data, modelTransform, normTransform,
                                                   global_pixels_set)
    for tri in transformed_triangles:
        v0, v1, v2 = tri
        clipped_triangles = myEngine.clipPoly([v0, v1, v2], top=775, bottom=625, right=350, left=225)
        for clipped_triangle in clipped_triangles:
            myEngine.rasterizeTriangle(clipped_triangle[0], clipped_triangle[1], clipped_triangle[2], global_pixels_set)

    # 3 -- one out -- bottom -- blue
    normTransform = myEngine.normalize(775, 625, 550, 425)
    myEngine.defineViewWindow(775, 625, 550, 425)
    myEngine.win.drawRect(775, 625, 550, 425, 1.0, 1.0, 1.0)
    transformed_triangles = myEngine.drawTriangles(tri3, color1, index_data2, modelTransform, normTransform,
                                                   global_pixels_set)
    for tri in transformed_triangles:
        v0, v1, v2 = tri
        clipped_triangles = myEngine.clipPoly([v0, v1, v2], top=775, bottom=625, right=550, left=425)
        for clipped_triangle in clipped_triangles:
            myEngine.rasterizeTriangle(clipped_triangle[0], clipped_triangle[1], clipped_triangle[2], global_pixels_set)

    # 4 -- one out -- right -- cyan
    normTransform = myEngine.normalize(775, 625, 750, 625)
    myEngine.defineViewWindow(775, 625, 750, 625)
    myEngine.win.drawRect(775, 625, 750, 625, 1.0, 1.0, 1.0)
    transformed_triangles = myEngine.drawTriangles(tri4, color1, index_data, modelTransform, normTransform,
                                                   global_pixels_set)
    for tri in transformed_triangles:
        v0, v1, v2 = tri
        clipped_triangles = myEngine.clipPoly([v0, v1, v2], top=775, bottom=625, right=750, left=625)
        for clipped_triangle in clipped_triangles:
            myEngine.rasterizeTriangle(clipped_triangle[0], clipped_triangle[1], clipped_triangle[2], global_pixels_set)

    # 5 -- one out -- left -- magenta
    normTransform = myEngine.normalize(575, 425, 150, 25)
    myEngine.defineViewWindow(575, 425, 150, 25)
    myEngine.win.drawRect(575, 425, 150, 25, 1.0, 1.0, 1.0)
    transformed_triangles = myEngine.drawTriangles(tri5, color1, index_data, modelTransform, normTransform,
                                                   global_pixels_set)
    for tri in transformed_triangles:
        v0, v1, v2 = tri
        clipped_triangles = myEngine.clipPoly([v0, v1, v2], top=575, bottom=425, right=150, left=25)
        for clipped_triangle in clipped_triangles:
            myEngine.rasterizeTriangle(clipped_triangle[0], clipped_triangle[1], clipped_triangle[2], global_pixels_set)

    # 6 -- two out -- right/right -- yellow
    normTransform = myEngine.normalize(575, 425, 350, 225)
    myEngine.defineViewWindow(575, 425, 350, 225)
    myEngine.win.drawRect(575, 425, 350, 225, 1.0, 1.0, 1.0)
    transformed_triangles = myEngine.drawTriangles(tri6, color1, index_data, modelTransform, normTransform,
                                                   global_pixels_set)
    for tri in transformed_triangles:
        v0, v1, v2 = tri
        clipped_triangles = myEngine.clipPoly([v0, v1, v2], top=575, bottom=425, right=350, left=225)
        for clipped_triangle in clipped_triangles:
            myEngine.rasterizeTriangle(clipped_triangle[0], clipped_triangle[1], clipped_triangle[2], global_pixels_set)

    # 7 -- two out -- right/left -- light red
    normTransform = myEngine.normalize(575, 425, 550, 425)
    myEngine.defineViewWindow(575, 425, 550, 425)
    myEngine.win.drawRect(575, 425, 550, 425, 1.0, 1.0, 1.0)
    transformed_triangles = myEngine.drawTriangles(tri7, color2, index_data, modelTransform, normTransform,
                                                   global_pixels_set)
    for tri in transformed_triangles:
        v0, v1, v2 = tri
        clipped_triangles = myEngine.clipPoly([v0, v1, v2], top=575, bottom=425, right=550, left=425)
        for clipped_triangle in clipped_triangles:
            myEngine.rasterizeTriangle(clipped_triangle[0], clipped_triangle[1], clipped_triangle[2], global_pixels_set)

    # 8 -- two out -- right/top -- light green
    normTransform = myEngine.normalize(575, 425, 750, 625)
    myEngine.defineViewWindow(575, 425, 750, 625)
    myEngine.win.drawRect(575, 425, 750, 625, 1.0, 1.0, 1.0)
    transformed_triangles = myEngine.drawTriangles(tri8, color3, index_data2, modelTransform, normTransform,
                                                   global_pixels_set)
    for tri in transformed_triangles:
        v0, v1, v2 = tri
        clipped_triangles = myEngine.clipPoly([v0, v1, v2], top=575, bottom=425, right=750, left=625)
        for clipped_triangle in clipped_triangles:
            myEngine.rasterizeTriangle(clipped_triangle[0], clipped_triangle[1], clipped_triangle[2], global_pixels_set)


    # 9 -- two out -- right/bottom --
    normTransform = myEngine.normalize(375, 225, 175, 25)
    myEngine.defineViewWindow(375, 225, 175, 25)
    myEngine.win.drawRect(375, 225, 175, 25, 1.0, 1.0, 1.0)
    transformed_triangles = myEngine.drawTriangles(tri9, color2, index_data, modelTransform, normTransform,
                                                   global_pixels_set)
    for tri in transformed_triangles:
        v0, v1, v2 = tri
        clipped_triangles = myEngine.clipPoly([v0, v1, v2], top=375, bottom=225, right=175, left=25)
        for clipped_triangle in clipped_triangles:
            myEngine.rasterizeTriangle(clipped_triangle[0], clipped_triangle[1], clipped_triangle[2], global_pixels_set)

    # 10 -- two out -- left/left
    normTransform = myEngine.normalize(375, 225, 375, 225)
    myEngine.defineViewWindow(375, 225, 375, 225)
    myEngine.win.drawRect(375, 225, 375, 225, 1.0, 1.0, 1.0)
    transformed_triangles = myEngine.drawTriangles(tri10, color2, index_data2, modelTransform, normTransform,
                                                   global_pixels_set)
    for tri in transformed_triangles:
        v0, v1, v2 = tri
        clipped_triangles = myEngine.clipPoly([v0, v1, v2], top=375, bottom=225, right=375, left=225)
        for clipped_triangle in clipped_triangles:
            myEngine.rasterizeTriangle(clipped_triangle[0], clipped_triangle[1], clipped_triangle[2], global_pixels_set)

    # 11 -- two out -- left / top
    normTransform = myEngine.normalize(375, 225, 575, 425)
    myEngine.defineViewWindow(375, 225, 575, 425)
    myEngine.win.drawRect(375, 225, 575, 425, 1.0, 1.0, 1.0)
    transformed_triangles = myEngine.drawTriangles(tri11, color2, index_data, modelTransform, normTransform,
                                                   global_pixels_set)
    for tri in transformed_triangles:
        v0, v1, v2 = tri
        clipped_triangles = myEngine.clipPoly([v0, v1, v2], top=375, bottom=225, right=575, left=425)
        for clipped_triangle in clipped_triangles:
            myEngine.rasterizeTriangle(clipped_triangle[0], clipped_triangle[1], clipped_triangle[2], global_pixels_set)

    # 12 -- two out -- left / bottom -- light yellow
    normTransform = myEngine.normalize(375, 225, 775, 625)
    myEngine.defineViewWindow(375, 225, 775, 625)
    myEngine.win.drawRect(375, 225, 775, 625, 1.0, 1.0, 1.0)
    transformed_triangles = myEngine.drawTriangles(tri12, color2, index_data2, modelTransform, normTransform,
                                                   global_pixels_set)
    for tri in transformed_triangles:
        v0, v1, v2 = tri
        clipped_triangles = myEngine.clipPoly([v0, v1, v2], top=375, bottom=225, right=775, left=625)
        for clipped_triangle in clipped_triangles:
            myEngine.rasterizeTriangle(clipped_triangle[0], clipped_triangle[1], clipped_triangle[2], global_pixels_set)

    # 13 -- two out -- top / bottom
    normTransform = myEngine.normalize(175, 25, 175, 25)
    myEngine.defineViewWindow(175, 25, 175, 25)
    myEngine.win.drawRect(175, 25, 175, 25, 1.0, 1.0, 1.0)
    transformed_triangles = myEngine.drawTriangles(tri13, color2, index_data, modelTransform, normTransform,
                                                   global_pixels_set)
    for tri in transformed_triangles:
        v0, v1, v2 = tri
        clipped_triangles = myEngine.clipPoly([v0, v1, v2], top=175, bottom=25, right=175, left=25)
        for clipped_triangle in clipped_triangles:
            myEngine.rasterizeTriangle(clipped_triangle[0], clipped_triangle[1], clipped_triangle[2], global_pixels_set)

    # 14 -- three out -- left / top / bottom
    normTransform = myEngine.normalize(175, 25, 375, 225)
    myEngine.defineViewWindow(175, 25, 375, 225)
    myEngine.win.drawRect(175, 25, 375, 225, 1.0, 1.0, 1.0)
    transformed_triangles = myEngine.drawTriangles(tri14, color2, index_data, modelTransform, normTransform,
                                                   global_pixels_set)
    for tri in transformed_triangles:
        v0, v1, v2 = tri
        clipped_triangles = myEngine.clipPoly([v0, v1, v2], top=175, bottom=25, right=375, left=225)
        for clipped_triangle in clipped_triangles:
            myEngine.rasterizeTriangle(clipped_triangle[0], clipped_triangle[1], clipped_triangle[2], global_pixels_set)

    # 15 -- all out -- left / top / bottom
    normTransform = myEngine.normalize(175, 25, 575, 425)
    myEngine.defineViewWindow(175, 25, 575, 425)
    myEngine.win.drawRect(175, 25, 575, 425, 1.0, 1.0, 1.0)
    transformed_triangles = myEngine.drawTriangles(tri15, color2, index_data, modelTransform, normTransform,
                                                   global_pixels_set)
    for tri in transformed_triangles:
        v0, v1, v2 = tri
        clipped_triangles = myEngine.clipPoly([v0, v1, v2], top=175, bottom=25, right=575, left=425)
        for clipped_triangle in clipped_triangles:
            myEngine.rasterizeTriangle(clipped_triangle[0], clipped_triangle[1], clipped_triangle[2], global_pixels_set)

    # 16 -- all consuming -- light grey
    normTransform = myEngine.normalize(175, 25, 775, 625)
    myEngine.defineViewWindow(175, 25, 775, 625)
    myEngine.win.drawRect(175, 25, 775, 625, 1.0, 1.0, 1.0)
    transformed_triangles = myEngine.drawTriangles(tri16, color4, index_data, modelTransform, normTransform,
                                                   global_pixels_set)
    for tri in transformed_triangles:
        v0, v1, v2 = tri
        clipped_triangles = myEngine.clipPoly([v0, v1, v2], top=175, bottom=25, right=775, left=625)
        for clipped_triangle in clipped_triangles:
            myEngine.rasterizeTriangle(clipped_triangle[0], clipped_triangle[1], clipped_triangle[2], global_pixels_set)


window = RitWindow(800, 800)
myEngine = CGIengine(window, default_action)


def main():
    window.run(myEngine)


if __name__ == "__main__":
    main()
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


def MidpointCircle(radius, x0, y0):
    # actual midpoint circle algorithm
    d = 1 - radius
    x = 0
    y = radius
    Circlepoints(x, y, x0, y0)
    while x < y:
        if d < 0:
            d = d + 2 * x + 3
            x = x + 1
        else:
            d = d + 2 * x - 2 * y + 5
            x = x + 1
            y = y - 1
        Circlepoints(x, y, x0, y0)

    
def Circlepoints(x, y, x0, y0):
    # 8-way symmetry around (x0, y0)
    draw_points(x0 + x, y0 + y)
    draw_points(x0 + y, y0 + x)
    draw_points(x0 - y, y0 + x)
    draw_points(x0 - x, y0 + y)
    draw_points(x0 - x, y0 - y)
    draw_points(x0 - y, y0 - x)
    draw_points(x0 + y, y0 - x)
    draw_points(x0 + x, y0 - y)



def draw_points(x, y):
    # Draw a single point at (x, y)
    glPointSize(3) #pixel size. by default 1 thake
    glBegin(GL_POINTS)
    glVertex2f(x,y) #jekhane show korbe pixel
    glEnd()


def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    
    glOrtho(90, 410, 290, 660, 0.0, 1.0) #2D orthographic viewing region. parameter gula holo (left, right, bottom, top, near, far)
    # padding = extra space around the circle
    # r = radius
    # left   = x0 - r - padding
    # right  = x0 + r + padding
    # bottom = y0 - r - padding
    # top    = y0 + r + padding 
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()


def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    glColor3f(1.0, 1.0, 0.0) #konokichur color set (RGB)

    #call the draw methods here
    x = 250
    y = 500
    radius = 150
    MidpointCircle(radius, x, y)
   
    glutSwapBuffers()


glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(700, 700) #window size
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"Midpoint Circle") #window name
glutDisplayFunc(showScreen)
glutMainLoop()

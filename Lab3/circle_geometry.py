from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


def MidpointCircle(radius, x0, y0):
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

    draw_points(x + x0, y + y0)
    draw_points(y + y0, x + x0)
    draw_points(y + y0, -x + x0)
    draw_points(x + x0, -y + y0)
    draw_points(-x + x0, -y + y0)
    draw_points(-y + y0, -x + x0)
    draw_points(-y + y0, x + x0)
    draw_points(-x + x0, y + y0)


def draw_points(x, y):
    glPointSize(3) #pixel size. by default 1 thake
    glBegin(GL_POINTS)
    glVertex2f(x,y) #jekhane show korbe pixel
    glEnd()


def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()


def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    glColor3f(1.0, 1.0, 0.0) #konokichur color set (RGB)
    #call the draw methods here
    x1 = 250 
    y1 = 250
    radius1 = 150
    MidpointCircle(radius1, x1, y1)

    x2 = 250 + 75
    y2 = 250
    radius2 = 75
    MidpointCircle(radius2, x2, y2)

    x3 = 250
    y3 = 250 + 75
    radius3 = 75
    MidpointCircle(radius3, x3, y3)

    x4 = 250 - 75
    y4 = 250
    radius4 = 75
    MidpointCircle(radius4, x4, y4)

    x5 = 250
    y5 = 250 - 75
    radius5 = 75
    MidpointCircle(radius5, x5, y5)

    x6 = 250 + 52.5
    y6 = 250 + 52.5
    radius6 = 75
    MidpointCircle(radius6, x6, y6)

    x7 = 250 - 52.5
    y7 = 250 + 52.5
    radius7 = 75
    MidpointCircle(radius7, x7, y7)

    x8 = 250 - 52.5
    y8 = 250 - 52.5
    radius8 = 75
    MidpointCircle(radius8, x8, y8)

    x9 = 250 + 52.5
    y9 = 250 - 52.5
    radius9 = 75
    MidpointCircle(radius9, x9, y9)

   
    glutSwapBuffers()


glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(700, 700) #window size
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"OpenGL Coding Practice") #window name
glutDisplayFunc(showScreen)
glutMainLoop()

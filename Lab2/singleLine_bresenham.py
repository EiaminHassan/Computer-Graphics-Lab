from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Window size
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600


# Will hold generated points from DDA
POINTS = []

# Bresenham function for line generation 
def Bresenham(X1,Y1,X2,Y2): 
    # calculate dx & dy 
    dx = X2 - X1 
    dy = Y2 - Y1 

    # initial value of decision parameter d 
    d = dy - (dx/2) 
    x = X1
    y = Y1 

    # Plot initial given point 
    # putpixel(x,y) can be used to print pixel 
    # of line in graphics 
    POINTS.append((x, y))
    # iterate through value of X 
    while (x < X2):
        x=x+1
        # E or East is chosen
        if(d < 0):
            d = d + dy 

        # NE or North East is chosen 
        else:
            d = d + (dy - dx) 
            y=y+1
    

        # Plot intermediate points 
        # putpixel(x,y) is used to print pixel 
        # of line in graphics 
        POINTS.append((x, y))
    return POINTS

def display():
    glClear(GL_COLOR_BUFFER_BIT)

    # ----- Draw Bresenham points -----
    glColor3f(1.0, 1.0, 0.0)
    glPointSize(2.0)
    glBegin(GL_POINTS)
    for (xi, yi) in POINTS:
        glVertex2i(xi, yi)

    POINTS.clear()
    glEnd()
    glutSwapBuffers()
    


def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, width, 0, height)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def init_glut_window():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Single Line Drawing using Bresenham Algorithm")
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glClearColor(0.0, 0.0, 0.0, 1.0)


def main():
    global POINTS

    POINTS = Bresenham(100, 100, 220, 230)
    print("Generated Bresenham points:")
    print(POINTS)

    # Start GLUT
    init_glut_window()
    glutMainLoop()


if __name__ == "__main__":
    main()

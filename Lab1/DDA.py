from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Window size
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

X0, Y0 = 100, 100
X1, Y1 = 220, 230

# Will hold generated points from DDA
POINTS = []


def DDA(x0, y0, x1, y1):
    points = []

    dx = x1 - x0
    dy = y1 - y0
    steps = int(max(abs(dx), abs(dy)))

    if steps == 0:
        # Single point (degenerate line)
        points.append((int(round(x0)), int(round(y0))))
        return points

    x_inc = dx / float(steps)
    y_inc = dy / float(steps)

    x = float(x0)
    y = float(y0)

    for _ in range(steps + 1):
        points.append((int(round(x)), int(round(y))))
        x += x_inc
        y += y_inc

    return points

def display():
    glClear(GL_COLOR_BUFFER_BIT)

    # ----- Draw DDA points -----
    glColor3f(1.0, 1.0, 0.0)
    glPointSize(2.0)
    glBegin(GL_POINTS)
    for (xi, yi) in POINTS:
        glVertex2i(xi, yi)
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
    glutCreateWindow(b"DDA Algorithm")
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glClearColor(0.0, 0.0, 0.0, 1.0)


def main():
    global POINTS

    POINTS = DDA(X0, Y0, X1, Y1)
    print("Generated DDA points:")
    print(POINTS)

    # Start GLUT
    init_glut_window()
    glutMainLoop()


if __name__ == "__main__":
    main()

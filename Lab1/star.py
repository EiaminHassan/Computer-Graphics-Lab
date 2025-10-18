from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Window size
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Manually defined 10 points of a star (x, y)
points = [
    (400, 500),  # top
    (430, 420),
    (510, 420),
    (450, 370),
    (470, 300),
    (400, 340),
    (330, 300),
    (350, 370),
    (290, 420),
    (370, 420),
]

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1.0, 1.0, 0.0)   # yellow star
    glLineWidth(2.0)

    # Draw star outline by connecting points in star order
    glBegin(GL_LINE_LOOP)
    for (x, y) in points:
        glVertex2f(x, y)
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
    glutCreateWindow(b"Star Draw")
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glClearColor(0.0, 0.0, 0.0, 1.0)

def main():
    init_glut_window()
    glutMainLoop()

if __name__ == "__main__":
    main()

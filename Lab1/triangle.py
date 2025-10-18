from OpenGL.GL import *             # Core OpenGL functions (glBegin, glVertex, glClear, etc.)
from OpenGL.GLU import *            # Utility library (gluOrtho2D)
from OpenGL.GLUT import *           # GLUT functions (window creation, main loop)
import math


# Window size constants (used for the orthographic projection and viewport)
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600


# Line endpoints for demonstration (you can change these or make them interactive)
# Coordinates are given in window pixel coordinates (0..WINDOW_WIDTH-1, 0..WINDOW_HEIGHT-1)
X0, Y0 = 100, 100
X1, Y1 = 200, 100
X2, Y2 = 150, 150




def display():
   
    # Clear the screen (color buffer). GL_COLOR_BUFFER_BIT refers to the color buffer of the window.
    glClear(GL_COLOR_BUFFER_BIT)

  
    glColor3f(2.0, 3.0, 0.0)


    glLineWidth(3.0)

    # Draw a triangle
    glPointSize(4.0)

    glBegin(GL_LINES)

    glVertex2f(X0, Y0)
    glVertex2f(X1, Y1)

    glVertex2f(X0, Y0)
    glVertex2f(X2, Y2)

    glVertex2f(X1, Y1)
    glVertex2f(X2, Y2)
    
    glEnd()


    glutSwapBuffers()




def reshape(width, height):


    # Set viewport to cover the whole window (0,0) to (width,height)
    glViewport(0, 0, width, height)


    # Select projection matrix and reset it
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluOrtho2D(0, width, 0, height)


    # Return to modelview matrix
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()








def init_glut_window():
 


    # Initialize GLUT runtime; pass no arguments (empty list)
    glutInit()


    # Use double buffering and RGBA color mode
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)


    # Initial window size
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)


    # Initial window position (x, y)
    glutInitWindowPosition(400, 100)


    # Create and show window with title (this call creates an OpenGL context)
    glutCreateWindow(b"Triangle - PyOpenGL + GLUT")


    # Register GLUT callback functions
    glutDisplayFunc(display)   # display callback: called when the window must be redrawn
    glutReshapeFunc(reshape)   # reshape callback: called when window is resized
   
    glClearColor(0.0, 0.0, 0.0, 1.0)  # black background




def main():

    init_glut_window()
    glutMainLoop()




if __name__ == "__main__":
    main()
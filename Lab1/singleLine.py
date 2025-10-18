from OpenGL.GL import *             # Core OpenGL functions (glBegin, glVertex, glClear, etc.)
from OpenGL.GLU import *            # Utility library (gluOrtho2D)
from OpenGL.GLUT import *           # GLUT functions (window creation, main loop)
import math


# Window size constants (used for the orthographic projection and viewport)
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600


# Line endpoints for demonstration (you can change these or make them interactive)
# Coordinates are given in window pixel coordinates (0..WINDOW_WIDTH-1, 0..WINDOW_HEIGHT-1)
X0, Y0 = 0, 0
X1, Y1 = 200, 520




def display():
   
    # Clear the screen (color buffer). GL_COLOR_BUFFER_BIT refers to the color buffer of the window.
    glClear(GL_COLOR_BUFFER_BIT)

    # Set current drawing color (r, g, b). Values in [0,1].
    # glColor3f sets the current primitive color for subsequent geometry.
    # Optionally draw the endpoints as larger green points for clarity
    # glPointSize(4.0)    
    # glColor3f(1.0, 0.0, 0.0)  # red color for line points

    glLineWidth(4.0)
    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_LINES)
    glVertex2f(int(X0), int(Y0))
    glVertex2f(int(X1), int(Y1))
    glEnd()

    # Flush commands and swap buffers:
    # - glFlush() ensures all issued GL commands will be executed in finite time.
    # - glutSwapBuffers() swaps front and back buffers (if double-buffered).
    # We use glutSwapBuffers because display mode below requests GLUT_DOUBLE.
    glutSwapBuffers()




def reshape(width, height):


    # Set viewport to cover the whole window (0,0) to (width,height)
    glViewport(0, 0, width, height)


    # Select projection matrix and reset it
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()


    # Create orthographic projection that matches window pixel coordinates.
    # gluOrtho2D(left, right, bottom, top)
    # We set bottom=0 and top=WINDOW_HEIGHT so the origin (0,0) is at lower-left.
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
    glutCreateWindow(b"Single Line - PyOpenGL + GLUT")


    # Register GLUT callback functions
    glutDisplayFunc(display)   # display callback: called when the window must be redrawn
    glutReshapeFunc(reshape)   # reshape callback: called when window is resized
   
    # Some GLUT implementations require an initial call to reshape or set up projection,
    # but our reshape will be called automatically on initial window creation.
    # Set clear color: glClearColor(r,g,b,a) sets the background color for glClear
    glClearColor(0.0, 0.0, 0.0, 1.0)  # black background




def main():
    """
    Program entry point.


    - Initialize GLUT and window (init_glut_window)
    - Enter GLUT main loop (glutMainLoop) which dispatches events and invokes callbacks.
      Note: glutMainLoop never returns under classic GLUT; some GLUT implementations provide
      glutMainLoopEvent / glutLeaveMainLoop to break out. For simple demos, glutMainLoop is fine.
    """
    init_glut_window()


    # Enter GLUT's main loop. This hands control to GLUT which will call the callbacks we registered.
    # GLUT's main loop handles events (keyboard, mouse, reshape) and rendering.
    glutMainLoop()




if __name__ == "__main__":
    main()
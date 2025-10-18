from OpenGL.GL import *             # Core OpenGL functions (glBegin, glVertex, glClear, etc.)
from OpenGL.GLU import *            # Utility library (gluOrtho2D)
from OpenGL.GLUT import *           # GLUT functions (window creation, main loop)
import math


# Window size constants (used for the orthographic projection and viewport)
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600


# Line endpoints for demonstration (you can change these or make them interactive)
# Coordinates are given in window pixel coordinates (0..WINDOW_WIDTH-1, 0..WINDOW_HEIGHT-1)
def find_zone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    if abs(dx) >= abs(dy):
        if dx >= 0 and dy >= 0:
            return 0
        elif dx < 0 and dy >= 0:
            return 3
        elif dx < 0 and dy < 0:
            return 4
        else:
            return 7
    else:
        if dx >= 0 and dy >= 0:
            return 1
        elif dx < 0 and dy >= 0:
            return 2
        elif dx < 0 and dy < 0:
            return 5
        else:
            return 6


def to_zone0(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return y, -x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return -y, x
    elif zone == 7:
        return x, -y


def from_zone0(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    elif zone == 7:
        return x, -y

def midPoint(x1, y1, x2, y2):
    zone = find_zone(x1, y1, x2, y2)
    nx1, ny1 = to_zone0(x1, y1, zone)
    nx2, ny2 = to_zone0(x2, y2, zone)

    dx = nx2 - nx1
    dy = ny2 - ny1

    d = 2 * dy - dx
    E = 2 * dy
    NE = 2 * (dy - dx)

    x, y = nx1, ny1
    points = [(x, y)]

    while x < nx2:
        if d < 0:
            d += E
            x += 1
        else:
            d += NE
            x += 1
            y += 1
        points.append((x, y))

    
    final_points = []
    for px, py in points:
        final_points.append(from_zone0(px, py, zone))
    return final_points



def reshape(width, height):
    glViewport(0, 0, width, height)  # Set viewport to cover the new window size

    glMatrixMode(GL_PROJECTION)      # Switch to projection matrix
    glLoadIdentity()                 # Reset projection matrix
    # Set up an orthographic projection with origin at bottom-left corner
    gluOrtho2D(0, WINDOW_WIDTH - 1, 0, WINDOW_HEIGHT - 1)

    glMatrixMode(GL_MODELVIEW)       # Switch back to modelview matrix
    glLoadIdentity()                 # Reset modelview matrix



def display():
    glClear(GL_COLOR_BUFFER_BIT)

    # Set color and point size
    glPointSize(4.0)
    glColor3f(1.0, 0.0, 0.0)  # red lines

    # --- Define vertices and edges ---
    vertices = {
        'A': (2, 2), 'B': (5, 2), 'C': (5, 5), 'D': (2, 5),
        'E': (1, 3), 'F': (4, 3), 'G': (4, 6), 'H': (1, 6)
    }

    edges = [
        ('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'A'),
        ('E', 'F'), ('F', 'G'), ('G', 'H'), ('H', 'E'),
        ('A', 'E'), ('B', 'F'), ('C', 'G'), ('D', 'H')
    ]

    # Scale up coordinates for better visibility
    scale = 50

    # --- Draw cube edges using DDA or midpoint line ---
    glBegin(GL_POINTS)
    for edge in edges:
        x0, y0 = vertices[edge[0]]
        x1, y1 = vertices[edge[1]]

        # Scale coordinates
        x0, y0 = x0 * scale, y0 * scale
        x1, y1 = x1 * scale, y1 * scale

        # Draw line points using your midPoint function
        points = midPoint(int(x0), int(y0), int(x1), int(y1))
        for p in points:
            glVertex2i(int(p[0]), int(p[1]))
    glEnd()

    # --- Draw vertex points in green ---
    glPointSize(6.0)
    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_POINTS)
    for v in vertices.values():
        glVertex2i(int(v[0] * scale), int(v[1] * scale))
    glEnd()

    glutSwapBuffers()


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
    glutCreateWindow(b"Cube with Midpoint Line Algorithm")


    # Register GLUT callback functions
    glutDisplayFunc(display)   # display callback: called when the window must be redrawn
    glutReshapeFunc(reshape)   # reshape callback: called when window is resized

    glClearColor(0.0, 0.0, 0.0, 1.0)  # black background




def main():
   
    init_glut_window()
    glutMainLoop()

if __name__ == "__main__":
    main()
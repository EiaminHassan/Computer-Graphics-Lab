from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Window size constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Heart shape coordinates (centered around 400, 300)
# The heart is made of two circles at the top and two diagonal lines meeting at bottom point

# Left circle (top-left of heart)
LEFT_CIRCLE_X = 310
LEFT_CIRCLE_Y = 430
CIRCLE_RADIUS = 90

# Right circle (top-right of heart)
RIGHT_CIRCLE_X = 490
RIGHT_CIRCLE_Y = 430

# Bottom point of heart
HEART_BOTTOM_X = 400
HEART_BOTTOM_Y = 150

# Left diagonal line endpoints
LEFT_LINE_START_X = 220  # leftmost point of left circle
LEFT_LINE_START_Y = 430

# Right diagonal line endpoints
RIGHT_LINE_START_X = 580  # rightmost point of right circle
RIGHT_LINE_START_Y = 430

# Inner smaller circles for decoration (optional)
INNER_LEFT_CIRCLE_X = 350
INNER_LEFT_CIRCLE_Y = 430
INNER_CIRCLE_RADIUS = 50

INNER_RIGHT_CIRCLE_X = 450
INNER_RIGHT_CIRCLE_Y = 430

# Center vertical line
CENTER_LINE_TOP_X = 400
CENTER_LINE_TOP_Y = 430
CENTER_LINE_BOTTOM_X = 400
CENTER_LINE_BOTTOM_Y = 150


def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1.0, 1.0, 1.0)  # White color
    glPointSize(2.0)
    
    glBegin(GL_POINTS)
    
    # Draw left upper half circle (top-left of heart)
    points = MidpointCircle(CIRCLE_RADIUS, LEFT_CIRCLE_X, LEFT_CIRCLE_Y)
    for point in points:
        # Only draw upper half (y >= center_y)
        if point[1] >= LEFT_CIRCLE_Y:
            glVertex2f(point[0], point[1])
    
    # Draw right upper half circle (top-right of heart)
    points = MidpointCircle(CIRCLE_RADIUS, RIGHT_CIRCLE_X, RIGHT_CIRCLE_Y)
    for point in points:
        # Only draw upper half (y >= center_y)
        if point[1] >= RIGHT_CIRCLE_Y:
            glVertex2f(point[0], point[1])
    
    # Draw left diagonal line (from left circle to bottom point)
    points = midPoint(LEFT_LINE_START_X, LEFT_LINE_START_Y, HEART_BOTTOM_X, HEART_BOTTOM_Y)
    for point in points:
        glVertex2f(point[0], point[1])
    
    # Draw right diagonal line (from right circle to bottom point)
    points = midPoint(RIGHT_LINE_START_X, RIGHT_LINE_START_Y, HEART_BOTTOM_X, HEART_BOTTOM_Y)
    for point in points:
        glVertex2f(point[0], point[1])
    
    # Draw center vertical line
    points = midPoint(CENTER_LINE_TOP_X, CENTER_LINE_TOP_Y, CENTER_LINE_BOTTOM_X, CENTER_LINE_BOTTOM_Y)
    for point in points:
        glVertex2f(point[0], point[1])
    
    # Draw inner left upper half circle (smaller, for decoration)
    points = MidpointCircle(INNER_CIRCLE_RADIUS, INNER_LEFT_CIRCLE_X, INNER_LEFT_CIRCLE_Y)
    for point in points:
        # Only draw upper half (y >= center_y)
        if point[1] >= INNER_LEFT_CIRCLE_Y:
            glVertex2f(point[0], point[1])
    
    # Draw inner right upper half circle (smaller, for decoration)
    points = MidpointCircle(INNER_CIRCLE_RADIUS, INNER_RIGHT_CIRCLE_X, INNER_RIGHT_CIRCLE_Y)
    for point in points:
        # Only draw upper half (y >= center_y)
        if point[1] >= INNER_RIGHT_CIRCLE_Y:
            glVertex2f(point[0], point[1])
    
    # Draw inner left diagonal line (from inner left circle to bottom point)
    INNER_LEFT_LINE_START_X = INNER_LEFT_CIRCLE_X - INNER_CIRCLE_RADIUS
    INNER_LEFT_LINE_START_Y = INNER_LEFT_CIRCLE_Y
    points = midPoint(INNER_LEFT_LINE_START_X, INNER_LEFT_LINE_START_Y, HEART_BOTTOM_X, HEART_BOTTOM_Y)
    for point in points:
        glVertex2f(point[0], point[1])
    
    # Draw inner right diagonal line (from inner right circle to bottom point)
    INNER_RIGHT_LINE_START_X = INNER_RIGHT_CIRCLE_X + INNER_CIRCLE_RADIUS
    INNER_RIGHT_LINE_START_Y = INNER_RIGHT_CIRCLE_Y
    points = midPoint(INNER_RIGHT_LINE_START_X, INNER_RIGHT_LINE_START_Y, HEART_BOTTOM_X, HEART_BOTTOM_Y)
    for point in points:
        glVertex2f(point[0], point[1])
    
    glEnd()
    glutSwapBuffers()


# =================== Midpoint Circle Algorithm ===================
def MidpointCircle(radius, x0, y0):
    """
    Midpoint Circle Algorithm
    Draws a circle using 8-way symmetry
    """
    x = 0
    y = radius
    d = 1 - radius
    points = []
    
    points.extend(Circlepoints(x, y, x0, y0))
    
    while x <= y:
        if d < 0:
            d = d + 2 * x + 3
            x = x + 1
        else:
            d = d + (2 * x) - (2 * y) + 5
            x = x + 1
            y = y - 1
        
        points.extend(Circlepoints(x, y, x0, y0))
    
    return points


def Circlepoints(x, y, x0, y0):
    """
    Generate 8 symmetric points for circle
    """
    return [
        (x + x0, y + y0),
        (y + x0, x + y0),
        (y + x0, -x + y0),
        (x + x0, -y + y0),
        (-x + x0, -y + y0),
        (-y + x0, -x + y0),
        (-y + x0, x + y0),
        (-x + x0, y + y0)
    ]


# =================== Midpoint Line Drawing Algorithm ===================

def get_zone(x0, y0, x1, y1):
    """
    Determine which of the 8 zones (octants) the line (x0,y0)->(x1,y1) lies in.
    This lets us convert any line into zone 0 (dx>=dy>=0), run the simple
    midpoint algorithm there, then transform points back.
    """
    dx = x1 - x0
    dy = y1 - y0

    if abs(dx) >= abs(dy):          # shallow: |slope| <= 1
        if dx >= 0 and dy >= 0:
            return 0
        elif dx < 0 and dy >= 0:
            return 3
        elif dx < 0 and dy < 0:
            return 4
        else:  # dx >= 0 and dy < 0
            return 7
    else:                           # steep: |slope| > 1
        if dx >= 0 and dy >= 0:
            return 1
        elif dx < 0 and dy >= 0:
            return 2
        elif dx < 0 and dy < 0:
            return 5
        else:  # dx >= 0 and dy < 0
            return 6


def convert_to_zone_0(x, y, zone):
    """
    Convert coordinates from any zone to zone 0 (dx>=dy>=0)
    using reflections and swaps.
    """
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


def convert_from_zone_0(x, y, zone):
    """
    Inverse of convert_to_zone_0:
    map a zone-0 point back to the original zone.
    """
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


def midPoint(X1, Y1, X2, Y2):
    """
    Midpoint Line Drawing Algorithm (integer-only version)
    using zone conversion for all 8 octants.

    Returns a list of (x, y) points that approximate the line segment
    from (X1, Y1) to (X2, Y2).
    """
    zone = get_zone(X1, Y1, X2, Y2)

    # Convert endpoints into zone 0
    nx1, ny1 = convert_to_zone_0(X1, Y1, zone)
    nx2, ny2 = convert_to_zone_0(X2, Y2, zone)

    dx = nx2 - nx1
    dy = ny2 - ny1

    # Decision variable and its increments (classic midpoint form)
    d  = 2 * dy - dx
    E  = 2 * dy
    NE = 2 * (dy - dx)

    x, y = nx1, ny1
    points_zone0 = [(x, y)]

    # Basic loop in zone 0: x always increases
    while x < nx2:
        if d < 0:
            d += E
            x += 1
        else:
            d += NE
            x += 1
            y += 1
        points_zone0.append((x, y))

    # Transform all computed points back to original zone
    final_points = []
    for px, py in points_zone0:
        fx, fy = convert_from_zone_0(px, py, zone)
        final_points.append((fx, fy))

    return final_points


# =================== OpenGL Setup ===================
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
    glutInitWindowPosition(400, 100)
    glutCreateWindow(b"Heart Shape - Midpoint Algorithm")
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Black background


def main():
    """
    Program entry point.
    Initialize GLUT and window, then enter main loop.
    """
    init_glut_window()
    glutMainLoop()


if __name__ == "__main__":
    main()

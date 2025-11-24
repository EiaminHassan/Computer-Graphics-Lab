from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Window size constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Car body coordinates (main rounded rectangle with curves)
# Bottom horizontal line
CAR_BOTTOM_LEFT_X = 120
CAR_BOTTOM_LEFT_Y = 280
CAR_BOTTOM_RIGHT_X = 520
CAR_BOTTOM_RIGHT_Y = 280

# Top horizontal line
CAR_TOP_LEFT_X = 120
CAR_TOP_LEFT_Y = 350
CAR_TOP_RIGHT_X = 520
CAR_TOP_RIGHT_Y = 350

# Front bumper (curved - small circle on right side)
FRONT_BUMPER_X = 520
FRONT_BUMPER_Y = 315
FRONT_BUMPER_RADIUS = 35

# Rear bumper (curved - small circle on left side)
REAR_BUMPER_X = 120
REAR_BUMPER_Y = 315
REAR_BUMPER_RADIUS = 35

# Car roof (semicircle on top behind wheels)
ROOF_CENTER_X = 240
ROOF_CENTER_Y = 350
ROOF_RADIUS = 70

# Roof vertical divider line
ROOF_DIVIDER_X = 240
ROOF_DIVIDER_TOP_Y = 420
ROOF_DIVIDER_BOTTOM_Y = 350

# Second upper roof (semicircle above first roof)
UPPER_ROOF_CENTER_X = 240
UPPER_ROOF_CENTER_Y = 350
UPPER_ROOF_RADIUS = 90

# Left wheel (rear)
LEFT_WHEEL_X = 200
LEFT_WHEEL_Y = 280
WHEEL_OUTER_RADIUS = 45
WHEEL_INNER_RADIUS = 25

# Right wheel (front)
RIGHT_WHEEL_X = 440
RIGHT_WHEEL_Y = 280

# Window circles on body
REAR_WINDOW_X = 280
REAR_WINDOW_Y = 315
REAR_WINDOW_RADIUS = 13

FRONT_WINDOW_X = 540
FRONT_WINDOW_Y = 323
FRONT_WINDOW_RADIUS = 15


def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1.0, 1.0, 1.0)  # White color
    glPointSize(2.0)
    
    glBegin(GL_POINTS)
    
    # Draw car body with rounded ends
    # Bottom horizontal line in three segments (avoiding wheels)
    # Left segment: from rear bumper to left wheel
    LEFT_WHEEL_LEFT_EDGE = LEFT_WHEEL_X - WHEEL_OUTER_RADIUS
    points = midPoint(CAR_BOTTOM_LEFT_X, CAR_BOTTOM_LEFT_Y, LEFT_WHEEL_LEFT_EDGE, CAR_BOTTOM_LEFT_Y)
    for point in points:
        glVertex2f(point[0], point[1])
    
    # Middle segment: between wheels
    LEFT_WHEEL_RIGHT_EDGE = LEFT_WHEEL_X + WHEEL_OUTER_RADIUS
    RIGHT_WHEEL_LEFT_EDGE = RIGHT_WHEEL_X - WHEEL_OUTER_RADIUS
    points = midPoint(LEFT_WHEEL_RIGHT_EDGE, CAR_BOTTOM_LEFT_Y, RIGHT_WHEEL_LEFT_EDGE, CAR_BOTTOM_LEFT_Y)
    for point in points:
        glVertex2f(point[0], point[1])
    
    # Right segment: from right wheel to front bumper
    RIGHT_WHEEL_RIGHT_EDGE = RIGHT_WHEEL_X + WHEEL_OUTER_RADIUS
    points = midPoint(RIGHT_WHEEL_RIGHT_EDGE, CAR_BOTTOM_LEFT_Y, CAR_BOTTOM_RIGHT_X, CAR_BOTTOM_RIGHT_Y)
    for point in points:
        glVertex2f(point[0], point[1])
    
    # Top horizontal line
    points = midPoint(CAR_TOP_LEFT_X, CAR_TOP_LEFT_Y, CAR_TOP_RIGHT_X, CAR_TOP_RIGHT_Y)
    for point in points:
        glVertex2f(point[0], point[1])
    
    # Draw front bumper (right semicircle)
    points = MidpointCircle(FRONT_BUMPER_RADIUS, FRONT_BUMPER_X, FRONT_BUMPER_Y)
    for point in points:
        # Only draw right half (x >= center_x)
        if point[0] >= FRONT_BUMPER_X:
            glVertex2f(point[0], point[1])
    
    # Draw rear bumper (left semicircle)
    points = MidpointCircle(REAR_BUMPER_RADIUS, REAR_BUMPER_X, REAR_BUMPER_Y)
    for point in points:
        # Only draw left half (x <= center_x)
        if point[0] <= REAR_BUMPER_X:
            glVertex2f(point[0], point[1])
    
    # Draw roof (upper half circle)
    points = MidpointCircle(ROOF_RADIUS, ROOF_CENTER_X, ROOF_CENTER_Y)
    for point in points:
        # Only draw upper half (y >= center_y)
        if point[1] >= ROOF_CENTER_Y:
            glVertex2f(point[0], point[1])
    
    # Draw second upper roof (upper half circle above first roof)
    points = MidpointCircle(UPPER_ROOF_RADIUS, UPPER_ROOF_CENTER_X, UPPER_ROOF_CENTER_Y)
    for point in points:
        # Only draw upper half (y >= center_y)
        if point[1] >= UPPER_ROOF_CENTER_Y:
            glVertex2f(point[0], point[1])
    
    # Draw vertical line divider on roof
    points = midPoint(ROOF_DIVIDER_X, ROOF_DIVIDER_TOP_Y, ROOF_DIVIDER_X, ROOF_DIVIDER_BOTTOM_Y)
    for point in points:
        glVertex2f(point[0], point[1])
    
    # Draw left wheel outer circle
    points = MidpointCircle(WHEEL_OUTER_RADIUS, LEFT_WHEEL_X, LEFT_WHEEL_Y)
    for point in points:
        glVertex2f(point[0], point[1])
    
    # Draw left wheel inner circle
    points = MidpointCircle(WHEEL_INNER_RADIUS, LEFT_WHEEL_X, LEFT_WHEEL_Y)
    for point in points:
        glVertex2f(point[0], point[1])
    
    # Draw right wheel outer circle
    points = MidpointCircle(WHEEL_OUTER_RADIUS, RIGHT_WHEEL_X, RIGHT_WHEEL_Y)
    for point in points:
        glVertex2f(point[0], point[1])
    
    # Draw right wheel inner circle
    points = MidpointCircle(WHEEL_INNER_RADIUS, RIGHT_WHEEL_X, RIGHT_WHEEL_Y)
    for point in points:
        glVertex2f(point[0], point[1])
    
    # Draw rear window circle
    points = MidpointCircle(REAR_WINDOW_RADIUS, REAR_WINDOW_X, REAR_WINDOW_Y)
    for point in points:
        glVertex2f(point[0], point[1])
    
    # Draw front window circle
    points = MidpointCircle(FRONT_WINDOW_RADIUS, FRONT_WINDOW_X, FRONT_WINDOW_Y)
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
    glutCreateWindow(b"Car Shape - Midpoint Algorithm")
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

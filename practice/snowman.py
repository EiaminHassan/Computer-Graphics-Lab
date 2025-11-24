from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Window size constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# =================== Snowman geometry (global) ===================

# Common X for all circles (vertical stack)
SNOWMAN_X = 400

# Radii for bottom, middle, and head circles
BOTTOM_R = 130
MIDDLE_R = 90
HEAD_R   = 60

# Center Y positions so circles are tangent (just touching)
BOTTOM_CY = 140
MIDDLE_CY = BOTTOM_CY + BOTTOM_R + MIDDLE_R   # 140 + 130 + 90 = 360
HEAD_CY   = MIDDLE_CY + MIDDLE_R + HEAD_R     # 360 + 90 + 60  = 510

BOTTOM_CX = SNOWMAN_X
MIDDLE_CX = SNOWMAN_X
HEAD_CX   = SNOWMAN_X

# Eyes (on the head)
EYE_R        = 8
EYE_OFFSET_X = 18   # left/right from head center
EYE_OFFSET_Y = 10   # upward from head center

LEFT_EYE_CX  = HEAD_CX - EYE_OFFSET_X
RIGHT_EYE_CX = HEAD_CX + EYE_OFFSET_X
EYE_CY       = HEAD_CY + EYE_OFFSET_Y

# Mouth (a short horizontal line on the head)
MOUTH_OFFSET_Y   = 20  # downward from head center
MOUTH_HALF_WIDTH = 25  # half-length of the line

MOUTH_Y  = HEAD_CY - MOUTH_OFFSET_Y
MOUTH_X1 = HEAD_CX - MOUTH_HALF_WIDTH
MOUTH_X2 = HEAD_CX + MOUTH_HALF_WIDTH

# Buttons on the middle circle
BUTTON_R        = 8
BUTTON_OFFSET_Y = 22   # up/down from the middle-circle center

TOP_BUTTON_CX,  TOP_BUTTON_CY    = MIDDLE_CX, MIDDLE_CY + BUTTON_OFFSET_Y
BOTTOM_BUTTON_CX, BOTTOM_BUTTON_CY = MIDDLE_CX, MIDDLE_CY - BUTTON_OFFSET_Y


def display():
    """
    Draw a vertical snowman:

      - 3 circles:
          * head (full circle)
          * middle: only lower part (above tangent with head is hidden)
          * bottom: only lower part (above tangent with middle is hidden)
      - eyes on the head
      - curved mouth (lower semicircle) on the head
      - diagonal nose line
      - two buttons on the middle circle
    """
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1.0, 1.0, 1.0)  # white
    glPointSize(2.0)

    glBegin(GL_POINTS)

    # --------- helper clip Y levels (tangent points) ----------
    # tangent between head & middle: at top of middle circle
    MID_CLIP_Y    = MIDDLE_CY + MIDDLE_R
    # tangent between middle & bottom: at top of bottom circle
    BOTTOM_CLIP_Y = BOTTOM_CY + BOTTOM_R

    # ---------------- bottom circle (3rd big) -----------------
    # draw only the part below its tangent with the middle circle
    bottom_points = MidpointCircle(BOTTOM_R, BOTTOM_CX, BOTTOM_CY)
    for x, y in bottom_points:
        if y <= BOTTOM_CLIP_Y:
            glVertex2f(x, y)

    # ---------------- middle circle (2nd big) -----------------
    # draw only the part below its tangent with the head circle
    middle_points = MidpointCircle(MIDDLE_R, MIDDLE_CX, MIDDLE_CY)
    for x, y in middle_points:
        if y <= MID_CLIP_Y:
            glVertex2f(x, y)

    # ---------------- head circle (full) ----------------------
    head_points = MidpointCircle(HEAD_R, HEAD_CX, HEAD_CY)
    for x, y in head_points:
        glVertex2f(x, y)

    # ---------------- eyes (small circles) --------------------
    left_eye_pts = MidpointCircle(EYE_R, LEFT_EYE_CX, EYE_CY)
    for x, y in left_eye_pts:
        glVertex2f(x, y)

    right_eye_pts = MidpointCircle(EYE_R, RIGHT_EYE_CX, EYE_CY)
    for x, y in right_eye_pts:
        glVertex2f(x, y)

    # ---------------- curved mouth (smile) --------------------
    # model mouth as lower semicircle centered on (HEAD_CX, MOUTH_Y)
    mouth_r = MOUTH_HALF_WIDTH
    mouth_pts = MidpointCircle(mouth_r, HEAD_CX, MOUTH_Y)
    for x, y in mouth_pts:
        if y <= MOUTH_Y:   # keep only lower half
            glVertex2f(x, y)

    # ---------------- nose (diagonal line) --------------------
    NOSE_START_X = HEAD_CX
    NOSE_START_Y = HEAD_CY
    NOSE_END_X   = HEAD_CX + 25
    NOSE_END_Y   = HEAD_CY - 10

    nose_points = midPoint(NOSE_START_X, NOSE_START_Y, NOSE_END_X, NOSE_END_Y)
    for x, y in nose_points:
        glVertex2f(x, y)

    # ---------------- buttons on middle circle ----------------
    top_btn_pts = MidpointCircle(BUTTON_R, TOP_BUTTON_CX, TOP_BUTTON_CY)
    for x, y in top_btn_pts:
        glVertex2f(x, y)

    bottom_btn_pts = MidpointCircle(BUTTON_R, BOTTOM_BUTTON_CX, BOTTOM_BUTTON_CY)
    for x, y in bottom_btn_pts:
        glVertex2f(x, y)

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
    glutCreateWindow(b"Mickey Mouse Face - Midpoint Algorithm")
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

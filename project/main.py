import sys
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import clock  # pendulum clock module


# Global animation variables
# a, b: control the sun’s position (it moves diagonally).
a = 0.0
b = 0.0

# m, n: control cloud movement.
m = 0.0
n = 0.0

# x: control the buses moving across the scene.
x = 0.0

y = 0.0

# o: controls one animated person’s horizontal movement.
o = 0.0

def myInit():
    """
    Initialize the main scene's projection and clear color.

    Sets a reddish background for the sky and configures an orthographic
    projection spanning 0..500 in both X and Y with a small Z range.
    """
    glClearColor(128.0/255.0, 0, 0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, 500, 0, 500, -10.0, 10.0)

def circlecar(x, y, rad, r, g, b):
    """
    Draw a filled circle using a triangle fan (utility for clouds/small shapes).

    Parameters:
    - x, y: Center position.
    - rad: Radius of the circle.
    - r, g, b: Color components (0..255) used for the circle fill.
    """
    x1 = x
    y1 = y
    glBegin(GL_TRIANGLE_FAN)
    glColor3ub(int(r), int(g), int(b))
    glVertex2f(x1, y1)
    angle = 0
    while angle <= 360:
        x2 = x1 + math.sin(math.radians(angle)) * rad
        y2 = y1 + math.cos(math.radians(angle)) * rad
        glVertex2f(x2, y2)
        angle += 0.5
    glEnd()

def circleWheel(x1, y1, rx, ry):
    """
    Draw a filled ellipse-like wheel using a triangle fan.

    Parameters:
    - x1, y1: Center position.
    - rx, ry: Radii along X and Y axes respectively.
    """
    glBegin(GL_TRIANGLE_FAN)
    glColor3ub(255, 255, 255)
    glVertex2f(x1, y1)
    for angle in range(361):
        glColor3ub(1, 1, 1)
        x2 = x1 + rx * math.sin(math.radians(angle))
        y2 = y1 + ry * math.cos(math.radians(angle))
        glVertex2f(x2, y2)
    glEnd()

def circleD(x1, y1, rx, ry):
    """
    Draw a filled ellipse (decorative element) using a triangle fan.

    Parameters:
    - x1, y1: Center position.
    - rx, ry: Radii along X and Y axes respectively.
    """
    glBegin(GL_TRIANGLE_FAN)
    glColor3ub(255, 41, 41)
    glVertex2f(x1, y1)
    for angle in range(361):
        glColor3ub(255, 41, 41)
        x2 = x1 + rx * math.sin(math.radians(angle))
        y2 = y1 + ry * math.cos(math.radians(angle))
        glVertex2f(x2, y2)
    glEnd()

def sun(x1, y1, rx, ry):
    """
    Draw the sun as a filled ellipse with warm colors.

    Parameters:
    - x1, y1: Center position.
    - rx, ry: Radii along X and Y axes respectively.
    """
    glBegin(GL_TRIANGLE_FAN)
    glColor3ub(255, 10, 0)
    glVertex2f(x1, y1)
    for angle in range(361):
        glColor3ub(240, 215, 0)
        x2 = x1 + rx * math.sin(math.radians(angle))
        y2 = y1 + ry * math.cos(math.radians(angle))
        glVertex2f(x2, y2)
    glEnd()

def circle(h, k, rx, ry, r, g, b):
    """
    Draw a filled ellipse using polygon approximation.

    Parameters:
    - h, k: Center coordinates.
    - rx, ry: Radii along X and Y axes respectively.
    - r, g, b: Color components (0..255) for the fill.
    """
    glColor3f(r / 255.0, g / 255.0, b / 255.0)
    glBegin(GL_POLYGON)
    for i in range(1, 361):
        glVertex2f(h + rx * math.cos(math.radians(i)), k + ry * math.sin(math.radians(i)))
    glEnd()
    glFlush()

def display():
    """
    Main scene display callback.

    Draws a stylized city/field scene with buildings, roads, mosque,
    clouds, sun, trees, buses, animated figures, and places the
    pendulum clock on a specific building facade.
    """
    global a, b, m, n, x, o
    
    # Clear the color buffer to prepare for new frame rendering
    glClear(GL_COLOR_BUFFER_BIT)
    
    # ========== SKY ==========
    # Draw gradient sky background with white at horizon transitioning to blue at top
    # Creates a realistic sky appearance from Y=250 to Y=500
    glBegin(GL_QUADS)
    glColor3ub(255, 255, 255)  # White color at bottom (horizon)
    glVertex2f(500, 250)
    glVertex2f(0, 250)
    glColor3ub(101, 193, 246)  # Sky blue at top
    glVertex2f(0, 500)
    glVertex2f(500, 500)
    glEnd()

    # ========== BACKGROUND ELEMENTS ==========
    # Left green background area - represents distant greenery/landscape
    # Located at far left from X=0 to X=100, Y=100 to Y=220
    glColor3ub(51, 255, 51)  # Bright green
    glBegin(GL_QUADS)
    glVertex2d(100, 220)
    glVertex2d(100, 100)
    glVertex2d(0, 100)
    glVertex2d(0, 220)
    glEnd()

    # ========== ROADS ==========
    # Front road segment 4 (Ab4Front Road) - diagonal road on left side
    # Creates perspective by connecting Y=50-100 to Y=230
    glColor3ub(251, 255, 203)  # Light yellowish road color
    glBegin(GL_POLYGON)
    glVertex2d(0, 50)
    glVertex2d(0, 100)
    glVertex2d(75, 230)
    glVertex2d(100, 230)
    glEnd()

    # Main horizontal road (Ab1Front Road) - runs across entire scene
    # Positioned at Y=220 to Y=250, spanning full width (X=0 to X=500)
    glColor3ub(251, 255, 203)  # Light yellowish road color
    glBegin(GL_POLYGON)
    glVertex2d(0, 220)
    glVertex2d(0, 250)
    glVertex2d(500, 250)
    glVertex2d(500, 220)
    glEnd()

    # ========== MOSQUE STRUCTURE ==========
    # Main mosque body - trapezoidal shape creating perspective
    # Base at Y=250 (road level), extending up to Y=360
    glColor3ub(191, 191, 191)  # Light gray for main structure
    glBegin(GL_POLYGON)
    glVertex2d(360, 250)
    glVertex2d(440, 250)
    glVertex2d(470, 360)
    glVertex2d(330, 360)
    glEnd()

    # Mosque decorative upper band (black/dark accent)
    # Horizontal strip near top for architectural detail
    glColor3ub(1, 1, 1)  # Near-black
    glBegin(GL_POLYGON)
    glVertex2d(370, 337)
    glVertex2d(430, 337)
    glVertex2d(430, 346)
    glVertex2d(370, 346)
    glEnd()

    # Mosque front wall section 1 (dark maroon/brown)
    # Creates depth by overlaying darker front panel
    glColor3ub(88, 9, 9)  # Dark reddish-brown
    glBegin(GL_POLYGON)
    glVertex2d(370, 325)
    glVertex2d(430, 325)
    glVertex2d(430, 250)
    glVertex2d(370, 250)
    glEnd()

    # Mosque front wall section 2 (lighter gray)
    # Central panel with entrance area
    glColor3ub(191, 191, 191)  # Light gray
    glBegin(GL_POLYGON)
    glVertex2d(383, 250)
    glVertex2d(417, 250)
    glVertex2d(417, 310)
    glVertex2d(383, 310)
    glEnd()

    # Mosque entrance door (rectangular blue section)
    # Main entrance doorway in blue color
    glColor3ub(0, 150, 250)  # Blue door
    glBegin(GL_POLYGON)
    glVertex2d(388, 250)
    glVertex2d(412, 250)
    glVertex2d(412, 290)
    glVertex2d(388, 290)
    glEnd()

    # Mosque entrance arch (triangular top of door)
    # Creates traditional Islamic arch shape above door
    glColor3ub(0, 150, 250)  # Blue to match door
    glBegin(GL_POLYGON)
    glVertex2d(412, 290)
    glVertex2d(388, 290)
    glVertex2d(400, 298)  # Apex of triangle
    glEnd()

    # Mosque upper decorative bar (dark accent layer)
    # First layer of horizontal band at top
    glColor3ub(1, 1, 1)  # Near-black
    glBegin(GL_POLYGON)
    glVertex2d(323, 359)
    glVertex2d(477, 359)
    glVertex2d(477, 373)
    glVertex2d(323, 373)
    glEnd()

    # Mosque upper decorative bar (light gray layer)
    # Second layer slightly offset for 3D effect
    glColor3ub(191, 191, 191)  # Light gray
    glBegin(GL_POLYGON)
    glVertex2d(324, 360)
    glVertex2d(476, 360)
    glVertex2d(476, 372)
    glVertex2d(324, 372)
    glEnd()

    # ========== ANIMATED ELEMENTS: SUN & CLOUDS ==========
    # Animated sun - moves diagonally using variables 'a' and 'b'
    # Base position (200, 300) with animation offset, radius 30
    sun(a + 200, b + 300, 30, 30)

    # Cloud group 1 (left side) - 4 overlapping circles create fluffy cloud
    # All use variable 'm' for horizontal animation (moves right to left or vice versa)
    circlecar(m + 100, n + 425, 10, 255, 255, 255)  # Bottom-left circle
    circlecar(m + 110, n + 430, 10, 255, 255, 255)  # Bottom-right circle
    circlecar(m + 90, n + 430, 10, 255, 255, 255)   # Top-left circle
    circlecar(m + 100, n + 440, 10, 255, 255, 255)  # Top-center circle

    # Cloud group 2 (center) - another set of 4 circles
    circlecar(m + 180, n + 445, 10, 255, 255, 255)  # Bottom-left circle
    circlecar(m + 190, n + 450, 10, 255, 255, 255)  # Bottom-right circle
    circlecar(m + 170, n + 450, 10, 255, 255, 255)  # Top-left circle
    circlecar(m + 180, n + 460, 10, 255, 255, 255)  # Top-center circle

    # Cloud group 3 (right side) - third set of 4 circles
    circlecar(m + 260, n + 445, 10, 255, 255, 255)  # Bottom-left circle
    circlecar(m + 270, n + 450, 10, 255, 255, 255)  # Bottom-right circle
    circlecar(m + 250, n + 450, 10, 255, 255, 255)  # Top-left circle
    circlecar(m + 260, n + 460, 10, 255, 255, 255)  # Top-center circle

    # Sun animation update - increments position until limit reached
    # Moves sun diagonally upward and rightward (150 units max)
    if a < 150:
        a += 0.5  # Horizontal movement speed
        b += 0.5  # Vertical movement speed

    # ========== BUILDING COMPLEX (AB1) ==========
    # AB1 Part 1 - Leftmost building section
    # 6-story tall building from X=20 to X=90, Y=250 to Y=400
    # Forms the left anchor of the building complex
    glColor3ub(233, 233, 233)  # Light gray building color
    glBegin(GL_POLYGON)
    glVertex2d(20, 250)
    glVertex2d(90, 250)
    glVertex2d(90, 400)
    glVertex2d(20, 400)
    glEnd()

    # Windows for AB1 Part 1 - 12 windows arranged in 6 floors (2 per floor)
    # Each floor has left and right windows with dark red/maroon color
    windows_part1 = [
        (25, 395, 45, 375), (60, 395, 85, 375),  # 6th Floor
        (25, 370, 45, 350), (60, 370, 85, 350),  # 5th Floor
        (25, 345, 45, 325), (60, 345, 85, 325),  # 4th Floor
        (25, 320, 45, 300), (60, 320, 85, 300),  # 3rd Floor
        (25, 295, 45, 275), (60, 295, 85, 275),  # 2nd Floor
        (25, 270, 45, 250), (60, 270, 85, 250)   # 1st Floor
    ]
    
    glColor3ub(188, 56, 56)
    for x1, y1, x2, y2 in windows_part1:
        glBegin(GL_POLYGON)
        glVertex2d(x1, y1)
        glVertex2d(x1, y2)
        glVertex2d(x2, y2)
        glVertex2d(x2, y1)
        glEnd()

    # AB1 Part 2 - Second building section with slanted top
    # Slightly shorter than Part 1, creating varied skyline
    # From X=90 to X=140, Y=250 to Y=390-400 (slanted top edge)
    glColor3ub(233, 233, 233)  # Light gray building color
    glBegin(GL_POLYGON)
    glVertex2d(90, 250)
    glVertex2d(140, 250)
    glVertex2d(140, 390)
    glVertex2d(90, 400)
    glEnd()

    # 6th Floor horizontal separator line
    glColor3ub(1, 1, 1)
    glBegin(GL_LINES)
    glVertex2d(90, 375)
    glVertex2d(140, 368)
    glEnd()

    # AB1 Part2 6thFloor Windows
    glColor3ub(127, 16, 16)
    glBegin(GL_POLYGON)
    glVertex2d(95, 395)
    glVertex2d(95, 380)
    glVertex2d(110, 377)
    glVertex2d(110, 391)
    glEnd()

    glColor3ub(127, 16, 16)
    glBegin(GL_POLYGON)
    glVertex2d(120, 390)
    glVertex2d(120, 377)
    glVertex2d(135, 374)
    glVertex2d(135, 386)
    glEnd()

    # 5th Floor Lines
    glColor3ub(127, 16, 16)
    glBegin(GL_LINES)
    glVertex2d(90, 350)
    glVertex2d(140, 343)
    glEnd()

    # AB1 Part2 5thFloor Windows
    glColor3ub(127, 16, 16)
    glBegin(GL_POLYGON)
    glVertex2d(95, 370)
    glVertex2d(95, 355)
    glVertex2d(110, 352)
    glVertex2d(110, 366)
    glEnd()

    glColor3ub(127, 16, 16)
    glBegin(GL_POLYGON)
    glVertex2d(120, 365)
    glVertex2d(120, 350)
    glVertex2d(135, 347)
    glVertex2d(135, 361)
    glEnd()

    # AB1 Part2 Another Building - Darker reddish-brown overlay
    # This section serves as the facade for the grandfather clock
    # Irregular pentagonal shape from X=90 to X=137, Y=250 to Y=335-345
    glColor3ub(180, 56, 56)  # Reddish-brown color
    glBegin(GL_POLYGON)
    glVertex2d(90, 250)
    glVertex2d(90, 345)
    glVertex2d(125, 340)
    glVertex2d(137, 335)
    glVertex2d(137, 250)
    glEnd()
    
    # ========== GRANDFATHER CLOCK PLACEMENT ==========
    # Place animated pendulum clock on the building facade
    # Building span: X=90 to X=137 (width 47), Y=250 to Y=345 (height 95)
    # Clock centered at X=113.5, base at Y=250, scaled to 49.0 units
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    # Slightly reduced scale to decrease height a bit while fitting width
    clock.draw_grandfather_clock(world_x=113.5, world_y=250.0, scale=49.0)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)


    # AB1 Part 3 - Wide central building section
    # Largest section of the building complex
    # From X=140 to X=226 (width 86), Y=250 to Y=390
    glColor3ub(233, 233, 233)  # Light gray building color
    glBegin(GL_POLYGON)
    glVertex2d(140, 250)
    glVertex2d(226, 250)
    glVertex2d(226, 390)
    glVertex2d(140, 390)
    glEnd()

    # Windows for AB1 Part 3 - 10 windows in 5 floors (2 per floor)
    # Floors: 6th, 5th, 4th, 3rd, 2nd (no 1st floor windows)
    windows_part3 = [
        (145, 385, 180, 370), (187, 385, 222, 370),  # 6th Floor
        (145, 363, 180, 348), (187, 363, 222, 348),  # 5th Floor
        (145, 338, 180, 323), (187, 338, 222, 323),  # 4th Floor
        (145, 312, 180, 297), (187, 312, 222, 297),  # 3rd Floor
        (145, 286, 180, 271), (187, 286, 222, 271)   # 2nd Floor
    ]
    
    glColor3ub(188, 56, 56)
    for x1, y1, x2, y2 in windows_part3:
        glBegin(GL_POLYGON)
        glVertex2d(x1, y1)
        glVertex2d(x1, y2)
        glVertex2d(x2, y2)
        glVertex2d(x2, y1)
        glEnd()

    # AB1 Part 4 - Medium height section
    # Shorter than Part 3, continuing the stepped skyline effect
    # From X=226 to X=253 (width 27), Y=250 to Y=367
    glColor3ub(233, 233, 233)  # Light gray building color
    glBegin(GL_POLYGON)
    glVertex2d(226, 250)
    glVertex2d(226, 367)
    glVertex2d(253, 367)
    glVertex2d(253, 250)
    glEnd()

    # Windows for AB1 Part 4 - 4 windows on floors 5, 4, 3, 2
    windows_part4 = [
        (229, 363, 249, 348),  # 5th Floor
        (229, 338, 249, 323),  # 4th Floor
        (229, 312, 249, 297),  # 3rd Floor
        (229, 286, 249, 271)   # 2nd Floor
    ]
    
    glColor3ub(188, 56, 56)
    for x1, y1, x2, y2 in windows_part4:
        glBegin(GL_POLYGON)
        glVertex2d(x1, y1)
        glVertex2d(x1, y2)
        glVertex2d(x2, y2)
        glVertex2d(x2, y1)
        glEnd()

    # AB1 Part 5 - Another stepped-down section
    # Even shorter, from X=253 to X=280 (width 27), Y=250 to Y=343
    glColor3ub(233, 233, 233)  # Light gray building color
    glBegin(GL_POLYGON)
    glVertex2d(253, 250)
    glVertex2d(253, 343)
    glVertex2d(280, 343)
    glVertex2d(280, 250)
    glEnd()

    # Windows for AB1 Part 5 - 3 windows on floors 4, 3, 2
    windows_part5 = [
        (256, 338, 276, 323),  # 4th Floor
        (256, 312, 276, 297),  # 3rd Floor
        (256, 286, 276, 271)   # 2nd Floor
    ]
    
    glColor3ub(188, 56, 56)
    for x1, y1, x2, y2 in windows_part5:
        glBegin(GL_POLYGON)
        glVertex2d(x1, y1)
        glVertex2d(x1, y2)
        glVertex2d(x2, y2)
        glVertex2d(x2, y1)
        glEnd()

    # AB1 Part 6 - Shortest building section (rightmost)
    # Completes the building complex with lowest height
    # From X=276 to X=308 (width 32), Y=250 to Y=316
    glColor3ub(233, 233, 233)  # Light gray building color
    glBegin(GL_POLYGON)
    glVertex2d(276, 250)
    glVertex2d(276, 316)
    glVertex2d(308, 316)
    glVertex2d(308, 250)
    glEnd()

    # Windows for AB1 Part 6 - Only 2 windows on floors 3 and 2
    glColor3ub(188, 56, 56)
    glBegin(GL_POLYGON)
    glVertex2d(283, 312)
    glVertex2d(283, 297)
    glVertex2d(303, 297)
    glVertex2d(303, 312)
    glEnd()

    glColor3ub(188, 56, 56)
    glBegin(GL_POLYGON)
    glVertex2d(283, 286)
    glVertex2d(283, 271)
    glVertex2d(303, 271)
    glVertex2d(303, 286)
    glEnd()

    # ========== FIELD (GROUND/GRASS AREA) ==========
    # Large green field spanning bottom of scene
    # Irregular pentagon from Y=0 to Y=220, covering most of bottom area
    # Represents a sports field or park area
    glColor3ub(60, 185, 72)  # Grass green color
    glBegin(GL_POLYGON)
    glVertex2d(0, 50)
    glVertex2d(0, 0)
    glVertex2d(500, 0)
    glVertex2d(500, 220)
    glVertex2d(93, 220)
    glEnd()

    # Field markings - white lines creating sports field layout
    # Includes boundary lines, goal areas, and center markings
    glColor3ub(255, 255, 255)
    glBegin(GL_LINES)
    glVertex2d(296, 205)
    glVertex2d(230, 0)
    
    glVertex2d(108, 205)
    glVertex2d(8, 0)
    
    glVertex2d(485, 205)
    glVertex2d(108, 205)
    
    glVertex2d(470, 0)
    glVertex2d(485, 205)
    
    glVertex2d(49, 110)
    glVertex2d(53, 92)
    
    glVertex2d(70, 154)
    glVertex2d(75, 139)
    
    glVertex2d(70, 154)
    glVertex2d(49, 110)
    
    glVertex2d(476, 80)
    glVertex2d(483, 97)
    
    glVertex2d(486, 130)
    glVertex2d(483, 97)
    
    glVertex2d(486, 130)
    glVertex2d(477, 110)
    glEnd()

    # ========== TREES ==========
    # Array of 13 trees positioned along the field
    # Each tree consists of trunk (brown rectangle) and leaves (green triangles)
    # Creates a tree-lined horizon effect
    tree_positions = [122, 152, 182, 212, 242, 272, 302, 332, 362, 392, 422, 452, 482]
    for tree_x in tree_positions:
        # Tree trunk - small vertical brown rectangle (width 2, height 7)
        glColor3ub(153, 0, 0)
        glBegin(GL_POLYGON)
        glVertex2d(tree_x, 210)
        glVertex2d(tree_x, 217)
        glVertex2d(tree_x + 2, 217)
        glVertex2d(tree_x + 2, 210)
        glEnd()
        
        # Tree Lower Leaf
        glColor3ub(0, 102, 0)
        glBegin(GL_POLYGON)
        glVertex2d(tree_x - 5, 216)
        glVertex2d(tree_x + 1, 225)
        glVertex2d(tree_x + 7, 216)
        glEnd()
        
        # Tree Upper Leaf
        glBegin(GL_POLYGON)
        glVertex2d(tree_x - 5, 220)
        glVertex2d(tree_x + 1, 229)
        glVertex2d(tree_x + 7, 220)
        glEnd()


    # ========== CLOUD ANIMATION LOGIC ==========
    # Clouds move from left to right across the sky
    # When m reaches 250, reset to -50 to wrap around (loop animation)
    # Speed: 0.3 units per frame
    if m < 250:
        m += 0.3  # Move clouds rightward
    else:
        m = -50   # Wrap back to left side

    # Alternative: For right-to-left movement, uncomment below:
    # if m > -100:
    #     m -= 0.3  # Move clouds leftward
    # else:
    #     m = 250   # Wrap back to right side

    # ========== ANIMATED PERSON 1 (Walking Figure) ==========
    # Stick figure that moves horizontally using variable 'o'
    # Consists of: 2 arms (lines), body/legs (polygons), head (circle)
    
    # Left arm - diagonal line from shoulder to hand
    glColor3ub(255, 160, 122)  # Peach/skin color
    glLineWidth(4.0)
    glBegin(GL_LINES)
    glVertex2d(o + 264, 260)  # Shoulder
    glVertex2d(o + 256, 257)  # Hand
    glEnd()

    # Right arm - diagonal line from shoulder to hand
    glColor3ub(255, 160, 122)  # Peach/skin color
    glLineWidth(4.0)
    glBegin(GL_LINES)
    glVertex2d(o + 266, 260)  # Shoulder
    glVertex2d(o + 275, 257)  # Hand
    glEnd()

    # Body/torso - purple/magenta colored trapezoid
    glColor3ub(197, 30, 255)  # Purple shirt
    glBegin(GL_POLYGON)
    glVertex2d(o + 260, 250)  # Bottom-left
    glVertex2d(o + 270, 250)  # Bottom-right
    glVertex2d(o + 266, 265)  # Top-right (shoulders)
    glVertex2d(o + 264, 265)  # Top-left (shoulders)
    glEnd()
    
    # Head - small black circle
    circlecar(o + 265, 267, 3, 0, 0, 0)  # Radius 3, black color

    # Left leg - gray triangle
    glColor3ub(149, 149, 149)  # Gray pants
    glBegin(GL_POLYGON)
    glVertex2d(o + 260, 250)  # Hip (left side of body)
    glVertex2d(o + 265, 250)  # Hip (center)
    glVertex2d(o + 260, 240)  # Foot
    glEnd()

    # Right leg - gray triangle
    glColor3ub(149, 149, 149)  # Gray pants
    glBegin(GL_POLYGON)
    glVertex2d(o + 265, 250)  # Hip (center)
    glVertex2d(o + 270, 250)  # Hip (right side of body)
    glVertex2d(o + 268, 240)  # Foot
    glEnd()

    # Left shoe - dark blue line at foot
    glColor3ub(0, 0, 105)  # Dark blue
    glLineWidth(2.0)
    glBegin(GL_LINES)
    glVertex2d(o + 263, 240)
    glVertex2d(o + 258, 240)
    glEnd()

    # Right shoe - dark blue line at foot
    glColor3ub(0, 0, 105)  # Dark blue
    glLineWidth(2.0)
    glBegin(GL_LINES)
    glVertex2d(o + 270, 240)
    glVertex2d(o + 265, 240)
    glEnd()

    # ========== PERSON 1 ANIMATION LOGIC ==========
    # Person walks left to right across the screen
    # When o reaches 250, wraps back to -250 (re-enters from left)
    # Speed: 0.2 units per frame
    if o < 250:
        o += 0.2  # Move rightward
    else:
        o = -250  # Wrap to left edge

    # Alternative: For right-to-left movement, uncomment below:
    # if o > -250:
    #     o -= 0.2  # Move leftward
    # else:
    #     o = 250   # Wrap to right edge

    # ========== PERSON 2 (Static Figure) ==========
    # Second stick figure - currently stationary (no animation offset)
    # Similar structure to Person 1 but different position and colors
    # To animate: add a variable offset like Person 1 uses 'o'
    
    # Left arm
    glColor3ub(255, 160, 122)  # Peach/skin color
    glLineWidth(4.0)
    glBegin(GL_LINES)
    glVertex2d(34, 160)  # Shoulder
    glVertex2d(26, 157)  # Hand
    glEnd()

    # Right arm
    glColor3ub(255, 160, 122)  # Peach/skin color
    glLineWidth(4.0)
    glBegin(GL_LINES)
    glVertex2d(36, 160)  # Shoulder
    glVertex2d(45, 157)  # Hand
    glEnd()

    # Body/torso - red colored trapezoid
    glColor3ub(255, 0, 25)  # Red shirt
    glBegin(GL_POLYGON)
    glVertex2d(30, 150)  # Bottom-left
    glVertex2d(40, 150)  # Bottom-right
    glVertex2d(36, 165)  # Top-right (shoulders)
    glVertex2d(34, 165)  # Top-left (shoulders)
    glEnd()
    
    # Head - small black circle
    circlecar(35, 167, 3, 0, 0, 0)  # Radius 3, black color

    # Left leg - gray triangle
    glColor3ub(149, 149, 149)  # Gray pants
    glBegin(GL_POLYGON)
    glVertex2d(30, 150)  # Hip (left)
    glVertex2d(35, 150)  # Hip (center)
    glVertex2d(30, 140)  # Foot
    glEnd()

    # Right leg - gray triangle
    glColor3ub(149, 149, 149)  # Gray pants
    glBegin(GL_POLYGON)
    glVertex2d(35, 150)  # Hip (center)
    glVertex2d(40, 150)  # Hip (right)
    glVertex2d(38, 140)  # Foot
    glEnd()

    # Left shoe - dark blue line
    glColor3ub(0, 0, 105)  # Dark blue
    glLineWidth(2.0)
    glBegin(GL_LINES)
    glVertex2d(33, 140)
    glVertex2d(28, 140)
    glEnd()

    # Right shoe - dark blue line
    glColor3ub(0, 0, 105)  # Dark blue
    glLineWidth(2.0)
    glBegin(GL_LINES)
    glVertex2d(40, 140)
    glVertex2d(35, 140)
    glEnd()

    # ========== BUS 1 (Animated) ==========
    # Green bus moving across the screen using variable 'x'
    # Full bus consists of: body, windows, wheels, door, and lights
    
    # Bus 1 main body - green trapezoid (front-left view)
    # Slanted front creates perspective effect
    glColor3ub(56, 132, 63)  # Dark green color
    glBegin(GL_POLYGON)
    glVertex2d(x + 250, 230)  # Bottom-left corner
    glVertex2d(x + 250, 240)  # Top-left corner
    glVertex2d(x + 256, 255)  # Top-front (windshield angle)
    glVertex2d(x + 310, 255)  # Top-right
    glVertex2d(x + 310, 230)  # Bottom-right
    glEnd()

    # Bus 1 upper window panel - dark strip for window frame
    glColor3ub(1, 1, 1)  # Near-black
    glBegin(GL_POLYGON)
    glVertex2d(x + 308, 253)
    glVertex2d(x + 308, 243)
    glVertex2d(x + 265, 243)
    glVertex2d(x + 265, 253)
    glEnd()

    # Bus 1 passenger windows - 4 white rectangles in a row
    # Represent windows where passengers sit
    windows = [
        (x + 267, 251, x + 275, 245),  # Window 1 (leftmost)
        (x + 277, 251, x + 285, 245),  # Window 2
        (x + 287, 251, x + 295, 245),  # Window 3
        (x + 297, 251, x + 305, 245)   # Window 4 (rightmost)
    ]
    
    glColor3ub(255, 255, 255)  # White windows
    for x1, y1, x2, y2 in windows:
        glBegin(GL_POLYGON)
        glVertex2d(x1, y1)
        glVertex2d(x1, y2)
        glVertex2d(x2, y2)
        glVertex2d(x2, y1)
        glEnd()

    # Bus 1 front windshield - white rectangle at front
    glColor3ub(255, 255, 255)  # White glass
    glBegin(GL_POLYGON)
    glVertex2d(x + 258, 247)
    glVertex2d(x + 258, 233)
    glVertex2d(x + 264, 233)
    glVertex2d(x + 264, 247)
    glEnd()

    # Bus 1 wheels - two white/gray circles at bottom
    circleWheel(x + 266, 227, 4, 4)  # Front wheel
    circleWheel(x + 296, 227, 4, 4)  # Rear wheel
    
    # Bus 1 decorative element - small red circle (headlight or detail)
    circleD(x + 274, 237, 4, 4)

    # Bus 1 door - green rectangle on left side
    glColor3ub(56, 132, 63)  # Green to match bus body
    glBegin(GL_POLYGON)
    glVertex2d(x + 273, 242)
    glVertex2d(x + 273, 230)
    glVertex2d(x + 264, 230)
    glVertex2d(x + 264, 242)
    glEnd()

    # Bus 1 front light/indicator 1 - red rectangle (brake light or turn signal)
    glColor3ub(255, 41, 41)  # Red
    glBegin(GL_POLYGON)
    glVertex2d(x + 280, 241)
    glVertex2d(x + 280, 234)
    glVertex2d(x + 283, 234)
    glVertex2d(x + 283, 241)
    glEnd()

    # Bus 1 front light/indicator 2 - second red rectangle
    glColor3ub(255, 41, 41)  # Red
    glBegin(GL_POLYGON)
    glVertex2d(x + 286, 241)
    glVertex2d(x + 286, 234)
    glVertex2d(x + 292, 234)
    glVertex2d(x + 292, 241)
    glEnd()

    # Bus 1 small decoration - green detail between lights
    glColor3ub(56, 132, 63)  # Green to match body
    glBegin(GL_POLYGON)
    glVertex2d(x + 288, 241)
    glVertex2d(x + 288, 236)
    glVertex2d(x + 290, 236)
    glVertex2d(x + 290, 241)
    glEnd()

    # ========== BUS 2 (Animated) ==========
    # Second green bus - same structure as Bus 1 but offset to the right
    # Both buses share the same 'x' animation variable, moving together
    
    # Bus 2 main body - green trapezoid
    glColor3ub(56, 132, 63)  # Dark green color
    glBegin(GL_POLYGON)
    glVertex2d(x + 370, 230)  # Bottom-left
    glVertex2d(x + 370, 240)  # Top-left
    glVertex2d(x + 376, 255)  # Top-front (windshield)
    glVertex2d(x + 430, 255)  # Top-right
    glVertex2d(x + 430, 230)  # Bottom-right
    glEnd()

    # Bus 2 upper window panel - dark frame
    glColor3ub(1, 1, 1)  # Near-black
    glBegin(GL_POLYGON)
    glVertex2d(x + 428, 253)
    glVertex2d(x + 428, 243)
    glVertex2d(x + 385, 243)
    glVertex2d(x + 385, 253)
    glEnd()

    # Bus 2 passenger windows - 4 white rectangles
    windows2 = [
        (x + 387, 251, x + 395, 245),  # Window 1
        (x + 397, 251, x + 405, 245),  # Window 2
        (x + 407, 251, x + 415, 245),  # Window 3
        (x + 417, 251, x + 425, 245)   # Window 4
    ]
    
    glColor3ub(255, 255, 255)  # White windows
    for x1, y1, x2, y2 in windows2:
        glBegin(GL_POLYGON)
        glVertex2d(x1, y1)
        glVertex2d(x1, y2)
        glVertex2d(x2, y2)
        glVertex2d(x2, y1)
        glEnd()

    # Bus 2 front windshield
    glColor3ub(255, 255, 255)  # White glass
    glBegin(GL_POLYGON)
    glVertex2d(x + 378, 247)
    glVertex2d(x + 378, 233)
    glVertex2d(x + 384, 233)
    glVertex2d(x + 384, 247)
    glEnd()

    # Bus 2 wheels - two circles
    circleWheel(x + 386, 227, 4, 4)  # Front wheel
    circleWheel(x + 416, 227, 4, 4)  # Rear wheel
    
    # Bus 2 decorative element
    circleD(x + 394, 237, 4, 4)

    # Bus 2 door - green rectangle
    glColor3ub(56, 132, 63)  # Green
    glBegin(GL_POLYGON)
    glVertex2d(x + 393, 242)
    glVertex2d(x + 393, 230)
    glVertex2d(x + 384, 230)
    glVertex2d(x + 384, 242)
    glEnd()

    # Bus 2 front light/indicator 1 - red rectangle
    glColor3ub(255, 41, 41)  # Red
    glBegin(GL_POLYGON)
    glVertex2d(x + 400, 241)
    glVertex2d(x + 400, 234)
    glVertex2d(x + 403, 234)
    glVertex2d(x + 403, 241)
    glEnd()

    # Bus 2 front light/indicator 2 - red rectangle
    glColor3ub(255, 41, 41)  # Red
    glBegin(GL_POLYGON)
    glVertex2d(x + 406, 241)
    glVertex2d(x + 406, 234)
    glVertex2d(x + 412, 234)
    glVertex2d(x + 412, 241)
    glEnd()

    # Bus 2 small decoration - green detail
    glColor3ub(56, 132, 63)  # Green
    glBegin(GL_POLYGON)
    glVertex2d(x + 408, 241)
    glVertex2d(x + 408, 236)
    glVertex2d(x + 410, 236)
    glVertex2d(x + 410, 241)
    glEnd()

    # ========== BUS ANIMATION LOGIC ==========
    # Both buses move together from right to left across the screen
    # When x drops below -430, reset to 250 (wrap from left back to right)
    # Speed: 0.7 units per frame (faster than people)
    if x > -430:
        x -= 0.7  # Move buses leftward
    else:
        x = 250   # Wrap back to right edge

    # Alternative: For left-to-right movement, uncomment below:
    # if x < 250:
    #     x += 0.7   # Move buses rightward
    # else:
    #     x = -430   # Wrap back to left edge

    glFlush()

def update(value):
    """
    GLUT timer update callback.

    Posts a redisplay request and re-registers itself to drive animation.
    """
    glutPostRedisplay()
    glutTimerFunc(15, update, 0)

def main():
    """
    Entry point for the composite graphics scene.

    Creates a GLUT window, initializes the projection, registers display
    and timer callbacks, and enters the event loop.
    """
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(1000, 1000)
    glutInitWindowPosition(100, 0)
    glutCreateWindow(b"Computer Graphics Project")
    myInit()
    glutDisplayFunc(display)
    glutTimerFunc(25, update, 0)
    glutMainLoop()

if __name__ == "__main__":
    main()

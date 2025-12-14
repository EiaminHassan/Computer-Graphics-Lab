import sys
import math
import time
from datetime import datetime

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


# ---------- Globals ----------

# Display window dimensions (pixels)
window_width = 800
window_height = 600

# Reference time used for calculating elapsed time for animation
start_time = time.time()

# Pendulum settings - Control the swinging motion behavior
PENDULUM_MAX_ANGLE_DEG = 30.0   # Maximum angle from center (±30° swing arc)
PENDULUM_PERIOD = 2.0           # Period of full oscillation: left->right->left (in seconds)


# ---------- Drawing helpers ----------

def draw_rectangle(x1, y1, x2, y2):
    """
    Draw a filled axis-aligned rectangle with current color.

    Parameters:
    - x1, y1: Bottom-left corner coordinates (in normalized device coordinates)
    - x2, y2: Top-right corner coordinates (in normalized device coordinates)

    Transformation: NONE - Uses raw vertices in current coordinate system
    Rendering: OpenGL GL_QUADS immediate mode for solid filled rectangle
    Uses current glColor setting to fill the rectangle.
    """
    glBegin(GL_QUADS)
    glVertex2f(x1, y1)
    glVertex2f(x2, y1)
    glVertex2f(x2, y2)
    glVertex2f(x1, y2)
    glEnd()


def draw_circle(cx, cy, r, segments=64):
    """
    Draw a filled circle using triangle fan primitives.

    Parameters:
    - cx, cy: Circle center coordinates (in normalized device coordinates)
    - r: Circle radius (in normalized device coordinates)
    - segments: Number of segments used to approximate the circle (higher = smoother)

    Transformation: NONE - Uses raw vertices in current coordinate system
    Rendering: GL_TRIANGLE_FAN radiates triangles from center to approximate circular shape
    Uses current glColor setting to fill the circle.
    """
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(cx, cy)
    for i in range(segments + 1):
        angle = 2.0 * math.pi * i / segments
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        glVertex2f(x, y)
    glEnd()


def draw_line(x1, y1, x2, y2, width=1.0):
    """
    Draw a straight line segment with configurable width.

    Parameters:
    - x1, y1: Start point coordinates (in normalized device coordinates)
    - x2, y2: End point coordinates (in normalized device coordinates)
    - width: Line width in pixels (OpenGL line width setting)

    Transformation: NONE - Uses raw vertices in current coordinate system
    Rendering: GL_LINES primitive for line segment
    Sets glLineWidth before drawing and resets to 1.0 after.
    """
    glLineWidth(width)
    glBegin(GL_LINES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glEnd()
    glLineWidth(1.0)


# ---------- Clock parts ----------

def draw_case():
    """
    Draw the wooden case of the grandfather clock (2D front view).

    Renders three rectangles representing:
    - Main body: outer rectangular frame of the clock (-0.4 to 0.4 width, -0.9 to 0.9 height)
    - Inner panel: lighter wood panel inside the case (for depth/contrast effect)
    - Base plinth: decorative base section at the bottom of the case

    Color palette: Uses warm brown tones to approximate wooden texture (flat shading).
    Transformations: NONE - All coordinates are in local clock coordinate system.
    Rendering order: Back to front (main body first, then details).
    """
    glColor3f(0.4, 0.2, 0.05)  # dark brown wood

    # Main body
    draw_rectangle(-0.4, -0.9, 0.4, 0.9)

    # Inner lighter panel
    glColor3f(0.6, 0.3, 0.1)
    draw_rectangle(-0.32, -0.82, 0.32, 0.82)

    # Base
    glColor3f(0.3, 0.15, 0.05)
    draw_rectangle(-0.5, -0.9, 0.5, -0.8)


def draw_clock_face():
    """
    Draw the circular clock face, rim, and hour tick marks.

    Components rendered:
    - Filled circle: Light-colored background (0.95, 0.95, 0.92) representing the clock face
    - Outer rim: Dark line loop around the circle (radius 0.22) for visual definition
    - 12 tick marks: Major hour markers radiating from center to face edge

    Transformations: NONE - All coordinates centered at (0.0, 0.45) in local space.
    Geometry: Circle positioned near top of clock case (cy=0.45), radius=0.22
    Tick marks: Positioned using trigonometric angles (360°/12 hours = 30° apart)
    """
    cx, cy = 0.0, 0.45
    radius = 0.22

    # Face background
    glColor3f(0.95, 0.95, 0.92)
    draw_circle(cx, cy, radius, segments=80)

    # Outer rim
    glColor3f(0.2, 0.2, 0.2)
    glLineWidth(2)
    glBegin(GL_LINE_LOOP)
    segments = 80
    for i in range(segments):
        angle = 2.0 * math.pi * i / segments
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        glVertex2f(x, y)
    glEnd()
    glLineWidth(1)

    # Hour tick marks (12 major)
    glColor3f(0.1, 0.1, 0.1)
    for i in range(12):
        theta = 2.0 * math.pi * i / 12.0
        # Outer and inner radii for ticks
        r_outer = radius * 0.95
        r_inner = radius * 0.80
        x1 = cx + r_inner * math.cos(theta)
        y1 = cy + r_inner * math.sin(theta)
        x2 = cx + r_outer * math.cos(theta)
        y2 = cy + r_outer * math.sin(theta)
        draw_line(x1, y1, x2, y2, width=2)


def draw_clock_hands():
    """
    Draw hour, minute, and second hands based on current system time.

    Angle calculation:
    - Second hand: 360°/60 seconds = 6° per second
    - Minute hand: 360°/60 minutes = 6° per minute  
    - Hour hand: 360°/12 hours = 30° per hour
    - Negative angles account for clockwise rotation in typical clock fashion

    Transformations used for each hand:
    1. glPushMatrix() - Save current transformation state
    2. glTranslatef(cx, cy, 0.0) - TRANSLATION: Move origin to clock face center (0.0, 0.45)
    3. glRotatef(angle, 0.0, 0.0, 1.0) - ROTATION: Rotate around Z-axis by computed angle
    4. draw_line(...) - Draw line from center outward (pivot point is now at origin)
    5. glPopMatrix() - Restore previous transformation state

    Center cap: Small circle at rotation pivot (0.0, 0.45) covers rotation center.
    """
    # Use real system time
    now = datetime.now()
    sec = now.second + now.microsecond / 1e6
    minute = now.minute + sec / 60.0
    hour = (now.hour % 12) + minute / 60.0

    # Angles in degrees (0 at 12 o'clock, positive CCW)
    # We negate them to get clockwise rotation (typical clock) in OpenGL.
    second_angle = -6.0 * sec          # 360°/60s = 6° per second
    minute_angle = -6.0 * minute       # 360°/60min
    hour_angle = -30.0 * hour          # 360°/12h = 30° per hour

    cx, cy = 0.0, 0.45

    # Hour hand
    glPushMatrix()
    glTranslatef(cx, cy, 0.0)
    glRotatef(hour_angle, 0.0, 0.0, 1.0)
    glColor3f(0.1, 0.1, 0.1)
    draw_line(0.0, 0.0, 0.0, 0.11, width=5)
    glPopMatrix()

    # Minute hand
    glPushMatrix()
    glTranslatef(cx, cy, 0.0)
    glRotatef(minute_angle, 0.0, 0.0, 1.0)
    glColor3f(0.1, 0.1, 0.1)
    draw_line(0.0, 0.0, 0.0, 0.18, width=3)
    glPopMatrix()

    # Second hand
    glPushMatrix()
    glTranslatef(cx, cy, 0.0)
    glRotatef(second_angle, 0.0, 0.0, 1.0)
    glColor3f(0.8, 0.0, 0.0)
    draw_line(0.0, 0.0, 0.0, 0.19, width=1)
    glPopMatrix()

    # Center cap
    glColor3f(0.1, 0.1, 0.1)
    draw_circle(cx, cy, 0.01, segments=24)


def draw_pendulum():
    """
    Draw a swinging pendulum driven by a sine-based harmonic motion model.

    Motion model (Simple Harmonic Motion - SHM):
    - angle(t) = θ_max × sin(ω × t)
    - θ_max = 30° (maximum swing angle from vertical)
    - ω = 2π/T (angular frequency, where T = PENDULUM_PERIOD = 2 seconds)
    - Result: Smooth oscillation between -30° and +30° from center

    Components rendered:
    - Rod: Thin brown rectangle (-rod_half_width to rod_half_width width, full rod_length)
    - Bob: Gold-colored circle at bottom of rod (pendulum weight)
    - Pivot: Small dark circle at rotation point

    Transformations applied:
    1. glPushMatrix() - Save transformation state
    2. glTranslatef(pivot_x, pivot_y, 0.0) - TRANSLATION: Move to pivot point (0.0, 0.15)
    3. glRotatef(angle_deg, 0.0, 0.0, 1.0) - ROTATION: Rotate around Z-axis by calculated angle
    4. draw_rectangle(...) and draw_circle(...) - Draw pendulum components
    5. glPopMatrix() - Restore transformation state
    
    Pivot point is fixed at (0.0, 0.15), just below the clock face center.
    """
    elapsed = time.time() - start_time

    omega = 2.0 * math.pi / PENDULUM_PERIOD
    # sin(...) is in [-1, 1], so multiply by max angle (in degrees)
    angle_deg = PENDULUM_MAX_ANGLE_DEG * math.sin(omega * elapsed)

    # Pivot point, just below the clock face
    pivot_x = 0.0
    pivot_y = 0.15

    rod_length = 0.55
    rod_half_width = 0.01

    bob_radius = 0.045

    glPushMatrix()
    # Move to pivot
    glTranslatef(pivot_x, pivot_y, 0.0)
    # Rotate around z-axis (2D) by angle_deg
    glRotatef(angle_deg, 0.0, 0.0, 1.0)

    # Draw rod (in local coordinates, pivot at origin)
    glColor3f(0.3, 0.2, 0.05)
    draw_rectangle(-rod_half_width, -rod_length, rod_half_width, 0.0)

    # Draw bob (circle) at bottom of rod
    glColor3f(0.85, 0.7, 0.2)
    draw_circle(0.0, -rod_length - bob_radius * 0.1, bob_radius, segments=40)

    glPopMatrix()

    # Optional: draw small pivot point
    glColor3f(0.1, 0.1, 0.1)
    draw_circle(pivot_x, pivot_y, 0.01, segments=24)
    

# ---------- Public draw function for importing into other scenes ----------
def draw_grandfather_clock(world_x, world_y, scale):
    """
    Draw the grandfather clock inside an existing OpenGL scene.
    This is a public interface function for reusing the clock in larger scenes.

    Parameters:
    - world_x, world_y: Bottom-center position in the caller's coordinate system
    - scale: Uniform scale multiplier applied equally to X and Y axes

    Transformation sequence (applied in order - matrix composition):
    1. glPushMatrix() - Save current transformation state
    2. glTranslatef(world_x, world_y, 0.0) - TRANSLATION: Move to world position
    3. glScalef(scale, scale, 1.0) - UNIFORM SCALING: Scale in X and Y (Z=1.0 for 2D)
    4. glTranslatef(0.0, 0.9, 0.0) - TRANSLATION: Align clock bottom at y=0 (shift model up by 0.9)
    5. draw_case/face/hands/pendulum() - Render all clock components
    6. glPopMatrix() - Restore previous transformation state

    Purpose: Allows reusable clock module that can be positioned and sized anywhere in a scene.
    """
    glPushMatrix()
    glTranslatef(world_x, world_y, 0.0)
    glScalef(scale, scale, 1.0)

    # shift local model so its bottom (y=-0.9) sits on y=0
    glTranslatef(0.0, 0.9, 0.0)

    draw_case()
    draw_clock_face()
    draw_clock_hands()
    draw_pendulum()

    glPopMatrix()


# ---------- GLUT callbacks ----------

def display():
    """
    GLUT display callback - called by GLUT whenever window needs redrawing.

    Operations:
    1. glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) - Clear screen to background color
    2. glLoadIdentity() - Reset modelview matrix to identity (no transformations)
    3. Render all clock components in back-to-front order for proper depth perception
    4. glutSwapBuffers() - Swap front and back buffers (enables smooth double-buffered animation)

    Transformations: NONE in this function (all handled by component draw functions)
    Rendering order: case → face → hands → pendulum (ensures correct visual layering)
    Frame rate: Controlled by timer() callback (~60 FPS)
    """
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Draw things in order back-to-front
    draw_case()
    draw_clock_face()
    draw_clock_hands()
    draw_pendulum()

    glutSwapBuffers()


def reshape(width, height):
    """
    GLUT reshape callback - called when window is resized.

    Operations performed:
    1. Update viewport: glViewport(0, 0, width, height) - Render to full window
    2. Set projection matrix to orthographic projection (2D view, no perspective)
    3. Calculate aspect ratio: width / height
    4. Adjust glOrtho() bounds to maintain aspect ratio
       - If aspect >= 1.0 (wider than tall): X range = [-aspect, aspect], Y range = [-1, 1]
       - If aspect < 1.0 (taller than wide): X range = [-1, 1], Y range = [-1/aspect, 1/aspect]

    Transformations applied:
    - glMatrixMode(GL_PROJECTION) - Select projection matrix stack
    - glLoadIdentity() - Reset to identity matrix
    - glOrtho(...) - ORTHOGRAPHIC PROJECTION: Maps 3D world coords to 2D screen (parallel projection)
    - glMatrixMode(GL_MODELVIEW) - Switch back to modelview matrix for scene rendering

    Purpose: Ensures clock maintains correct proportions when window is resized.
    """
    global window_width, window_height
    window_width = width
    window_height = height

    glViewport(0, 0, width, height)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    # Maintain aspect ratio using an orthographic projection
    aspect = width / float(height) if height > 0 else 1.0

    # Base coordinate system from -1..1 in shorter dimension
    if aspect >= 1.0:
        # Wider than tall
        glOrtho(-1.0 * aspect, 1.0 * aspect, -1.0, 1.0, -1.0, 1.0)
    else:
        # Taller than wide
        glOrtho(-1.0, 1.0, -1.0 / aspect, 1.0 / aspect, -1.0, 1.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def timer(value):
    """
    GLUT timer callback - handles continuous animation timing.

    Operations:
    1. glutPostRedisplay() - Request a redraw (calls display() function)
    2. glutTimerFunc(16, timer, 0) - Re-register this callback after 16 milliseconds

    Timing:
    - 16 ms interval corresponds to approximately 62.5 FPS (1000/16 ≈ 62.5)
    - Each redraw calls display(), which renders updated clock with current time
    - Pendulum animation is calculated in draw_pendulum() using elapsed time

    Flow: timer() → glutPostRedisplay() → display() → draw_clock_hands() + draw_pendulum() → repeat
    """
    glutPostRedisplay()
    glutTimerFunc(16, timer, 0)  # roughly 60 FPS


def init_gl():
    """
    Initialize OpenGL rendering state before main loop.

    Configuration:
    1. glClearColor(1.0, 1.0, 1.0, 1.0) - Set background to white (RGBA: 1.0=full intensity)
    2. glEnable(GL_BLEND) - Enable alpha blending for transparency/antialiasing
    3. glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA) - Set blending equation
       - SRC_ALPHA: Use alpha channel of source (foreground) pixel
       - ONE_MINUS_SRC_ALPHA: Inverse alpha of source for background
       - Result: Smooth feathering at edges (antialiased appearance)

    Effect: Produces smoother-looking geometric primitives and handles transparency.
    """
    glClearColor(1.0, 1.0, 1.0, 1.0)  # white background
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


def main():
    """
    Entry point for standalone clock visualization using GLUT.

    Initialization sequence:
    1. glutInit(sys.argv) - Initialize GLUT library with command-line arguments
    2. glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
       - GLUT_DOUBLE: Double-buffered rendering (smooth animation)
       - GLUT_RGB: RGB color model
       - GLUT_DEPTH: Depth buffer for hidden surface removal
    3. glutInitWindowSize(width, height) - Set initial window dimensions
    4. glutCreateWindow(...) - Create window with title
    5. init_gl() - Initialize OpenGL state (colors, blending, etc.)
    6. Register GLUT callbacks:
       - display: Render function (called by timer)
       - reshape: Window resize handler
       - timer: Animation update function
    7. glutMainLoop() - Enter infinite event loop
       - Processes events and calls registered callbacks
       - Runs until window is closed

    Transformation pipeline during rendering:
    - Window coordinates → Viewport → Projection matrix (glOrtho) → Model-view matrix
    """
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(window_width, window_height)
    glutCreateWindow(b"Swinging Pendulum Grandfather Clock - Python OpenGL")

    init_gl()

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutTimerFunc(0, timer, 0)

    glutMainLoop()


if __name__ == "__main__":
    main()

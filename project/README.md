# Computer Graphics Project – Scene and Clock Explanation

This README walks through `main.py` step by step, in simple terms, so you can confidently explain the program.

## Overview

- The program draws a 2D scene using OpenGL (via PyOpenGL).
- It shows sky, roads, buildings, a mosque, trees, buses, clouds, the sun, and animated people.
- A swinging grandfather clock (from `clock.py`) is placed on one of the buildings.
- Animation is driven by GLUT timer callbacks.

## How the Program Starts

1. `main()` creates a window and initializes GLUT (the toolkit that manages windows and events).
2. `myInit()` sets the background color and defines an orthographic projection (a 2D coordinate system from 0 to 500 in both X and Y).
3. Two callbacks are registered:
   - `display()` – draws the whole scene every frame.
   - `update()` – schedules redrawing periodically to animate things.
4. `glutMainLoop()` starts the event loop so the program keeps running and updating.

## Coordinate System

- `glOrtho(0, 500, 0, 500, -10, 10)` makes a 2D canvas.
- X increases left → right from 0 to 500.
- Y increases bottom → top from 0 to 500.

## Global Animation Variables

- `a, b`: control the sun’s position (it moves diagonally).
- `m, n`: control cloud movement.
- `x`: controls the buses moving across the scene.
- `o`: controls one animated person’s horizontal movement.

## Drawing Helpers (Reusable Shapes)

- `circlecar(x, y, rad, r, g, b)`: draws a filled circle (used for clouds and small round shapes).
- `circleWheel(x, y, rx, ry)`: draws a filled wheel/ellipse for bus wheels.
- `circleD(x, y, rx, ry)`: draws a decorative filled ellipse.
- `sun(x, y, rx, ry)`: draws the sun as a circle/ellipse using warm colors.
- `circle(h, k, rx, ry, r, g, b)`: draws an ellipse using polygon approximation.

All of these use OpenGL’s immediate mode (`glBegin`/`glEnd`) to place vertices.

## The `display()` Function – Building the Scene

`display()` is called repeatedly to draw the frame.

1. Clear the screen: `glClear(GL_COLOR_BUFFER_BIT)`.
2. Draw the sky: a big rectangle split into lower white (near horizon) and upper blue.
3. Left background and roads: several quads/polygons form ground and road segments.
4. Mosque:
   - Main body: a big polygon.
   - Upper bar (light and dark layers).
   - Front sections and windows using rectangles and triangles.
5. Sun and clouds:
   - `sun(a + 200, b + 300, 30, 30)` makes the sun; `a` and `b` slowly increase.
   - Clouds are multiple small circles grouped together; `m` animates them sideways.
6. AB1 building complex (multiple parts):
   - Part 1, Part 2, Part 3, Part 4, Part 5, Part 6 – each is a polygon block.
   - Each part has windows drawn as smaller rectangles.
7. Place the grandfather clock on “AB1 Part2 Another Building”:
   - A special block at `x=[90..137], y=[250..345]` acts as the facade.
   - Switch to `GL_MODELVIEW`, reset model matrix, then call:
     - `clock.draw_grandfather_clock(world_x=113.5, world_y=250.0, scale=49.0)`.
   - The clock module handles drawing the case, face, hands, and swinging pendulum.
8. Field and lines: a green polygon for the field and several white line segments for markings.
9. Trees: repeated small polygons for trunk and leaves along the field.
10. Animated people:
    - Person 1: lines for arms, polygons for body/legs, small circle for head; moves with `o`.
    - Person 2: another static person near the left.
11. Buses:
    - Two bus bodies as rectangles; windows as smaller white rectangles.
    - Wheels as circles; decorative elements as small polygons.
    - The buses slide left across the screen using `x`.
12. Update animation state:
    - Sun: `a` and `b` increase until a limit.
    - Clouds: `m` moves and wraps when reaching the edge.
    - Person 1: `o` moves and wraps.
    - Buses: `x` decreases (move left) then resets.
13. Flush the pipeline: `glFlush()` ensures commands are executed.

## Function-by-Function Summary (main.py)

This section lists every function and its role.

- `myInit()`:
  - Sets clear color (background) and selects the projection matrix.
  - Applies `glOrtho(0, 500, 0, 500, -10, 10)` for a 2D coordinate space.
- `circlecar(x, y, rad, r, g, b)`:
  - Draws a filled circle via `GL_TRIANGLE_FAN` around center `(x, y)`.
  - `rad` is radius; `(r,g,b)` is color in 0..255.
- `circleWheel(x, y, rx, ry)`:
  - Draws a filled wheel/ellipse via `GL_TRIANGLE_FAN` around `(x, y)`.
  - `rx`, `ry` are ellipse radii along X and Y.
- `circleD(x, y, rx, ry)`:
  - Decorative ellipse using the same technique and a red color.
- `sun(x, y, rx, ry)`:
  - Sun ellipse with warm colors; position is animated using `a` and `b`.
- `circle(h, k, rx, ry, r, g, b)`:
  - Generic filled ellipse via polygon approximation; color uses 0..255 inputs normalized to 0..1.
- `display()`:
  - Main draw routine; composes sky, roads, mosque, buildings, trees, people, buses, clouds, sun.
  - Calls into `clock.draw_grandfather_clock(...)` to render the clock on the facade.
  - Updates animation variables (`a`, `b`, `m`, `x`, `o`) to move elements.
- `update(value)`:
  - Timer callback; posts a redisplay and re-schedules itself to maintain animation.
- `main()`:
  - Bootstraps GLUT window, calls `myInit()`, registers callbacks, enters event loop.

## The `update()` Function – Animation Timer

- `update(value)` posts a redisplay and schedules itself after ~15 ms.
- This keeps the scene updating smoothly.

## The `myInit()` Function – Scene Setup

- Sets a reddish clear color for the sky background.
- Chooses the projection matrix and applies an orthographic 2D projection.

## The `main()` Function – Bootstrapping

- Initializes GLUT, creates the window, calls `myInit()`, installs callbacks, and starts the main loop.

## How the Clock is Integrated

- The clock is imported from `clock.py` (`import clock`).
- In `display()`, a matrix push/reset isolates transformations.
- `clock.draw_grandfather_clock(...)` is called with a base position and a uniform scale so it fits the facade.
- Inside `clock.py`, the clock components are drawn in local coordinates and then scaled/translated.

## Run It

From the project folder:

```powershell
python .\main.py
```

If you want to quickly adjust the clock size or position:

- Edit `scale` in the call to `clock.draw_grandfather_clock(...)` in `main.py`.
- Adjust `world_x` or `world_y` to shift horizontal or vertical placement.

## Key Talking Points for a Presentation

- Uses an orthographic 2D projection for easy pixel-like positioning.
- Scene is built from simple geometric primitives: quads, polygons, lines, and circles.
- Animation is achieved by small variable updates in a timer callback.
- The clock module demonstrates hierarchical transforms (translate + scale) and time-based rotation for hands and pendulum.
- Immediate mode rendering (simple to learn) is used for clarity in educational contexts.

---

## Movement Recipes (How to Implement Specific Animations)

Below are clear steps to achieve each requested animation using the existing variables and patterns in `main.py`.

### 1) Cloud movement from right to left

- Idea: Increase `m` to shift cloud centers to the right; decrease to shift left. The current code moves clouds to the right; for right-to-left, we want them to go the other way.
- Implementation: In `display()`, find the cloud update block and change the direction logic.

Current logic (moves to the right, then wraps):

```python
if m < 250:
   m += 0.3
else:
   m = -50
```

Right-to-left movement (decrease `m` over time, wrap when too far left):

```python
if m > -50:
   m -= 0.3  # move left
else:
   m = 250   # wrap back to the right
```

This makes the entire cloud group slide left across the sky.

### 2) Bus running from left to right

- Idea: The variable `x` offsets bus positions. Currently buses move left (`x` decreases). To move right, increase `x` over time and wrap when exceeding the canvas.

Current logic (moves left, then resets):

```python
if x > -430:
   x -= 0.7
else:
   x = 250
```

Left-to-right movement (increase `x`, wrap to the left when too far right):

```python
if x < 250:
   x += 0.7  # move right
else:
   x = -430  # wrap back to the left
```

This slides both buses to the right since they use `x` for their offsets.

### 3) Make the standing person move (start animating the static one)

- Idea: The second person is currently static (no `o` offset). Reuse `o` or introduce a new variable (e.g., `p`) to shift its X positions.
- Minimal change: Reuse `o` for Person 2 with a separate speed or reuse existing update logic.

Example (reuse `o` but scaled to move slowly):

```python
# Before drawing Person 2, add an offset, e.g., px = o * 0.3
px = o * 0.3
# Replace hard-coded X values like 34, 36, 40 with (34+px), (36+px), (40+px)
# Do this consistently for that person’s vertices.

# Update logic already exists:
if o < 250:
   o += 0.2
else:
   o = -250
```

- Alternative: Use a new variable `p` so each person can have independent motion:

```python
# Globals:
p = 0.0

# In update block:
if p < 300:
   p += 0.15
else:
   p = -100

# In Person 2 drawing, add +p to all X coordinates.
```

### 4) Person walking right to left

- Idea: Use a motion variable (e.g., `o` or `p`) and subtract over time for right-to-left motion.

Example using `o` (reverse direction):

```python
if o > -250:
   o -= 0.2  # move left
else:
   o = 250   # wrap to the right edge
```

Apply `+ o` to the X coordinates of that person’s vertices (as already done for Person 1), and the figure will walk right-to-left.

Tip: For a more “walking” look, you can animate arm/leg angles by slightly varying some Y coordinates or adding small rotations in a periodic way (e.g., using `math.sin` with time).

---

## Notes on Animation Timing

- All movement depends on the `update()` timer callback, which calls `glutTimerFunc(15, update, 0)`.
- Lower timer interval (e.g., 10 ms) = faster updates; higher interval = slower.
- Speed of each moving element is controlled by the increments (`+= 0.2`, `-= 0.7`, etc.). Adjust these for smoother or faster motion.

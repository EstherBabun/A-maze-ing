# A-maze-ing
 Create your own maze generator and display its result!

# Usefull tools

- #### [mypy](#https://mypy.readthedocs.io/en/stable/) for static type checking
    flags to use : 
    - --warn-return-any 
    - --warn-unused-ignores 
    - --ignore-missing-imports
    - --disallow-untyped-defs 
    - --check-untyped-defs

- #### [PEP 257](#https://peps.python.org/pep-0257/) for docstring convention

- #### [flake8](#https://flake8.pycqa.org/en/latest/) for Style Enforcement

- #### [pytest](#https://docs.pytest.org/en/stable/) for unit testing
    Note: pytest is more intuitive than unittest
- #### [venv](#https://docs.python.org/3/library/venv.html) for virtual environments
    ```bash
    # Create venv in the project's root folder
    $ python3 -m venv /path/to/venv
    ```
    ```bash
    # Activate it 
    # under bash/zsh :
    $ source venv/bin/activate
    ```
    ```bash
    # install dependencies and tools
    (venv) $ install <your_py_tool>
    ```
    ```bash
    # When done working, deactivate
    (venv) $ deactivate
    ```

- #### [pdb](#https://docs.python.org/3/library/pdb.html) for python debugging

- #### [MiniLibX](#https://harm-smits.github.io/42docs/libs/minilibx) graphics library for visual rendering



# Theory
- Prim's, Kruskal's and the recursive backtracker algorithms for maze generation.
- Perfect mazes are related to spanning trees in graph theory.


# config.txt
example:
```
"WIDTH=20"
"HEIGHT=15"
"ENTRY=0,0"
"EXIT=19,14"
"OUTPUT_FILE=maze.txt"
"PERFECT=True"

Note: We may add additional keys (e.g., seed, algorithm, display mode) if useful.
```
<br/>

# MLX for python3

## Step1: Extract and install

- Download  mlx-2.2-py3-ubuntu-any.whl form the project's page and move it to the project's root.
- Extract and install the MLX wheel manually in the site-packages of our virtual environement (venv)

Install in venv:
```bash
# Make sure you're in your project directory with venv activated
cd ~/Desktop/A-maze-ing

# Extract the wheel
mkdir mlx_temp 
cd mlx_temp
unzip ../mlx-2.2-py3-ubuntu-any.whl

# Copy to site-packages
cp -r mlx ../venv/lib/python3.10/site-packages/
cp -r mlx-2.2.dist-info ../venv/lib/python3.10/site-packages

# Clean up
cd ..
rm -rf mlx_temp

# Test
python3 -c "import mlx; print('✓ MLX installed successfully!')"
```

# MLX for Python: Complete Comprehensive Guide
### Based on Official 42 Documentation

## Table of Contents
1. [Introduction](#introduction)
2. [Installation & Setup](#installation--setup)
3. [Core Concepts](#core-concepts)
4. [Initialization](#initialization)
5. [Window Management](#window-management)
6. [Colors in MLX](#colors-in-mlx)
7. [Drawing Functions](#drawing-functions)
8. [Image Manipulation (The Correct Way)](#image-manipulation-the-correct-way)
9. [Events & Hooks](#events--hooks)
10. [Event Loop](#event-loop)
11. [Mouse Functions](#mouse-functions)
12. [Advanced Topics](#advanced-topics)
13. [Complete Examples](#complete-examples)
14. [Common Pitfalls & Solutions](#common-pitfalls--solutions)

---

## Introduction

### What is MiniLibX?

MiniLibX is a tiny graphics library which allows you to do the most basic things for rendering something in screens without any knowledge of X-Window and Cocoa. It provides so-called simple window creation, a questionable drawing tool, half-ass image functions and a weird event management system.

Despite its quirky description, MLX is the standard graphics library for 42 School projects and provides a simple interface for:
- Window creation and management
- Pixel and image rendering
- Event handling (keyboard, mouse)
- Basic animations

### Python Wrapper Architecture

The Python MLX wrapper uses `ctypes` to interface with the native C library (`libmlx.so`). This means:
- All C pointers are represented as Python `c_void_p` objects
- The wrapper automatically manages callback references to prevent garbage collection
- Some C functions returning values via pointers are converted to return tuples (Pythonic API)
- **Performance is identical to C** since we're calling the same native library

---

## Installation & Setup

### Linux Installation

MiniLibX for Linux requires `xorg`, `x11` and `zlib`, therefore you will need to install the following dependencies: `xorg`, `libxext-dev` and `zlib1g-dev`.

```bash
sudo apt-get update && sudo apt-get install xorg libxext-dev zlib1g-dev libbsd-dev
```

For the Python wrapper, you'll need the `mlx.py` file and `libmlx.so` in your project directory.

### MacOS Installation

Because MiniLibX requires Cocoa of MacOSX (AppKit) and OpenGL (it doesn't use X11 anymore) we need to link them accordingly.

The Python wrapper will handle linking automatically, but you need the MLX library compiled for macOS.

### Windows (WSL2/WSLg)

Windows 11's WSL comes with an option to run graphic applications directly. To enable this, follow their official guide for running linux gui apps in wsl. When you have finished the installation, you can simply compile and run minilibx apps and they will appear like an actual application as if they were executed in windows.

---

## Core Concepts

### The Three Pointer Types

MLX uses three main pointer types that you must understand:

1. **`mlx_ptr`** - The MLX instance
   - Created by `mlx_init()`
   - Represents the connection to the graphics system
   - Required by almost all MLX functions

2. **`win_ptr`** - Window identifier  
   - Created by `mlx_new_window()`
   - Identifies a specific window
   - Required for drawing and event handling

3. **`img_ptr`** - Image identifier
   - Created by `mlx_new_image()` or image loading functions
   - Represents an image buffer in memory
   - **The correct way to draw graphics efficiently**

### The Event-Driven Architecture

All hooks in MiniLibX are nothing more than a function that gets called whenever a event is triggered.

MLX applications work by:
1. Setting up windows and graphics
2. Registering callback functions ("hooks") for events
3. Entering the event loop with `mlx_loop()`
4. Responding to events through callbacks

---

## Initialization

### `mlx_init()`

**Purpose**: This will establish a connection to the correct graphical system and will return a `void *` which holds the location of our current MLX instance.

**Signature**:
```python
mlx_ptr = m.mlx_init()
```

**Returns**: 
- Pointer to MLX instance on success
- `None` on failure

**Example**:
```python
from mlx import Mlx

m = Mlx()
mlx_ptr = m.mlx_init()

if mlx_ptr is None:
    print("Failed to initialize MLX")
    exit(1)
```

**What it does**:
- Connects to X11 (Linux) or Cocoa/OpenGL (macOS)
- Initializes internal data structures
- Returns identifier for this connection

---

## Window Management

### `mlx_new_window(mlx_ptr, width, height, title)`

**Purpose**: Creates a new window.

**Signature**:
```python
win_ptr = m.mlx_new_window(mlx_ptr, width, height, title)
```

**Parameters**:
- `mlx_ptr`: The MLX instance
- `width`: Window width in pixels
- `height`: Window height in pixels  
- `title`: Window title (string)

**Returns**: Window pointer or `None` on failure

**Example**:
```python
# Create a 1920x1080 window
win_ptr = m.mlx_new_window(mlx_ptr, 1920, 1080, "Hello world!")
```

**Coordinate System**: (0,0) is the top-left corner.

---

### `mlx_clear_window(mlx_ptr, win_ptr)`

**Purpose**: Clears the entire window to black.

**Example**:
```python
m.mlx_clear_window(mlx_ptr, win_ptr)
```

---

### `mlx_destroy_window(mlx_ptr, win_ptr)`

**Purpose**: Destroys a window and frees its resources.

**Example**:
```python
m.mlx_destroy_window(mlx_ptr, win_ptr)
```

**Important**: Don't use `win_ptr` after destroying it!

---

## Colors in MLX

### Color Format: TRGB

We shift bits to use the TRGB format. To define a color, we initialize it as follows: `0xTTRRGGBB`

Where:
- `T` = Transparency (often ignored)
- `R` = Red component (0x00-0xFF)
- `G` = Green component (0x00-0xFF)
- `B` = Blue component (0x00-0xFF)

### **CRITICAL: BGR vs RGB**

⚠️ **On most systems, MLX actually uses BGR (Blue-Green-Red) format internally!**

This means:
```python
# What you think     →  What you need
0xFF0000  # "Red"    →  0x0000FF  # Actually displays red
0x00FF00  # "Green"  →  0x00FF00  # Green is the same
0x0000FF  # "Blue"   →  0xFF0000  # Actually displays blue
```

### Standard Colors (BGR Format)

```python
# Correct colors for most systems
RED    = 0x0000FF
GREEN  = 0x00FF00
BLUE   = 0xFF0000
YELLOW = 0x00FFFF  # Red + Green
CYAN   = 0xFFFF00  # Blue + Green
MAGENTA= 0xFF00FF  # Blue + Red
WHITE  = 0xFFFFFF
BLACK  = 0x000000
```

### Creating Colors Programmatically

In order to set the values programatically we use `bitshifting`.

```python
def create_trgb(t, r, g, b):
    """Create TRGB color (standard format)."""
    return (t << 24) | (r << 16) | (g << 8) | b

def create_bgr(b, g, r):
    """Create BGR color (what MLX actually uses)."""
    return (r << 16) | (g << 8) | b

# Example
red_color = create_bgr(0, 0, 255)  # BGR: Blue=0, Green=0, Red=255
```

### Extracting Color Components

We can also do the exact opposite and retrieve integer values from a encoded TRGB integer.

```python
def get_t(trgb):
    return ((trgb >> 24) & 0xFF)

def get_r(trgb):
    return ((trgb >> 16) & 0xFF)

def get_g(trgb):
    return ((trgb >> 8) & 0xFF)

def get_b(trgb):
    return (trgb & 0xFF)
```

---

## Drawing Functions

### `mlx_pixel_put(mlx_ptr, win_ptr, x, y, color)`

**Purpose**: Draws a single pixel.

**⚠️ WARNING**: The `mlx_pixel_put` function is very, very slow. This is because it tries to push the pixel instantly to the window (without waiting for the frame to be entirely rendered).

**Signature**:
```python
m.mlx_pixel_put(mlx_ptr, win_ptr, x, y, color)
```

**Example**:
```python
# Draw red pixel (using BGR format!)
m.mlx_pixel_put(mlx_ptr, win_ptr, 100, 50, 0x0000FF)
```

**Use case**: **Only for debugging or very simple graphics.** For anything else, use images!

---

### `mlx_string_put(mlx_ptr, win_ptr, x, y, color, string)`

**Purpose**: Draws text on the window.

**Signature**:
```python
m.mlx_string_put(mlx_ptr, win_ptr, x, y, color, string)
```

**Parameters**:
- `x`, `y`: Position (baseline of text)
- `color`: Text color in TRGB/BGR format
- `string`: Text to display

**Example**:
```python
m.mlx_string_put(mlx_ptr, win_ptr, 10, 20, 0xFFFFFF, "Hello World!")
```

---

## Image Manipulation (The Correct Way)

Because of this sole reason, we will have to buffer all of our pixels to a image, which we will then push to the window.

### Why Use Images?

1. **Performance**: 100-1000x faster than `mlx_pixel_put`
2. **No screen tearing**: Complete frames render at once
3. **Standard practice**: All MLX projects use images

### Creating an Image

#### `mlx_new_image(mlx_ptr, width, height)`

**Signature**:
```python
img_ptr = m.mlx_new_image(mlx_ptr, width, height)
```

**Example**:
```python
# Create 1920x1080 image buffer
img_ptr = m.mlx_new_image(mlx_ptr, 1920, 1080)
```

---

### Getting Image Data

#### `mlx_get_data_addr(img_ptr)`

We need to get the memory address on which we will mutate the bytes accordingly.

**Signature** (Python returns tuple):
```python
(addr, bits_per_pixel, line_length, endian) = m.mlx_get_data_addr(img_ptr)
```

**Returns**:
- `addr`: `memoryview` of the pixel data
- `bits_per_pixel`: Bits per pixel (usually 32)
- `line_length`: Bytes per line (may have padding!)
- `endian`: 0=little endian, 1=big endian

**Example**:
```python
img_ptr = m.mlx_new_image(mlx_ptr, 100, 100)
data, bpp, size_line, endian = m.mlx_get_data_addr(img_ptr)
```

---

### Understanding Image Memory Layout

The bytes are not aligned, this means that the `line_length` differs from the actual window width. We therefore should ALWAYS calculate the memory offset using the line length set by `mlx_get_data_addr`.

**Memory offset formula**:
```python
offset = y * line_length + x * (bits_per_pixel // 8)
```

**Pixel format** (little endian, typical):
```
Each pixel = 4 bytes in memory: [B, G, R, A]
- Byte 0: Blue
- Byte 1: Green  
- Byte 2: Red
- Byte 3: Alpha (usually ignored)
```

### Writing Pixels to Images

Now that we know where to write, it becomes very easy to write a function that will mimic the behaviour of `mlx_pixel_put` but will simply be many times faster.

```python
def my_mlx_pixel_put(data, x, y, color, line_length, bpp):
    """Fast pixel writing to image buffer."""
    if x >= 0 and y >= 0:  # Basic bounds checking
        offset = y * line_length + x * (bpp // 8)
        # Write color in BGR format
        data[offset] = color & 0xFF           # Blue
        data[offset + 1] = (color >> 8) & 0xFF    # Green
        data[offset + 2] = (color >> 16) & 0xFF   # Red
        data[offset + 3] = 0                       # Alpha
```

**Complete Example**:
```python
# Create image
img_ptr = m.mlx_new_image(mlx_ptr, 640, 480)
data, bpp, size_line, endian = m.mlx_get_data_addr(img_ptr)

# Draw pixels (fast!)
for y in range(480):
    for x in range(640):
        color = 0x0000FF  # Red in BGR
        my_mlx_pixel_put(data, x, y, color, size_line, bpp)

# Display the image
m.mlx_put_image_to_window(mlx_ptr, win_ptr, img_ptr, 0, 0)
```

---

### Displaying Images

#### `mlx_put_image_to_window(mlx_ptr, win_ptr, img_ptr, x, y)`

**Purpose**: Displays an image on the window.

**Parameters**:
- `x`, `y`: Position to place image's top-left corner

**Example**:
```python
# Display image at position (0, 0)
m.mlx_put_image_to_window(mlx_ptr, win_ptr, img_ptr, 0, 0)
```

---

### Loading Images from Files

#### `mlx_xpm_file_to_image(mlx_ptr, filename)`

**Returns** (tuple):
```python
(img_ptr, width, height) = m.mlx_xpm_file_to_image(mlx_ptr, "sprite.xpm")
```

#### `mlx_png_file_to_image(mlx_ptr, filename)`

**Returns** (tuple):
```python
(img_ptr, width, height) = m.mlx_png_file_to_image(mlx_ptr, "background.png")
```

**Example**:
```python
img_ptr, w, h = m.mlx_png_file_to_image(mlx_ptr, "player.png")
print(f"Loaded {w}x{h} image")
m.mlx_put_image_to_window(mlx_ptr, win_ptr, img_ptr, 100, 100)
```

---

### Destroying Images

#### `mlx_destroy_image(mlx_ptr, img_ptr)`

**Purpose**: Frees image memory.

**Example**:
```python
m.mlx_destroy_image(mlx_ptr, img_ptr)
```

**Important**: Always destroy images before exiting!

---

## Events & Hooks

Events are the foundation of writing interactive applications in MiniLibX. It is therefore of essence that you fully comprehend this chapter as this will be of use in your future graphical projects.

### X11 Event Types

Note: On MacOS - Cocoa (AppKit) and OpenGL - version, minilibx has partial support of X11 events and doesn't support X11 mask (x_mask argument of mlx_hook is useless, keep it at 0).

Common event codes:
```python
ON_KEYDOWN = 2     # Key press
ON_KEYUP = 3       # Key release
ON_MOUSEDOWN = 4   # Mouse button press
ON_MOUSEUP = 5     # Mouse button release
ON_MOUSEMOVE = 6   # Mouse movement
ON_EXPOSE = 12     # Window needs redraw
ON_DESTROY = 17    # Window destroy notify
```

---

### Keyboard Hooks

#### `mlx_key_hook(win_ptr, callback, param)`

**Purpose**: Hook into key events. This will trigger every time a key is pressed in a focused window. Unfocused windows will not register any key events.

**Callback signature**:
```python
def key_handler(keycode, param):
    # keycode: integer key code
    # param: user data passed to mlx_key_hook
    pass
```

**Example**:
```python
def handle_key(keycode, data):
    print(f"Key pressed: {keycode}")
    if keycode == 65307:  # ESC
        m.mlx_loop_exit(mlx_ptr)

m.mlx_key_hook(win_ptr, handle_key, None)
```

**Common keycodes**:
- ESC: 65307
- Space: 32
- Enter: 65293
- Arrow Left: 65361
- Arrow Up: 65362
- Arrow Right: 65363
- Arrow Down: 65364
- Letters a-z: 97-122
- Numbers 0-9: 48-57

---

### Mouse Hooks

#### `mlx_mouse_hook(win_ptr, callback, param)`

**Purpose**: Hook into mouse events. This will trigger every time you click somewhere in the given screen. Do mind that currently these mouse events barely work, it is therefore suggested to not use them.

**Callback signature**:
```python
def mouse_handler(button, x, y, param):
    # button: 1=left, 2=middle, 3=right, 4=scroll up, 5=scroll down
    # x, y: mouse coordinates
    # param: user data
    pass
```

**Example**:
```python
def handle_mouse(button, x, y, data):
    if button == 1:  # Left click
        print(f"Clicked at ({x}, {y})")

m.mlx_mouse_hook(win_ptr, handle_mouse, None)
```

**Note**: Mouse hooks have known issues. Use `mlx_hook` with event 4/5 for better reliability.

---

### General Hook System

#### `mlx_hook(win_ptr, event, mask, callback, param)`

Hooking into events is one of the most powerful tools that MiniLibX provides. It allows you to register to any of the aforementioned events with the call of a simple hook registration function.

**Signature**:
```python
m.mlx_hook(win_ptr, x_event, x_mask, callback, param)
```

**Parameters**:
- `x_event`: Event type code (2, 3, 4, 5, 6, 17, etc.)
- `x_mask`: Event mask (use 0 on macOS, may be ignored)
- `callback`: Function to call
- `param`: User data

**Callback signatures vary by event**:

```python
# Key events (2=press, 3=release)
def key_callback(keycode, param):
    pass

# Mouse button events (4=press, 5=release)  
def mouse_callback(button, x, y, param):
    pass

# Mouse motion (6)
def motion_callback(x, y, param):
    pass

# Window events (12, 17, etc.)
def window_callback(param):
    pass
```

**Examples**:

```python
# Window close button
def handle_close(param):
    m.mlx_loop_exit(mlx_ptr)

m.mlx_hook(win_ptr, 17, 0, handle_close, None)
```

```python
# Key press and release
def key_pressed(keycode, param):
    print(f"Key {keycode} down")

def key_released(keycode, param):
    print(f"Key {keycode} up")

m.mlx_hook(win_ptr, 2, 0, key_pressed, None)
m.mlx_hook(win_ptr, 3, 0, key_released, None)
```

```python
# Mouse movement tracking
def track_mouse(x, y, param):
    print(f"Mouse at ({x}, {y})")

m.mlx_hook(win_ptr, 6, 0, track_mouse, None)
```

---

### Loop Hook (Animation)

#### `mlx_loop_hook(mlx_ptr, callback, param)`

**Purpose**: Hook into each loop. This will trigger every frame.

**Callback signature**:
```python
def loop_handler(param):
    # Called continuously
    return 0  # Return value ignored
```

**Example - Animation**:
```python
x_pos = 0

def animate(param):
    global x_pos, img_ptr, data, size_line, bpp
    
    # Clear image
    for i in range(len(data)):
        data[i] = 0
    
    # Draw at new position
    for dy in range(10):
        for dx in range(10):
            my_mlx_pixel_put(data, x_pos + dx, 100 + dy, 0x0000FF, size_line, bpp)
    
    # Display
    m.mlx_put_image_to_window(mlx_ptr, win_ptr, img_ptr, 0, 0)
    
    # Update position
    x_pos = (x_pos + 1) % 640

m.mlx_loop_hook(mlx_ptr, animate, None)
```

**Warning**: This runs VERY frequently. Keep it fast!

---

### Expose Hook

#### `mlx_expose_hook(win_ptr, callback, param)`

**Purpose**: Called when window needs redrawing (uncovered, resized, etc.)

**Callback signature**:
```python
def redraw(param):
    # Redraw your graphics
    pass
```

**Example**:
```python
def redraw_window(param):
    m.mlx_put_image_to_window(mlx_ptr, win_ptr, img_ptr, 0, 0)

m.mlx_expose_hook(win_ptr, redraw_window, None)
```

---

## Event Loop

### `mlx_loop(mlx_ptr)`

**Purpose**: Starts the main event loop.

**Signature**:
```python
m.mlx_loop(mlx_ptr)
```

**Behavior**:
- Enters infinite loop
- Processes events continuously
- Calls registered hooks
- **NEVER returns normally**
- Only exits via `mlx_loop_exit()`

**Example**:
```python
# Setup everything first
m.mlx_key_hook(win_ptr, key_handler, None)
m.mlx_hook(win_ptr, 17, 0, close_handler, None)

# Start loop (blocks here forever)
m.mlx_loop(mlx_ptr)

# This line is never reached during normal operation
```

**Important**: You CANNOT use Ctrl+C to exit. Use Ctrl+\ or implement proper exit handling.

---

### `mlx_loop_exit(mlx_ptr)`

**Purpose**: Exits the event loop.

**Example**:
```python
def handle_esc(keycode, param):
    if keycode == 65307:
        m.mlx_loop_exit(mlx_ptr)
```

**What it does**:
- Stops event processing
- Cleans up internal resources
- Returns control after `mlx_loop()`

---

## Mouse Functions

### `mlx_mouse_hide(mlx_ptr)` / `mlx_mouse_show(mlx_ptr)`

Hide or show the mouse cursor.

```python
m.mlx_mouse_hide(mlx_ptr)  # Hide cursor
m.mlx_mouse_show(mlx_ptr)  # Show cursor
```

---

### `mlx_mouse_move(mlx_ptr, x, y)`

Move cursor to specified coordinates.

```python
m.mlx_mouse_move(mlx_ptr, 320, 240)  # Center of 640x480 window
```

---

### `mlx_mouse_get_pos(mlx_ptr)`

Get current mouse position.

**Returns** (tuple):
```python
(result, x, y) = m.mlx_mouse_get_pos(mlx_ptr)
print(f"Mouse at ({x}, {y})")
```

---

## Advanced Topics

### Screen Information

#### `mlx_get_screen_size(mlx_ptr)`

**Returns** (tuple):
```python
(result, width, height) = m.mlx_get_screen_size(mlx_ptr)
print(f"Screen: {width}x{height}")

# Create fullscreen window
win_ptr = m.mlx_new_window(mlx_ptr, width, height, "Fullscreen")
```

---

### Synchronization

#### `mlx_do_sync(mlx_ptr)`

Forces synchronization with graphics system.

```python
m.mlx_do_sync(mlx_ptr)
```

---

#### `mlx_sync(mlx_ptr, cmd, img_or_win_ptr)`

Advanced synchronization control.

**Commands**:
- `m.SYNC_IMAGE_WRITABLE` (1): Make image writable
- `m.SYNC_WIN_FLUSH` (2): Flush window updates
- `m.SYNC_WIN_COMPLETED` (3): Wait for completion

**Example**:
```python
m.mlx_sync(mlx_ptr, m.SYNC_WIN_FLUSH, win_ptr)
```

---

### Keyboard Autorepeat

#### `mlx_do_key_autorepeatoff(mlx_ptr)` / `mlx_do_key_autorepeaton(mlx_ptr)`

Disable/enable keyboard autorepeat.

```python
m.mlx_do_key_autorepeatoff(mlx_ptr)  # For precise key detection
# ... game logic ...
m.mlx_do_key_autorepeaton(mlx_ptr)   # Restore default
```

---

## Complete Examples

### Example 1: Interactive Drawing with Images

```python
#!/usr/bin/env python3
from mlx import Mlx

# Color constants (BGR format!)
RED = 0x0000FF
WHITE = 0xFFFFFF

m = Mlx()
mlx_ptr = m.mlx_init()
win_ptr = m.mlx_new_window(mlx_ptr, 800, 600, "Drawing App")

# Create image buffer
img_ptr = m.mlx_new_image(mlx_ptr, 800, 600)
data, bpp, size_line, endian = m.mlx_get_data_addr(img_ptr)

# Initialize to black
for i in range(len(data)):
    data[i] = 0

m.mlx_put_image_to_window(mlx_ptr, win_ptr, img_ptr, 0, 0)
m.mlx_string_put(mlx_ptr, win_ptr, 10, 20, WHITE, "Click and drag to draw")

def put_pixel(x, y, color):
    """Draw pixel in image buffer."""
    if 0 <= x < 800 and 0 <= y < 600:
        offset = y * size_line + x * 4
        data[offset] = color & 0xFF
        data[offset + 1] = (color >> 8) & 0xFF
        data[offset + 2] = (color >> 16) & 0xFF

# Track if mouse is pressed
mouse_down = False

def mouse_press(button, x, y, param):
    global mouse_down
    if button == 1:
        mouse_down = True
        # Draw 3x3 square
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                put_pixel(x + dx, y + dy, RED)
        m.mlx_put_image_to_window(mlx_ptr, win_ptr, img_ptr, 0, 0)

def mouse_release(button, x, y, param):
    global mouse_down
    if button == 1:
        mouse_down = False

def mouse_move(x, y, param):
    global mouse_down
    if mouse_down:
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                put_pixel(x + dx, y + dy, RED)
        m.mlx_put_image_to_window(mlx_ptr, win_ptr, img_ptr, 0, 0)

def key_press(keycode, param):
    if keycode == 65307:  # ESC
        m.mlx_destroy_image(mlx_ptr, img_ptr)
        m.mlx_loop_exit(mlx_ptr)
    elif keycode == 99:  # 'c' - clear
        for i in range(len(data)):
            data[i] = 0
        m.mlx_put_image_to_window(mlx_ptr, win_ptr, img_ptr, 0, 0)

def handle_close(param):
    m.mlx_destroy_image(mlx_ptr, img_ptr)
    m.mlx_loop_exit(mlx_ptr)

# Register hooks
m.mlx_hook(win_ptr, 4, 0, mouse_press, None)    # Mouse press
m.mlx_hook(win_ptr, 5, 0, mouse_release, None)  # Mouse release
m.mlx_hook(win_ptr, 6, 0, mouse_move, None)     # Mouse move
m.mlx_key_hook(win_ptr, key_press, None)
m.mlx_hook(win_ptr, 17, 0, handle_close, None)

m.mlx_loop(mlx_ptr)
```

---

### Example 2: Bouncing Ball Animation

```python
#!/usr/bin/env python3
from mlx import Mlx

RED = 0x0000FF

m = Mlx()
mlx_ptr = m.mlx_init()
win_ptr = m.mlx_new_window(mlx_ptr, 640, 480, "Bouncing Ball")

# Create image
img_ptr = m.mlx_new_image(mlx_ptr, 640, 480)
data, bpp, size_line, endian = m.mlx_get_data_addr(img_ptr)

# Ball state
ball_x = 320.0
ball_y = 240.0
ball_dx = 3.0
ball_dy = 2.5
ball_radius = 15

def put_pixel(x, y, color):
    if 0 <= x < 640 and 0 <= y < 480:
        offset = y * size_line + x * 4
        data[offset] = color & 0xFF
        data[offset + 1] = (color >> 8) & 0xFF
        data[offset + 2] = (color >> 16) & 0xFF

def draw_circle(cx, cy, radius, color):
    """Draw filled circle."""
    for y in range(int(cy - radius), int(cy + radius + 1)):
        for x in range(int(cx - radius), int(cx + radius + 1)):
            dx = x - cx
            dy = y - cy
            if dx*dx + dy*dy <= radius*radius:
                put_pixel(x, y, color)

def animate(param):
    global ball_x, ball_y, ball_dx, ball_dy
    
    # Clear screen (black)
    for i in range(len(data)):
        data[i] = 0
    
    # Update position
    ball_x += ball_dx
    ball_y += ball_dy
    
    # Bounce off walls
    if ball_x - ball_radius <= 0 or ball_x + ball_radius >= 640:
        ball_dx = -ball_dx
        ball_x = max(ball_radius, min(640 - ball_radius, ball_x))
    if ball_y - ball_radius <= 0 or ball_y + ball_radius >= 480:
        ball_dy = -ball_dy
        ball_y = max(ball_radius, min(480 - ball_radius, ball_y))
    
    # Draw ball
    draw_circle(int(ball_x), int(ball_y), ball_radius, RED)
    
    # Display
    m.mlx_put_image_to_window(mlx_ptr, win_ptr, img_ptr, 0, 0)

def key_press(keycode, param):
    if keycode == 65307:  # ESC
        m.mlx_destroy_image(mlx_ptr, img_ptr)
        m.mlx_loop_exit(mlx_ptr)

def handle_close(param):
    m.mlx_destroy_image(mlx_ptr, img_ptr)
    m.mlx_loop_exit(mlx_ptr)

m.mlx_loop_hook(mlx_ptr, animate, None)
m.mlx_key_hook(win_ptr, key_press, None)
m.mlx_hook(win_ptr, 17, 0, handle_close, None)

m.mlx_loop(mlx_ptr)
```

---

### Example 3: Keyboard-Controlled Character

```python
#!/usr/bin/env python3
from mlx import Mlx

RED = 0x0000FF
WHITE = 0xFFFFFF

m = Mlx()
mlx_ptr = m.mlx_init()
win_ptr = m.mlx_new_window(mlx_ptr, 640, 480, "WASD Controls")

# Create image
img_ptr = m.mlx_new_image(mlx_ptr, 640, 480)
data, bpp, size_line, endian = m.mlx_get_data_addr(img_ptr)

# Player state
player_x = 320
player_y = 240
player_size = 20

# Track pressed keys
keys_down = set()

def put_pixel(x, y, color):
    if 0 <= x < 640 and 0 <= y < 480:
        offset = y * size_line + x * 4
        data[offset] = color & 0xFF
        data[offset + 1] = (color >> 8) & 0xFF
        data[offset + 2] = (color >> 16) & 0xFF

def render():
    """Render the scene."""
    # Clear to black
    for i in range(len(data)):
        data[i] = 0
    
    # Draw player
    for dy in range(player_size):
        for dx in range(player_size):
            put_pixel(player_x + dx, player_y + dy, RED)
    
    # Display
    m.mlx_put_image_to_window(mlx_ptr, win_ptr, img_ptr, 0, 0)
    m.mlx_string_put(mlx_ptr, win_ptr, 10, 20, WHITE, "WASD to move, ESC to quit")

def key_press(keycode, param):
    keys_down.add(keycode)
    if keycode == 65307:  # ESC
        m.mlx_destroy_image(mlx_ptr, img_ptr)
        m.mlx_loop_exit(mlx_ptr)

def key_release(keycode, param):
    if keycode in keys_down:
        keys_down.remove(keycode)

def game_loop(param):
    global player_x, player_y
    
    speed = 3
    moved = False
    
    # WASD controls
    if 119 in keys_down or 65362 in keys_down:  # W or Up
        player_y -= speed
        moved = True
    if 115 in keys_down or 65364 in keys_down:  # S or Down
        player_y += speed
        moved = True
    if 97 in keys_down or 65361 in keys_down:   # A or Left
        player_x -= speed
        moved = True
    if 100 in keys_down or 65363 in keys_down:  # D or Right
        player_x += speed
        moved = True
    
    # Keep in bounds
    player_x = max(0, min(640 - player_size, player_x))
    player_y = max(0, min(480 - player_size, player_y))
    
    # Render if moved
    if moved or len(keys_down) > 0:
        render()

def handle_close(param):
    m.mlx_destroy_image(mlx_ptr, img_ptr)
    m.mlx_loop_exit(mlx_ptr)

# Initial render
render()

# Setup hooks
m.mlx_hook(win_ptr, 2, 0, key_press, None)      # Key press
m.mlx_hook(win_ptr, 3, 0, key_release, None)    # Key release
m.mlx_hook(win_ptr, 17, 0, handle_close, None)
m.mlx_loop_hook(mlx_ptr, game_loop, None)

m.mlx_loop(mlx_ptr)
```

---

### Example 4: Image Loader

```python
#!/usr/bin/env python3
from mlx import Mlx
import sys

if len(sys.argv) < 2:
    print("Usage: python image_viewer.py <image.png>")
    exit(1)

m = Mlx()
mlx_ptr = m.mlx_init()

# Load image
img_ptr, width, height = m.mlx_png_file_to_image(mlx_ptr, sys.argv[1])

if img_ptr is None:
    print(f"Failed to load {sys.argv[1]}")
    exit(1)

print(f"Loaded {width}x{height} image")

# Create window sized to image
win_ptr = m.mlx_new_window(mlx_ptr, width, height, f"Viewing: {sys.argv[1]}")

# Display image
m.mlx_put_image_to_window(mlx_ptr, win_ptr, img_ptr, 0, 0)

def key_press(keycode, param):
    if keycode == 65307:  # ESC
        m.mlx_destroy_image(mlx_ptr, img_ptr)
        m.mlx_loop_exit(mlx_ptr)

def handle_close(param):
    m.mlx_destroy_image(mlx_ptr, img_ptr)
    m.mlx_loop_exit(mlx_ptr)

m.mlx_key_hook(win_ptr, key_press, None)
m.mlx_hook(win_ptr, 17, 0, handle_close, None)

m.mlx_loop(mlx_ptr)
```

---

## Common Pitfalls & Solutions

### 1. Colors Showing Wrong (BGR vs RGB)

**Problem**: Your red pixels show up as blue.

**Solution**: Note that `0x00FF0000` is the hex representation of `ARGB(0,255,0,0)`. But MLX actually uses BGR format internally!

```python
# WRONG
RED = 0xFF0000  # This shows as BLUE!

# CORRECT  
RED = 0x0000FF  # This shows as red
```

### 2. `mlx_pixel_put` is Too Slow

**Problem**: Drawing is extremely slow.

**Solution**: The `mlx_pixel_put` function is very, very slow. This is because it tries to push the pixel instantly to the window. We will have to buffer all of our pixels to a image.

Use images instead!

### 3. Forgetting Line Length Alignment

**Problem**: Image rendering looks corrupted or offset.

**Solution**: The bytes are not aligned, this means that the `line_length` differs from the actual window width. We therefore should ALWAYS calculate the memory offset using the line length.

```python
# WRONG
offset = y * width * 4 + x * 4

# CORRECT
offset = y * line_length + x * (bpp // 8)
```

### 4. Calling `mlx_release()` Causes Segfault

**Problem**: Program crashes when calling `mlx_release()`.

**Solution**: `mlx_loop_exit()` already cleans up resources. Don't call `mlx_release()` after it!

```python
# WRONG
def handle_close(param):
    m.mlx_loop_exit(mlx_ptr)

# ... later in main ...
m.mlx_loop(mlx_ptr)
m.mlx_release(mlx_ptr)  # SEGFAULT!

# CORRECT
def handle_close(param):
    m.mlx_loop_exit(mlx_ptr)
    # That's it - no mlx_release needed!
```

### 5. Window Not Responding

**Problem**: Window appears but nothing draws or events don't work.

**Solution**: Make sure you called `mlx_loop()`:

```python
# Setup
win_ptr = m.mlx_new_window(mlx_ptr, 640, 480, "Title")
m.mlx_key_hook(win_ptr, key_handler, None)

# MUST CALL THIS
m.mlx_loop(mlx_ptr)
```

### 6. Can't Exit with Ctrl+C

**Problem**: Ctrl+C doesn't close the program.

**Solution**: This is normal MLX behavior. Use Ctrl+\ or implement proper exit handling:

```python
def key_press(keycode, param):
    if keycode == 65307:  # ESC
        m.mlx_loop_exit(mlx_ptr)

m.mlx_key_hook(win_ptr, key_press, None)
```

### 7. Screen Tearing When Drawing

**Problem**: Flickering or tearing during animation.

**Solution**: Use double buffering - draw to image, then display complete frame:

```python
def animate(param):
    # Draw everything to image buffer
    for i in range(len(data)):
        data[i] = 0  # Clear
    # ... draw all objects ...
    
    # Display complete frame
    m.mlx_put_image_to_window(mlx_ptr, win_ptr, img_ptr, 0, 0)
```

### 8. Mouse Events Not Working

**Problem**: Do mind that currently these mouse events barely work, it is therefore suggested to not use them.

**Solution**: Use `mlx_hook` instead of `mlx_mouse_hook`:

```python
# Instead of mlx_mouse_hook, use:
m.mlx_hook(win_ptr, 4, 0, mouse_press, None)    # Button press
m.mlx_hook(win_ptr, 5, 0, mouse_release, None)  # Button release
m.mlx_hook(win_ptr, 6, 0, mouse_move, None)     # Motion
```

---

## Best Practices Summary

1. **Always use images for rendering** - Never use `mlx_pixel_put` for production code
2. **Use BGR color format** - Remember colors are BGR, not RGB!
3. **Use `line_length` for offset calculations** - Don't assume width * 4
4. **Handle window close properly** - Use `mlx_hook(win_ptr, 17, 0, ...)`
5. **Keep loop hooks fast** - `mlx_loop_hook` runs very frequently
6. **Clean up resources** - Destroy images before exiting
7. **Don't call `mlx_release`** - `mlx_loop_exit` handles cleanup
8. **Use `mlx_hook` for reliable events** - More reliable than specific hook functions
9. **Initialize to black** - Always clear image buffers after creation
10. **Test keycodes** - Print keycode values to find the keys you need

---

## Resources

- **Official 42 Documentation**: https://harm-smits.github.io/42docs/libs/minilibx
- **MLX Man Pages**: Check `/mnt/skills/public/` for detailed man pages
- **XPM/PNG Examples**: Use image files for sprites and textures
- **Color Picker**: Google "color picker" to find hex values

---

## Conclusion

MLX for Python provides a simple but powerful interface for 2D graphics. The key to success is:

1. Understanding the event-driven architecture
2. Using images instead of direct pixel drawing
3. Remembering the BGR color format
4. Properly handling events and cleanup

With these fundamentals, you can create games, visualizations, and interactive applications efficiently!

Happy coding with MLX! 🎨
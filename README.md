*This project has been created as part of the 42 curriculum by mmeurer, ebabun.*

# A-maze-ing
**A-maze-ing** is a maze generator, maze solver and maze rendering project.  
The purpose of the program is to generate mazes and display them either in ASCII or using a graphical interface (MinilibX).

  ## Table of Contents

  - [A-maze-ing : Description](#a-maze-ing--description)
  - [Configuration file](#configuration-file)
    - [Configuration File settings](#configuration-file-settings)
      - [Configuration tips](#configuration-tips)
      - [Example](#example-of-configuration-file)
  - [Instructions](#instructions)
    - [1. Create a virtual environement and install
  dependencies](#1-create-a-virtual-environement-and-install-dependencies)
    - [2. Edit the config file](#2-edit-the-config-file)
    - [3. Run the program](#3-run-the-program)
  - [Team and Project Management](#team-and-project-management)
    - [Team Roles](#team-roles)
    - [Planning and Evolution](#planning-and-evolution)
    - [What worked well](#what-worked-well)
    - [What could be improved](#what-could-be-improved)
    - [Tools used](#tools-used)
    - [AI Usage](#ai-usage)
  - [Program Features](#program-features)
    - [Features summary](#features-summary)
    - [Parsing](#parsing)
    - [Maze generation algorithms](#maze-generation-algorithms)
      - [The DFS Algorithm](#the-dfs-algorithm)
      - [Wilson's Algorithm](#wilsons-algorithm)
    - [Maze resolution algorythm](#maze-resolution-algorythm)
      - [Breadth-First Search (BFS)](#breadth-first-search-bfs)
      - [How does BFS garantee the shortest
  path](#how-does-bfs-garantee-the-shortest-path)
    - [Rendering](#rendering)
      - [ASCII Renderer](#ascii-renderer)
      - [MinilibX Renderer](#minilibx-renderer)
  - [Hexadecimal Output Format](#hexadecimal-output-format)
    - [The cell and walls representation](#the-cell-and-walls-representation)
    - [The solution path representation](#the-solution-path-representation)
    - [The file structure](#the-file-structure)
  - [Reusable Code](#reusable-code)
    - [Package contents](#package-contents)
    - [Building the package](#building-the-package)
    - [Installation](#installation)
    - [Example usage](#example-usage)
  - [Resources](#resources)

<br/>

# Configuration file

The program takes a configuration file as argument (optional).\
If no configuration file is provided, the default settings are applied.

## Configuration File settings

| Parameter | Description | Default | Valid Options/Range | Example |
|-----------|-------------|---------|---------------------|---------|
| WIDTH | Width of the maze | `20` | Integer between 2 and 350 | `WIDTH=42` |
| HEIGHT | Height of the maze | `10` | Integer between 2 and 200 | `HEIGHT=42` |
| ENTRY | Maze entry coordinates | `(0, 0)` | `x,y` within maze bounds | `ENTRY=1,1` |
| EXIT | Maze exit coordinates | `(width - 1, height - 1)` | `x,y` within maze bounds | `EXIT=40,41` |
| PERFECT | Perfect or imperfect maze | `True` | `True`/`False`, `1`/`0`, `Yes`/`No`, `Y`/`N` | `PERFECT=False` |
| SEED | Seed for reproducibility | `None` | `None` or any integer | `SEED=None` |
| OUTPUT_FILE | Path for output file | `maze.txt` | Any valid file path | `OUTPUT_FILE=maze.txt` |
| ALGORITHM | Maze generation algorithm | `wilson` | `dfs`, `wilson` | `ALGORITHM=wilson` |
| DISPLAY | Display mode | `None` | `None`, `ascii`, `mlx` | `DISPLAY=mlx` |

#### Configuration tips

- **File Location**: Place the config file at the root of the project
- **Format**: Use `KEY=value` format (standard configuration file syntax)
- All parameters are optional and will use default values if not specified
- **PERFECT:** A perfect maze will have exactly one path between any two points (no loops, no isolated areas).
- **SEED:** using the same integer value will always produce the same maze

#### Example of Configuration file

```ini
# A-maze-ing Configuration File
# Place the config file at the root of the project

WIDTH=40
HEIGHT=20
ENTRY=1,1
EXIT=37,17
PERFECT=False
SEED=None
OUTPUT_FILE=my_imperfect_maze.txt
ALGORITHM=dfs
DISPLAY=ascii
```

<br/>  
<br/>  

# Instructions

Note: python3.10 or above is required for the program to run

To see all available commands of the Makefile use:
```bash
make help
```

### 1. Create a virtual environement and install dependencies
```bash
make install
```
This will create a virtual environement and install the following dependencies:
- flake8 and flake8-docstrings (linter standard)
- mypy (static type checking)
- pytest (testing module)
- build (packaging tool)

### 2. Edit the config file

Edit the [Configuration file](#configuration-file) to customize the program settings.

**Note :** By default the file name used for execution is `config.txt` but this name can be changed. (See section bellow)

### 3. Run the program

The program can be executed with the following commands:

- Run the program with a configuration file named config.txt:
```bash
$ make run
```

- Run the program with another configuration file name:
```bash
$ make run CONFIG=file.txt
```

- Run the program without configuration file (using the default settings):
```bash
$ make default
```

<br/>
<br/>


# Team and Project Management

### Team Roles
| Member | Responsibilities |
|--------|-----------------|
| Esther (ebabun) | Parsing system, DFS algorithm, MinilibX renderer |
| Morgane (mmeurer) | Wilson's algorithm, BFS solver, ASCII renderer |

Both team members collaborated on:
- Core architecture (Cell and MazeGenerator classes)
- Code review and testing
- Documentation

## Planning and Evolution
**Conception plan:**
1. Week 1: 
   - Establish parsing system
   - Define core classes (Cell, MazeGenerator)
   - Implement generation algorithms (DFS and Wilson's)

2. Week 2: 
   - Implement method to create imperfect mazes
   - Implement BFS solver
   - Create the Ascii and MLX renderers

3. Week 3: 
   - Perfect the protection system and error handling
   - Adapt to flake8 linter standard and static type checking
   - package preparation
   - documentation


How it evolved:
- (week2) The initial make_imperfect() method was flawed and had to be improved
- (week2) A circular import between MazeGenerator and Cell was removed, migrating all maze related methods in Cell back to MazeGenerator.
- (week2) Added a navigation feature to the MlxRenderer class
- (week3) The parsing system was refactored into a `MazeParser` class for better separation of concerns (SRP)
- (week3) Added the abstract `MazeRenderer` base class to share common functionality between renderers

### What worked well
- Strong communication: open dialogue about implementation approaches, design decisions, and technical challenges
- Collaborative mindset: mutual adaptability to each other's working styles and willingness to learn together
- Clear separation of responsibilities enabled efficient parallel development
- Consistent code quality through regular code reviews and constructive feedback

### What could be improved
- The architecture could have been made more modular from the start,\
allowing for easier testing of individual components
- Continuous enforcement of linting and type-checking standards,\
rather than deferring these checks to the end of development
- Our initial Git workflow wasn't optimized for collaborative merging, requiring time-consuming manual merges at each integration point (but this experience improved our understanding of branching)

### Tools used
- **Version control:** Git/Github with feature branches
- **Code quality:** flake8 (linting), mypy (type checking)
- **MinilibX for python:** graphic library  
- **IDE:** Visual Studio Code
- **Communication:** Discord for daily coordination

### AI Usage
Claude (Sonnet 4.5) and ChatGPT (5.2) were used to assist with:
- Learning about maze generation algorithms
- Learning about python best practices and circular dependencies
- Understanding MinilibX library usage patterns
- Learning how to create a python package
- Generating docstrings and documentation drafts for the entire project
- Fixing a few intricated type checking issues

All AI-generated content was reviewed, tested, and modified to ensure correctness and understanding.

<br/>
<br/>

# Program Features

## Features summary
- Parsing with automatic fallback to default settings
- Maze generation using:
  - Depth-First Search (DFS)
  - Wilson’s algorithm
- Maze solving using Breadth-First Search (BFS)
- Two rendering modes for the display:
  - ASCII display
  - MinilibX graphical display
- user interactions:
  - Re-generate a new maze
  - Show or hide the solution path
  - Change wall colors
  - Navigate in the maze (MinilibX only)
  - Quit the program
<br/>

## Parsing
*Implemented by Esther Babun*

The parsing system uses the `MazeParser` class (`mazegen/maze_parser.py`) to handle configuration reading and settings validation.

**Default values:**
| Key | Default Value | Constraints |
|-----|--------------|-------------|
| WIDTH | 20 | 2 - 350 |
| HEIGHT | 10 | 2 - 200 |
| ENTRY | (0, 0) | Must be within maze bounds |
| EXIT | (width-1, height-1) | Must be within maze bounds |
| PERFECT | True | True/False, 1/0, Yes/No, Y/N |
| SEED | None | Any integer or None |
| OUTPUT_FILE | maze.txt | Valid file path |
| ALGORITHM | wilson | dfs or wilson |
| DISPLAY | None | None, ascii, or mlx |

<br/>

**Validation features:**
- Automatic fallback to default values for invalid or missing settings
- Entry/exit coordinates are validated against maze bounds
- Entry/exit coordinates are checked against the "42" pattern to avoid conflicts
- File paths are validated for existence and read/write permissions
- Size constraints are enforced:
  - max size for generation: 350x200
  - max size for display: 320x150

**Note:** The max sizes were enforced as performance safeguards to avoid excessive generation times and system freezes during rendering.

<br/>

## Maze generation algorithms

### The DFS Algorithm

*Implemented by Esther Babun*

[Depth-First Search (DFS)](https://en.wikipedia.org/wiki/Depth-first_search) was chosen for its simplicity and the visually pleasing, long, winding corridors it produces.

![DFS algo](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*unQanD3lFwpajj6lsJVw8g.gif)

**How it works:**
1. Start from the entry cell and mark it as visited.
2. Push the current cell onto a stack.
3. Choose a random unvisited neighbor and carve a passage to it.
4. If no unvisited neighbors exist, backtrack by popping from the stack.
5. Repeat until all cells are visited.

**Characteristics:**
- Creates mazes with long corridors and fewer dead ends
- Uses an iterative approach with an explicit stack to avoid recursion limits
- Produces a "biased" maze structure (unlike Wilson's uniform distribution)

**Note :** why biased ? Because the first path carved is typically very long, creating a main "river" that subsequent branches connect to. The dead-ends tend to accumulate near edges and corners because of the backtracking logic. Therefore, the possible maze structures are more limited than with Wilson's algorithm, giving the maze a more predictable feel, easier to solve (follow the main corridor).

<br/>

### Wilson’s Algorithm

*Implemented by Morgane Meurer*

[Wilson’s algorithm](https://medium.com/@batbat.senturk/the-ultimate-unbiased-maze-generation-technique-you-need-to-see-46123d5fec76) was chosen for its elegant approach and the high quality of the generated mazes (also… the gif convinced us).

![Wilson's algo](https://miro.medium.com/v2/resize:fit:640/format:webp/1*Ewed2CKIK6oLAKDfo21DFg.gif)

**How it works:**
1. Mark the entry cell as part of the maze (as visited).
2. Pick a random unvisited cell and begin a random walk form that cell.
3. At each step, move to a random neighbor\
adding it to the path and recording the direction taken.\
If the walk crosses its own trail, erase the loop\
form the path (loop-erased random walk).
4. When the walk reaches any cell already in the maze, stop.
5. Carve passages along the entire loop-erased path,\
adding all those cells to the maze.
6. Repeat steps 2-5 until all cells are part of the maze.

**Characteristics:**
- Unbiased: Every possible maze has equal probability
  of being generated
- No directional texture: No visible "flow" or pattern
in the structure
- Varied corridor lengths: Mix of short and long
passages (unlike DFS's long corridors)
- Evenly distributed dead ends: No clustering in
corners or edges
- Higher perceived difficulty: More unpredictable,
harder to solve by intuition


<br/>

## Maze resolution algorythm

*Implemented by Morgane Meurer*

### Breadth-First Search (BFS)
BFS was chosen for its simplicity and its ability to guarantee the shortest solution path in a maze. Plus, several methods of MazeGenerator were reused, avoiding redundancy and simplifying the code.

**How it works:**
- Start from the entry cell and add it to a queue (implemented using a **deque** chosen for its efficient removal of the first element).
- Explore all unvisited neighbors level by level (FIFO).
- Store each visited cell’s parent in a dictionary.
- Stop when the exit is reached or when all reachable cells are explored.
- Reconstruct the shortest path by backtracking from the exit to the start.

<br/>

### How does BFS garantee the shortest path

BFS explores level by level (all cells at distance N before any cell at
  distance N+1).

  Visual Proof

  Distance from Entry:

      0   1   2   3
    +---+---+---+---+
    | 0 | 1 | 2 | 3 |   BFS explores in this order:
    +---+---+---+---+   - First all cells at distance 0 (entry)
    | 1 | 2 | 3 | 4 |   - Then all cells at distance 1
    +---+---+---+---+   - Then all cells at distance 2
    | 2 | 3 | 4 | X |   - etc.
    +---+---+---+---+

  Why It Works

  Key insight: The first time BFS reaches any cell, it's via the shortest path.

  1. BFS uses a FIFO queue (First In, First Out)
  2. Cells discovered at distance N are added to the queue before cells at distance
  N+1
  3. Therefore cells at distance N are processed before cells at distance N+1
  4. When we first reach the exit, we've taken exactly N steps, and no shorter path
  exists (we would have found it earlier)

<br/>

## Rendering

**Note:** AsciiRenderer and MlxRenderer are child classes of the MazeRenderer abstract base class.

### ASCII Renderer
*Implemented by Morgane Meurer*

The maze can be rendered directly in the terminal using ASCII characters.

**Features:**
- Display walls, paths, entry (green square), exit (red square),\
and the solution path (optional) on the terminal.
- Supports multiple wall colors with [ANSI codes](https://talyian.github.io/ansicolors/).
- Interactive menu to:
  1. Re-generate a new maze
  2. Show or hide the solution path
  3. Rotate wall colors
  4. Quit the program

**How it works:**
1. The terminal is cleared and the cursor is placed at the top-left corner to give the impression that each new maze is displayed in a fresh window.
2. The maze is printed:
   - On the first iteration, the solution path is hidden and the walls are displayed in white by default.
   - Each cell is rendered according to its content:
     - Entry
     - Exit
     - Solution path (if enabled)
     - 42 block cells (`■`)
     - All other cells are left empty.
   - The maze is drawn line by line using the hexadecimal representation from the `MazeGenerator` class, with each cell’s content centered.
3. The user is prompted for input:
   - If an invalid choice is entered, a message is displayed and the prompt repeats until a valid choice is made.
   - Once a valid choice is entered, step 1 is repeated, updating the display accordingly.

**Note :** On first display or after re-generating, the maze configuration and any error messages are printed outside the frame of the window, above the maze representation, to provide a more pleasant “fresh window” experience to the user. To view these messages the user can scroll up in the terminal.

<br/>


### MinilibX Renderer

*Implemented by Esther Babun*

**Features:**
- Dynamic cell sizing based on screen resolution
- Color palette cycling (green, cyan, pink, orange, red)
- Interactive navigation using arrow keys
- Solution path toggle
- maze re-generation

**How it works:**
1. Calculate optimal cell size based on screen dimensions and maze size.
2. Create a window with enough space for the maze image and the command instructions.
3. Draw each cell with appropriate colors for walls, paths, and special markers (entry/exit).
4. Handle keyboard events for user interactions:
   - `Arrow keys`: Navigate through the maze
   - `s`: Show/hide solution path
   - `c`: Cycle through color palettes
   - `d`: Delete navigation path
   - `r`: Regenerate a new maze
   - `q`: Quit the program

**Technical details:**
- Uses direct pixel manipulation for fast rendering
- Walls are drawn with configurable thickness proportional to cell size
- Entry point is marked in cyan, exit in yellow
- Navigation path can be deleted
- The color changes apply to the walls and the solution path


<br/>
<br/>


# Hexadecimal Output Format

The program produces an output file with the maze encoded in hexadecimal format.

## The cell and walls representation
the maze is represented using one hex digit per cell:

```
Bit 0 (LSB): North wall
Bit 1: East wall
Bit 2: South wall
Bit 3: West wall
```

**Examples:**
- `0` (0000) = all walls removed
- `F` (1111) = all walls intact
- `3` (0011) = North and East walls only
- `A` (1010) = East and West walls only

## The solution path representation
the solution path is a string with the series of directions taken form entry to exit (W,S,E,N)


**Example:**
```
SSWSSENENNESSSENNEENWWNWWNEEEEESENEEEEEEEEEEESSESWWWSSE
```

## The file structure
```
[Hex row]
[Hex row]
[Hex row]

entry_x,entry_y
exit_x,exit_y
SOLUTION_PATH_AS_DIRECTIONS
```

**Note:** the entry coordinates are separated from the hexadecimal rows by an empty line.

<br/>
<br/>

# Reusable Code

The maze generation logic is packaged as a standalone module (`mazegen`) that can be installed and imported in other projects.

## Package contents
- `Cell`: Class representing a single cell in the maze grid
- `MazeGenerator`: Main class for maze generation and solving
- `OFFSET`: Direction offset dictionary for navigation

## Building the package
To build the package run:
```bash
$ make build
```
This will:
1. Use `venv/bin/python3 -m build` to generate the package
2. Move the output files to the project root
3. Clean up temporary build artifacts

Two files are generated:
- mazegen-1.0.0-py3-none-any.whl (wheel - recommended for installation)
- mazegen-1.0.0.tar.gz (source distribution)

**About the tarball**: A .tar.gz file is a compressed archive containing the raw source code.\
**Note:** For local installation, prefer the `.whl` file - it's pre-built and installs faster.

## Installation
```bash
(venv)$ pip install mazegen-1.0.0-py3-none-any.whl
```

## Example usage
```python
from mazegen import MazeGenerator

# Create a maze passing the config file as argument
maze = MazeGenerator("config.txt")

# Access maze properties
print(f"Size: {maze.cols}x{maze.rows}")
print(f"Entry: {maze.entry}, Exit: {maze.exit}")
print(f"Solution: {maze.path}")

# Access the grid structure
for row in maze.grid:
    for cell in row:
        print(f"Cell ({cell.coord}) walls: {cell.walls}")
```

For detailed documentation, see `mazegen_info/README.md`.

<br/>
<br/>

# Resources

  Maze Algorithms

  - **Wikipedia - Maze Generation Algorithm**\
    https://en.wikipedia.org/wiki/Maze_generation_algorithm\
    *Overview of all major algorithms (DFS, Prim's, Kruskal's, Wilson's)*
  - **Think Labyrinth - Maze Algorithms**\
    http://www.astrolog.org/labyrnth/algrithm.htm\
    *Comprehensive reference on maze algorithms and their properties*
  - **batuSenturk - Maze generation and solving reference**  
  https://github.com/batuSenturk/Mazes
  - **Medium - Wilson’s algorithm article**\
    https://medium.com/@batbat.senturk/the-ultimate-unbiased-maze-generation-technique-you-need-to-see-46123d5fec76
  - **Wikipedia - Random Walk** (Wilson's algorithm foundation)\
    https://en.wikipedia.org/wiki/Random_walk\
  - **Wikipedia - Depth-First Search**\
    https://en.wikipedia.org/wiki/Depth-first_search\
  - **Wikipedia - Breadth-First Search (solver algorithm)**\
    https://en.wikipedia.org/wiki/Breadth-first_search\
  - **GeeksforGeeks - BFS for Shortest Path in Unweighted Graph**\
    https://www.geeksforgeeks.org/shortest-path-unweighted-graph/

  MinilibX documentation
  - **Harm Smits - documentation on MLX**\
    https://harm-smits.github.io/42docs/libs/minilibx/getting_started.html

  Python Language

  - **Python.org - typing module**\
    https://docs.python.org/3/library/typing.html
  - **PEP 257 - Docstring Conventions**\
    https://peps.python.org/pep-0257/
  - ***Python.org - collections.deque (used for BFS)**\
    https://docs.python.org/3/library/collections.html#collections.deque
  - **GeeksForGeeks - Deque in Python**\
    https://www.geeksforgeeks.org/python/deque-in-python/

  Python Packaging
  - **Python.org - Packaging User Guide**\
    https://packaging.python.org/en/latest/
  - **Python.org - writing a pyproject.toml**\
    https://packaging.python.org/en/latest/guides/writing-pyproject-toml/
  - **Medium - Building Python Packages**\
    https://medium.com/@ebimsv/building-python-packages-07fbfbb959a9\
    *Usefull ressource on the difference between setup.py and pyproject.toml*
  - **PEP 517 - Build System Interface**\
    https://peps.python.org/pep-0518/
  - **Setuptools Documentation**\
    https://setuptools.pypa.io/en/latest/userguide/quickstart.html


  Code Quality

  - **Flake8 Documentation**\
  https://flake8.pycqa.org/en/latest/
  - **Mypyp documentation**\
  https://mypy.readthedocs.io/en/stable/getting_started.html
  - **Pytest Documentation**\
  https://docs.pytest.org/en/stable/

  Other
  - **Keyboard keys reference**\
  https://www.cl.cam.ac.uk/~mgk25/ucs/keysymdef.h
  - **ANSI color codes**\
  https://talyian.github.io/ansicolors/
  - **ANSI Escape Codes (Wikipedia)**\
  https://en.wikipedia.org/wiki/ANSI_escape_code
  - **Terminal visual sequences**\  
  https://learn.microsoft.com/fr-fr/windows/console/console-virtual-terminal-sequences

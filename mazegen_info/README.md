
*Created by ebabun and mmeurer as part of the 42 School curriculum.*

# mazegen

A Python library for generating and solving mazes.

## About this package

This package creates random mazes using different algorithms (Wilson's algorithm or DFS) and finds the shortest path from entry to exit.

## Package contents
- `Cell`: Class representing a single cell in the maze grid
- `MazeGenerator`: Main class for maze generation and solving
- `OFFSET`: Direction offset dictionary
<br/>
<br/>

## Installation
```bash
$ pip install mazegen-1.0.0-py3-none-any.whl
```
<br/>

## Configuration file

The MazeGenerator class of the module takes a configuration file as argument (optional).\
**Note:** If no configuration file is provided, the default settings are applied.

### Configuration settings

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

**Note:** the DISPLAY setting exists but should always be absent from the config file or set to None since the mazegen module doesn't include any rendering features.

### Configuration file example

Create a config file:
```ini
WIDTH=30
HEIGHT=20
ENTRY=0,0
EXIT=29,19
PERFECT=True
SEED=None
ALGORITHM=dfs
OUTPUT_FILE=my_maze.txt
```
<br/>

## Basic Usage

### Generate a maze with default settings
```python
from mazegen import MazeGenerator

# Create a 20x10 maze (default size)
maze = MazeGenerator()
```

### Generate a maze from a configuration file

Pass the name of the config file as argument to use the defined settings.
```python
from mazegen import MazeGenerator

# Use a config file to customize your maze
maze = MazeGenerator("your_config.txt")
```

Note: As soon as you instanciate a MazeGenerator object, an output file containing the hexadecimal structure of the maze will be generated (see the section dedicated to the [output format](#-hexadecimal-output-format))

### Access the maze attributes

After creating a maze, you can access:

- `maze.cols` - Width of the maze
- `maze.rows` - Height of the maze
- `maze.entry` - Entry coordinates (x, y)
- `maze.exit` - Exit coordinates (x, y)
- `maze.grid` - 2D array of Cell objects
- `maze.hex_repr` - Hexadecimal representation of the maze
- `maze.get_cell(x, y)` - Get a specific cell
- `maze.path` - Shortest solution path as a string of directions (N/S/E/W)

Example:

```python
print(f"Maze size: {maze.cols}x{maze.rows}")
print(f"Entry point: {maze.entry}")
print(f"Exit point: {maze.exit}")
print(f"Solution path: {maze.path}")
```

### Access the cell objects and cell attributes
```python
# Get a cell at position (5, 5)
cell = maze.get_cell(5, 5)

if cell:
    print(f"Cell coordinates: {cell.coord}")
    print(f"Cell walls: {cell.walls}")
    print(f"Hex representation: {cell.hex_repr}")

# Get all cells of the maze
for row in maze.grid:
    for cell in row:
        print(f"Cell ({cell.coord}) walls: {cell.walls}")
```

### Check if a cell is part of the "42" pattern

 The center of the maze contains a "42" pattern made of blocked cells.

 ```python
 cell = maze.get_cell(10, 5)
 if cell and cell.is_42:
     print("This cell is part of the 42 pattern")
 ```


### Using OFFSET to follow the solution path

The `OFFSET` dictionary maps directions to coordinate differences.

```python
from mazegen import MazeGenerator, OFFSET

# OFFSET = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "W": (-1, 0)}

maze = MazeGenerator()

# Follow the solution path step by step
x, y = maze.entry
print(f"Start: ({x}, {y})")

for direction in maze.path:
    dx, dy = OFFSET[direction]
    x, y = x + dx, y + dy
    print(f"Move {direction} -> ({x}, {y})")

print(f"Reached exit: {(x, y) == maze.exit}")
 ```

### Wall Encoding Explanation

  Each cell's walls are stored as a dictionary and can be represented as a hex digit:

  ```python
  cell.walls = {"W": 1, "S": 0, "E": 1, "N": 0}
  #              │     │     │     └── North: open
  #              │     │     └──────── East: wall
  #              │     └────────────── South: open
  #              └──────────────────── West: wall

  # Binary: 1010 = 0xA
  print(cell.hex_repr)  # "A"
  ┌─────┬────────┬────────────────────┐
  │ Hex │ Binary │    Walls (WSEN)    │
  ├─────┼────────┼────────────────────┤
  │ 0   │ 0000   │ All open           │
  ├─────┼────────┼────────────────────┤
  │ 5   │ 0101   │ West + East only   │
  ├─────┼────────┼────────────────────┤
  │ A   │ 1010   │ South + North only │
  ├─────┼────────┼────────────────────┤
  │ F   │ 1111   │ All closed         │
  └─────┴────────┴────────────────────┘
```

<br/>

## Further help on the modules and methods

To access modules and methods inner documentation.

- use the help() function.

Example:

```python
>>> from mazegen import MazeGenerator, Cell, OFFSET

# help for an entire class
>>> help(MazeGenerator)

# help for a specific method
>>> help(MazeGenerator.export_to_txt)
```

- use the \__doc__ attribute.

Example:
```python
>>> from mazegen import MazeGenerator, Cell, OFFSET

# short documentation of a class
>>> print(MazeGenerator.__doc__)

# short documentation of a method
>>> print(MazeGenerator.export_to_txt.__doc__)
```

<br/>

## Hexadecimal Output Format

The MazeGenerator instanciation produces an output file with the maze encoded in hexadecimal format.

### The maze representation
the maze is represented using one hex digit per cell.

Example:

```
95155553955555555553B95539515553
ABC5153C6915553D553AC297AC3C553A
EA93C52D56C53969556C3AA943AD396E
96AA956955556C3C39556C6A96C3AC53
A96AA956B95553A92AD15396C53AA952
C6BC6A93AAD1786AEC56BAC553EAAA96
950792AAC452FC52FFF96C553A96AAC7
ABC56C6C553EFD5057FA95556AAD2C53
C43D515557C3FFFAFFF8451156A9057A
95455695393A93FAFD52D16E93C6A93A
C57953A96A86AAFEFFFC3C396C156AC2
9556D46C3AE96C513957C3AA93AB96BA
8539553D2A945796A8513A86AAC6AB86
C3C69543C2A955696C7AAAA96C53AAC3
BAD5413A96AC3D54553AAAEA953AA852
AA9396AAC7C3A93D5546AC56C3C6A83A
C46C6D6C5556C6C55555455554556EC6
```

### The solution path representation
the solution path is a string with the series of directions taken form entry to exit (W,S,E,N)

example:
```
SSWSSENENNESSSENNEENWWNWWNEEEEESENEEEEEEEEEEESSESWWWSSE
```

### The file structure
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

## Additional Metadata
### Requirements

- Python 3.10 or higher

### Authors

- Morgane Meurer
- Esther Babun

### License

MIT License - See LICENSE file for details.

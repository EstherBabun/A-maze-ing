
*Created by ebabun and mmeurer as part of the 42 School curriculum.*

# mazegen

A Python library for generating and solving mazes.

## About this package

This package creates random mazes using different algorithms (Wilson's algorithm or DFS) and finds the shortest path from entry to exit.
<br/>
<br/>
<br/>
<br/>

# Installation
```bash
$ pip install mazegen-1.0.0-py3-none-any.whl
```
<br/>
<br/>

# Configuration

The MazeGenerator class of the mazegen module takes a configuration file as argument (optional).\
**Note:** If no configuration file is provided, the default settings are applied.

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
<br/>

# Basic Usage




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
```
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

# Additional Metadata
## Requirements

- Python 3.10 or higher

## Authors

- Morgane Meurer
- Esther Babun

## License

MIT License - See LICENSE file for details.


*Created by ebabun and mmeurer as part of the 42 School curriculum.*

# mazegen

A Python library for generating and solving mazes.

## What does it do?

This package creates random mazes using different algorithms (Wilson's algorithm or DFS) and can find the shortest path from entry to exit.

## Installation
```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

## Basic Usage

### Generate a maze with default settings
```python
from mazegen import MazeGenerator

# Create a 20x10 maze (default size)
maze = MazeGenerator()

print(f"Maze size: {maze.cols}x{maze.rows}")
print(f"Entry point: {maze.entry}")
print(f"Exit point: {maze.exit}")
print(f"Solution path: {maze.path}")
```

### Generate a maze from a configuration file
```python
from mazegen import MazeGenerator

# Use a config file to customize your maze
maze = MazeGenerator("your_config.txt")
```

### Configuration file example

Create a config file containing:
```
WIDTH=30
HEIGHT=20
ENTRY=0,0
EXIT=29,19
PERFECT=True
SEED=42
ALGORITHM=wilson
OUTPUT_FILE=my_maze.txt
```

## What can you access?

After creating a maze, you can access:

- `maze.cols` - Width of the maze
- `maze.rows` - Height of the maze
- `maze.entry` - Entry coordinates (x, y)
- `maze.exit` - Exit coordinates (x, y)
- `maze.grid` - 2D array of Cell objects
- `maze.hex_repr` - Hexadecimal representation of the maze
- `maze.get_cell(x, y)` - Get a specific cell
- `maze.path` - Shortest solution path as a string of directions (N/S/E/W)

## Example: Access cells
```python
from mazegen import MazeGenerator, Cell

maze = MazeGenerator()

# Get a cell at position (5, 5)
cell = maze.get_cell(5, 5)

if cell:
    print(f"Cell coordinates: {cell.coord}")
    print(f"Cell walls: {cell.walls}")
    print(f"Hex representation: {cell.hex_repr}")
```

## Available algorithms

- **wilson** (default) - Creates uniform random mazes
- **dfs** - Depth-first search, creates longer corridors

## Requirements

- Python 3.10 or higher

## Authors

- Morgane Meurer
- Esther Babun

## License

MIT License - See LICENSE file for details.

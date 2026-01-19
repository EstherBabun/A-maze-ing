#!/usr/bin/env python3
# File: my_maze.py
# Author: ebabun <ebabun@student.42belgium.be>
# Created: 2026/01/19 08:42:20
# Updated: 2026/01/19 08:42:21

"""Docstring to write."""

import sys
import random
from typing import Dict, List, Any


class Cell:
    """Class that holds the cell attributes in a 2D maze.

    Attributes:
        coord (tuple): the (x, y) coordinates or (col, row) coordinates
        walls (list): dict of the 4 wall status[W,S,E,N] (1=closed, 0=open)
        is_entry (bool): True if the cell is the entry
        is_exit (bool): True if the cell is the exit
        current (bool): True if this is the current cell
        visited (bool): True if the cell has been checked already
    """

    def __init__(self, x: int, y: int) -> None:
        """Initialise the attributes of a cell."""
        self.coord: tuple = (x, y)
        self.walls: Dict[str, int] = {"W": 1, "S": 1, "E": 1, "N": 1}
        self.is_entry: bool = False
        self.is_exit: bool = False
        self.visited: bool = False

    @property
    def hex_repr(self) -> str:
        """Convert the status of the walls to an hex representation."""
        # store binary representation of walls into a string
        binary_str = "".join(str(v) for v in self.walls.values())
        # convert string from binary to decimal with int(binary_str, 2)
        # convert to hex using format specifier :X
        return f"{int(binary_str, 2):X}"


class Maze:
    """A class for the maze attributes and methods."""

    offset: Dict[str, tuple] = {
            "N": (0, -1),
            "S": (0, 1),
            "E": (1, 0),
            "W": (-1, 0)
            }
    adjacent: Dict[str, str] = {"N": "S", "S": "N", "E": "W", "W": "E"}


    def __init__(self, config_file: Optional[str] = None) -> None:
        """Initialise the attributes of the maze with the default config."""
        # Set defaults first
        self.cols: int = 20
        self.rows: int = 10
        self.seed: int | None = None
        self.perfect: bool = True
        self.entry: tuple = (0, 0)
        self.exit: tuple = (19, 9)

        # Track which settings came from config file
        custom: List[str] = []
        # Load config file if provided
        if config_file is not None:
            custom = self.load_config(config_file)
        else:
            print("No config file, switching to default settings.")
            self.print_config(custom)

        # Initialize remaining attributes
        self.tot_size: int = self.cols * self.rows
        self.path: str = ""
        self.grid: List[List[Cell]] = [[Cell(x, y) for x in range(self.cols)]
                                       for y in range(self.rows)]

    def print_config(self, custom: List[str]) -> None:
        """Print final settings of the maze."""
        print("\nMaze configuration:")
        config_items = {
            "WIDTH": self.cols,
            "HEIGHT": self.rows,
            "ENTRY": self.entry,
            "EXIT": self.exit,
            "SEED": self.seed,
            "PERFECT": self.perfect
        }

        for k, v in config_items.items():
            if k in custom:
                print(f"  {k}: {v}")
            else:
                print(f"  {k}: {v} (default)")

    def load_config(self, file: str) -> List[str]:
        """Parse the config file and update maze attributes. Returns list of custom keys."""
        custom: List[str] = []
        raw_config: Dict[str, str] = {}

        # Read and parse the config file
        raw_config = self._read_config_file(file)
        if raw_config is None:
            print("Switching to default settings")
            self.print_config(custom)
            return custom

        # Parse each configuration value
        custom = self._parse_config_values(raw_config)

        # Validate and adjust entry/exit points
        self._validate_entry_exit(custom)

        self.print_config(custom)
        return custom

    def _read_config_file(self, file: str) -> Dict[str, str] | None:
        """Read config file and return raw key-value pairs. Returns None on error."""
        try:
            with open(file, "r") as f:
                content: str = f.read()
                if content == '':
                    print(f"Config file is empty")
                    return None

                print(f"Loading settings from config file {file}...")
                raw_config: Dict[str, str] = {}

                for line in content.splitlines():
                    try:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            key, value = line.split('=', 1)
                            key = key.strip().upper()
                            raw_config[key] = value.strip()
                    except ValueError:
                        print(f'Error in line {line} - Expected syntax: "KEY=value"')
                        continue

                return raw_config

        except (FileNotFoundError, PermissionError) as e:
            print(f"Error: {e}")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None

    def _parse_config_values(self, raw_config: Dict[str, str]) -> List[str]:
        """Parse and validate each config value. Returns list of successfully parsed keys."""
        custom: List[str] = []

        for k, v in raw_config.items():
            try:
                if k == "WIDTH":
                    self.cols = int(v)
                    custom.append(k)
                elif k == "HEIGHT":
                    self.rows = int(v)
                    custom.append(k)
                elif k == "ENTRY":
                    self.entry = self._parse_coordinate(v, k)
                    custom.append(k)
                elif k == "EXIT":
                    self.exit = self._parse_coordinate(v, k)
                    custom.append(k)
                elif k == "PERFECT":
                    self.perfect = self._parse_boolean(v, k)
                    custom.append(k)
                elif k == "SEED":
                    self.seed = int(v)
                    custom.append(k)
                elif k == "OUTPUT_FILE":
                    self.output_file = v
                    custom.append(k)
                else:
                    print(
                            f"Error: Invalid keyword {k} - "
                            "Allowed: WIDTH, HEIGHT, ENTRY, "
                            "EXIT, OUTPUT_FILE, PERFECT, SEED"
                            )
            except Exception as e:
                print(f'Error in {k}: {e}\nSwitching to default value')

        return custom

    def _parse_coordinate(self, value: str, key: str) -> tuple:
        """Parse a coordinate string 'x,y' into a tuple."""
        coord_tuple = tuple(int(i.strip()) for i in value.split(','))
        if len(coord_tuple) != 2:
            raise ValueError(f'coordinates expect 2 values "x,y"')
        return coord_tuple

    def _parse_boolean(self, value: str, key: str) -> bool:
        """Parse a boolean string 'True' or 'False'."""
        if value.upper() == "TRUE":
            return True
        elif value.upper() == "FALSE":
            return False
        else:
            raise ValueError(f'boolean expects "True" or "False"')

    def _is_within_bounds(self, coord: tuple) -> bool:
        """Check if a coordinate is within maze bounds."""
        x, y = coord
        return 0 <= x < self.cols and 0 <= y < self.rows

    def reset_default_extry(self, point_type: str, custom: List[str]) -> None:
        """Reset entry or exit to default value and remove from custom list."""
        if point_type == "ENTRY":
            self.entry = (0, 0)
        elif point_type == "EXIT":
            self.exit = (self.cols - 1, self.rows - 1)
        if point_type in custom:
            custom.remove(point_type)

    def _validate_entry_exit(self, custom: List[str]) -> None:
        """Validate and adjust entry/exit points based on maze dimensions and 42 cells."""
        # Adjust exit defaults if WIDTH/HEIGHT changed
        if "EXIT" not in custom and ("WIDTH" in custom or "HEIGHT" in custom):
            self.exit = (self.cols - 1, self.rows - 1)

        # Check if entry/exit coordinates are within maze bounds
        if not self._is_within_bounds(self.entry):
            print(
                "Error: Entry point exceeds borders of the maze.\n"
                'Switching to default entry'
            )
            self.reset_default_extry("ENTRY", custom)
        if not self._is_within_bounds(self.exit):
            print(
                "Error: Exit point exceeds borders of the maze.\n"
                'Switching to default exit'
            )
            self.reset_default_extry("EXIT", custom)

        # Check if entry/exit coordinates conflict with 42 blocked cells
        ft_walls: List[tuple] = self.get_42_cells(self.cols, self.rows)
        if self.entry in ft_walls:
            print(
                f"Entry point is stuck in the 42 cells\n"
                "Switching to default entry"
            )
            self.reset_default_extry("ENTRY", custom)
        if self.exit in ft_walls:
            print(
                f"Exit point is stuck in the 42 cells\n"
                "Switching to default exit"
            )
            self.reset_default_extry("EXIT", custom)


    def get_42_cells(self, w: int, h: int) -> List[tuple]:
        """Calculate the coordinates of the 42 cells."""
        if w < 9 or h < 7:
                return [] #  No 42_walls, maze too small
        cx: int = (w - 1) // 2 if w % 2 == 0 else w // 2
        cy: int = (h - 1) // 2 if h % 2 == 0 else h // 2

        four_walls: List[tuple] = [(cx - 1, cy), (cx - 2, cy), (cx - 3, cy),
                        (cx - 1, cy + 1), (cx - 1, cy + 2),
                        (cx - 3, cy - 1), (cx - 3, cy - 2)]
        two_walls: List[tuple] = [(cx + 1, cy), (cx + 2, cy), (cx + 3, cy),
                        (cx + 1, cy + 1), (cx + 1, cy + 2),
                        (cx + 3, cy - 1), (cx + 3, cy - 2),
                        (cx + 1, cy - 2), (cx + 2, cy - 2), (cx + 3, cy - 2),
                        (cx + 2, cy + 2), (cx + 3, cy + 2)]

        ft_walls = four_walls + two_walls
        return ft_walls
    
    def block_42_walls(self) -> None:
        """Prevent access to the 42 walls in the center of the maze."""
        for x, y in self.get_42_cells(self.cols, self.rows):
            self.grid[y][x].visited = True

    def get_cell(self, x: int, y: int) -> Cell | None:
        """Get cell at (x, y), return None if out of borders."""
        if 0 <= x < self.cols and 0 <= y < self.rows:
            return self.grid[y][x]
        return None

    def get_unvisited_neighbors(self, cell: Cell) -> List[tuple]:
        """get all unvisited cells that have common wall with current cell."""
        neighbors: List[tuple] = []
        x, y = cell.coord
        for direction, (ox, oy) in self.offset.items():
            nx, ny = x + ox, y + oy
            neighbor: Cell = self.get_cell(nx, ny)
            if neighbor and not neighbor.visited:
                neighbors.append((direction, neighbor))
        return neighbors

    def delete_wall(self, cell: Cell, neighbor: Cell, direction: str) -> None:
        """Delete wall between two cells."""
        cell.walls[direction] = 0
        adj: str = self.adjacent[direction]
        neighbor.walls[adj] = 0
    
    def generate_maze(self) -> bool:
        """Generate maze with dfs backtracking."""
        # set entry point:
        entry_x, entry_y = self.entry 
        # block access to 42 walls
        self.block_42_walls()

        stack = []
        current = self.get_cell(entry_x, entry_y)
        current.visited = True
        n_visited = 1
        # set seed if configured
        if self.seed is not None:
            random.seed(self.seed)

        while n_visited < self.tot_size:
            neighbors = self.get_unvisited_neighbors(current)
            if neighbors:
                direction, next_cell = random.choice(neighbors)
                self.delete_wall(current, next_cell, direction)
                stack.append(current)
                current = next_cell
                current.visited = True
                n_visited += 1
            else:
                if stack:
                    current = stack.pop()
                else:
                    break

        # mark entry and exit:
        entry_cell = self.get_cell(*self.entry)
        entry_cell.is_entry = True
        exit_cell = self.get_cell(*self.exit)
        exit_cell.is_exit = True
        return True


    @property
    def hex_repr(self):
        """To print in hexa the grid of the maze"""
        maze_hex: str = ""
        for y in range(self.rows):
            maze_hex += "".join(self.grid[y][x].hex_repr for x in range(self.cols))
            maze_hex += "\n"
        return maze_hex

    def print_maze_visual(self):
        """Print a visual ASCII representation of the maze."""
        # Top border
        print("┌" + "─" * (self.cols * 2 - 1) + "┐")

        for y in range(self.rows):
            # Print vertical walls
            row = "│"
            for x in range(self.cols):
                cell = self.grid[y][x]

                # Cell marker (entry/exit)
                row += "S" if cell.is_entry else "E" if cell.is_exit else " "

                # East wall
                if cell.walls['E']:
                    row += "│"
                else:
                    row += " "
            print(row)

            # Print horizontal walls (except after last row)
            if y < self.rows - 1:
                row = "├"
                for x in range(self.cols):
                    cell = self.grid[y][x]

                    # South wall
                    if cell.walls['S']:
                        row += "─"
                    else:
                        row += " "

                    # Corner
                    if x < self.cols - 1:
                        row += "┼"
                    else:
                        row += "┤"
                print(row)

        # Bottom border
        print("└" + "─" * (self.cols * 2 - 1) + "┘")

   

def main() -> None:
    """Docstring to write."""
    # check the arguments
    if len(sys.argv) == 1:
        # Init maze with default settings
        my_maze: maze = Maze()
    elif len(sys.argv) == 2:
        # take the path to the config file
        config_file: str = sys.argv[1]
        # create maze instance
        my_maze: Maze = Maze(config_file)
    else:
        print("Usage: python3 a_maze_ing.py config_file(optional)")
        return

    # generate maze
    if my_maze.generate_maze() is False:
        return
    my_maze.print_maze_visual()
    print(my_maze.hex_repr)


if __name__ == "__main__":
    main()

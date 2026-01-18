#!/usr/bin/env python3
# File: parsing.py
# Author: ebabun <ebabun@student.42belgium.be>
# Author: mmeurer <mmeurer@student.42belgium.be>
# Created: 2026/01/15 18:33:22
# Updated: 2026/01/15 18:33:22


"""Docstring to write."""

import sys
import math
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
        dict_config: Dict[str, Any] = self.load_config(config_file)
        self.cols: int = dict_config["WIDTH"]
        self.rows: int = dict_config["HEIGHT"]
        self.tot_size: int = self.cols * self.rows
        self.entry: tuple = dict_config["ENTRY"]
        self.exit: tuple = dict_config["EXIT"]
        self.path: str = ""
        self.grid: List[List[Cell]] = [[Cell(x, y) for x in range(self.cols)]
                                       for y in range(self.rows)]
        self.seed: int | None = dict_config["SEED"]
        self.perfect: bool = dict_config["PERFECT"]

    def print_config(self, dict_config: Dict[str, Any], custom: List[str]) -> None:
        """Print final settings of the maze."""
        print("\nMaze configuration:")
        for k, v in dict_config.items():
            if k in custom:
                print(f"  {k}: {v}")
            else:
                print(f"  {k}: {v} (default)")

    def load_config(self, file: str) -> Dict[str, Any]:
        """Parse the config file and return the key,value pairs."""
        # create default dict settings
        dict_config: dict[str, Any] = {
                "WIDTH": 20,
                "HEIGHT": 10,
                "SEED": None,
                "PERFECT": True
                }
        custom: List[str] = []

        if file is None:
            print("No config file, switching to default settings.")
            dict_config["ENTRY"] = (0, 0)
            dict_config["EXIT"] = (19, 9)
            self.print_config(dict_config, custom)
            return dict_config

        # read from file and create dict of strings:
        try:
            with open(file, "r") as f:
                content: str = f.read()
                if content == '':
                    print(f"Config file is empty - switching to default settings")
                    dict_config["ENTRY"] = (0, 0)
                    dict_config["EXIT"] = (19, 9)
                    self.print_config(dict_config, custom)
                    return dict_config

                print(f"Loading settings from config file {file}...")
                for line in content.splitlines():
                    line = line.strip()
                    if line and not line.startswith('#'):
                        key, value = line.split('=', 1)
                        key = key.strip().upper()
                        dict_config[key] = value.strip()
                        custom.append(key)
        except ValueError as e:
            print(f'Error in line {line} - Expected syntax: "KEY=value"')
            return {}
        except (FileNotFoundError, PermissionError) as e:
            print(f"Error: {e}")
            return {}
        except Exception as e:
            print(f"Error: {e}")
            return {}

        # Convert numeric values, tuples and booleans
        for k, v in dict_config.items():
            if k in custom:
                try:
                    # Numeric values for WIDTH and HEIGHT
                    if k == "WIDTH" or k == "HEIGHT":
                        dict_config[k] = int(v)
                        # Raise error to prevent huge maze:
                        # if dict_config[k] > MAX_SIZE(tbd) raise error
                    # tuples for ENTRY and EXIT
                    elif k == "ENTRY" or k == "EXIT":
                        dict_config[k] = tuple(int(i.strip()) for i in v.split(','))
                        if len(dict_config[k]) > 2:
                            raise ValueError(f'{k} expects 2 values "x,y"')
                    # bool value for PERFECT
                    elif k == "PERFECT":
                        if v.upper() == "TRUE":
                            dict_config[k] = True
                        elif v.upper() == "FALSE":
                            dict_config[k] = False
                        else:
                            raise ValueError(f'{k} expects "True" or "False"')
                    # path name of the OUTPUT_FILE
                    elif k == "OUTPUT_FILE":
                        dict_config[k] = v
                    # the chosen seed
                    elif k == "SEED":
                        if dict_config["SEED"] == None:
                            continue
                        else:
                            dict_config[k] = int(v)
                    # discard invalid keys
                    else:
                        print(
                                f"Error in {k} - "
                                "Allowed: WIDTH, HEIGHT, ENTRY, "
                                "EXIT, OUTPUT_FILE, PERFECT, SEED"
                                )
                except Exception as e:
                    default_value = {
                        "WIDTH": 20,
                        "HEIGHT": 10,
                        "SEED": None,
                        "PERFECT": True
                        }.get(k, None)

                    print(
                            f'Error in {k}: {e}\n'
                            f'Switching to default {k}'
                            )
                    dict_config[k] = default_value
                    custom.remove(k)

        w = dict_config["WIDTH"]
        h = dict_config["HEIGHT"]
        if "ENTRY" not in custom:
            dict_config["ENTRY"] = (0, 0)
        if "EXIT" not in custom:
            dict_config["EXIT"] = (w - 1, h - 1)

        # Check if entry/exit are within bounds
        entry_x, entry_y = dict_config["ENTRY"]
        exit_x, exit_y = dict_config["EXIT"]
        if entry_x < 0 or entry_y < 0 or entry_x > w - 1 or entry_y > h - 1:
            print(
                    "Error: Entry point exceeds borders of the maze.\n"
                    'Switching to default entry'
                    )
            dict_config["ENTRY"] = (0, 0)
            custom.remove("ENTRY")
        if exit_x < 0 or exit_y < 0 or exit_x > w - 1 or exit_y > h - 1:
            print(
                    "Error: Exit point exceeds borders of the maze.\n"
                    'Switching to default exit'
                    )
            dict_config["EXIT"] = (w - 1, h - 1)
            custom.remove("EXIT")
        # Check if entry/exit are within the 42 blocked cells
        ft_walls: List[tuple] = self.get_42_cells(w, h)
        if dict_config["ENTRY"] in ft_walls:
            print(
                    f"Entry point is stuck in the 42 cells\n"
                        "Switching to default entry"
                    )
            dict_config["ENTRY"] = (0, 0)
            custom.remove("ENTRY")

        if dict_config["EXIT"] in ft_walls:
            print(
                    f"Exit point is stuck in the 42 cells\n"
                    "Switching to default exit"
                    )
            dict_config["EXIT"] = (w - 1, h - 1)
            custom.remove("EXIT")

        self.print_config(dict_config, custom)
        return dict_config

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

    if len(sys.argv) == 2:
        # take the path to the config file
        config_file: str = sys.argv[1]
        # create maze instance
        my_maze: Maze = Maze(config_file)
        if my_maze is None:
            return
    # generate maze
    if my_maze.generate_maze() is False:
        return
    my_maze.print_maze_visual()
    print(my_maze.hex_repr)
    


if __name__ == "__main__":
    main()

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


class Cell(object):
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
        self.current: bool = False
        self.visited: bool = False

    @property
    def hex_repr(self) -> str:
        """Convert the status of the walls to an hex representation."""
        # store binary representation of walls into a string
        str_bin: str = "".join(str(v) for v in self.walls.values())

        # convert string from binary to decimal with int(str, 2)
        dec_repr: int = int(str_bin, 2)

        # Convert to hex (without '0x' prefix)
        hex_repr: str = hex(dec_repr)[2:].upper()
        return hex_repr


class Maze:
    """A class for the maze attributes and methods."""

    offset: Dict[str, tuple] = {
            "N": (0, -1),
            "S": (0, 1),
            "E": (1, 0),
            "W": (-1, 0)
            }
    adjacent: Dict[str, str] = {"N": "S", "S": "N", "E": "W", "W": "E"}

    def __init__(self) -> None:
        """Initialise the attributes of the maze with the default config."""
        self.cols: int = 20
        self.rows: int = 10
        self.tot_size: int = self.cols * self.rows
        self.entry: tuple = (0, 0)
        self.exit: tuple = (self.cols - 1, self.rows - 1)
        self.path: str = ""
        self.grid: List[List[Cell]] = [[Cell(x, y) for x in range(self.cols)]
                                       for y in range(self.rows)]
        self.seed: Union[int, None] = None
        self.perfect: bool = True

    def configure_maze(self, config: Dict[str, Any]) -> None:
        """Initialise the attributes of the maze with the loaded config."""
        if "WIDTH" in config.keys():
            self.cols = config["WIDTH"]
        if "HEIGHT" in config.keys():
            self.rows = config["HEIGHT"]
        self.tot_size = self.cols * self.rows
        if "ENTRY" in config.keys():
            self.entry = config["ENTRY"]
        if "EXIT" in config.keys():
            self.exit = config["EXIT"]
        if "SEED" in config.keys():
            self.seed = config["SEED"]
        if "PERFECT" in config.keys():
            self.perfect = config["PERFECT"]

    def load_config(self, file: str) -> Dict[str, Any]:
        """Parse the config file and return the key,value pairs."""
        dict_config: dict[str, Any] = {}

        # read from file and create dict of strings:
        try:
            with open(file, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        key, value = line.split('=', 1)
                        dict_config[key.strip().upper()] = value.strip()
        except ValueError as e:
            print(f"Error in line {line}: {e}")
            return {}
        except (FileNotFoundError, PermissionError) as e:
            print(f"Error: {e}")
            return {}
        except Exception as e:
            print(f"Error: {e}")
            return {}

        # Convert numeric values, tuples and booleans
        for k, v in dict_config.items():
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
                    dict_config[k] = int(v)
                # discard invalid keys
                else:
                    raise ValueError(
                            "Expected: WIDTH, HEIGHT, ENTRY, "
                            "EXIT, OUTPUT_FILE, PERFECT, SEED"
                            )
            except Exception as e:
                print(f"Error in config file: {k}={v}\n{e}")
                return {}

        # Check if entry/exit are within bounds
        entry_x, entry_y = dict_config["ENTRY"]
        exit_x, exit_y = dict_config["EXIT"]
        w = dict_config["WIDTH"]
        h = dict_config["HEIGHT"]
        if entry_x < 0 or entry_y < 0 or entry_x > w - 1 or entry_y > h - 1:
            print("Error: Entry point exceeds borders of the maze.")
            return {}
        if exit_x < 0 or exit_y < 0 or exit_x > w - 1 or exit_y > h - 1:
            print("Error: Exit point exceeds borders of the maze.")
            return {}

        return dict_config

    def get_42_cells(self) -> List[tuple]:
        """Calculate the coordinates of the 42 cells."""
        w = self.cols
        h = self.rows
        if w < 9 or h < 7:
                return [] #  No 42_walls, maze too small
        if w % 2 == 0:
                cx = math.floor(w / 2) - 1
        else:
                cx = math.floor(w / 2)
        if h % 2 == 0:
                cy = math.floor(h / 2) - 1
        else:
                cy = math.floor(h / 2)

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

    def validate_entry_exit(self) -> bool:
        """Check if entry/exit is outside of the blocked 42 cells."""
        ft_walls = self.get_42_cells()
        # Check if entry/exit are in 42 blocked cells
        if self.entry in ft_walls:
                print(f"Wrong entry point: {self.entry}")
                print(f"Forbiden: {ft_walls}")
                return False #  return false to stop execution !
        if self.exit in ft_walls:
                print(f"Wrong exit point: {self.exit}")
                print(f"Forbiden: {ft_walls}")
                return False #  return false to stop execution

        return True

    
    def block_42_walls(self) -> None:
        """Prevent access to the 42 walls in the center of the maze."""
        ft_walls: List[tuple] = self.get_42_cells()
        for item in ft_walls:
                x, y = item
                self.grid[y][x].visited = True

    def get_cell(self, x: int, y: int) -> Optional[Cell]:
        """Get cell at (x, y), return None if out of borders."""
        if 0 <= x < self.cols and 0 <= y < self.rows:
            return self.grid[y][x]
        return None

    def get_unvisited_commons(self, cell: Cell) -> List[tuple]:
        """get all unvisited cells that have common wall with current cell."""
        commons: List[tuple] = []
        x, y = cell.coord
        for direction, (ox, oy) in self.offset.items():
            nx, ny = x + ox, y + oy
            common: Cell = self.get_cell(nx, ny)
            if common and not common.visited:
                commons.append((direction, common))
        return commons

    def delete_wall(self, cell: Cell, common: Cell, direction: str) -> None:
        """Delete wall between two cells."""
        cell.walls[direction] = 0
        adj: str = self.adjacent[direction]
        common.walls[adj] = 0
    
    def generate_maze(self) -> bool:
        """Generate maze with dfs backtracking."""
        # set entry point:
        entry_x, entry_y = self.entry 
        # block access to 42 walls
        self.block_42_walls()
        # check entry/exit aren't within blocked cells
        if self.validate_entry_exit() is False:
            return False
        stack = []
        current = self.get_cell(entry_x, entry_y)
        current.visited = True
        n_visited = 1
        # set seed if configured
        if self.seed is not None:
            random.seed(self.seed)

        while n_visited < self.tot_size:
            commons = self.get_unvisited_commons(current)
            if commons:
                direction, next_cell = random.choice(commons)
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


    def print_grid_hexa(self):
        """To print in hexa the grid of the maze"""
        for y in range(self.rows):
            row = ""
            for x in range(self.cols):
                row += self.grid[y][x].hex_repr
            print(row)

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
                if cell.is_entry:
                    row += "S"
                elif cell.is_exit:
                    row += "E"
                else:
                    row += " "

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
        print("No config file, switching to default settings.")
        # Init maze with default settings
        my_maze: maze = Maze()

    if len(sys.argv) == 2:
        print(f"Loading settings from config file {sys.argv[1]}")
        # take the path to the config file
        config_file: str = sys.argv[1]
        # create maze instance
        my_maze: Maze = Maze()
        # parse config file into a dict
        config: Dict[str, Any] = my_maze.load_config(config_file)
        # Stop if error in config file
        if not config:
            return
        # set maze attributes with loaded config
        my_maze.configure_maze(config)

    if my_maze.generate_maze() is False:
        return
    my_maze.print_maze_visual()
    


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# File: parsing.py
# Author: ebabun <ebabun@student.42belgium.be>
# Author: mmeurer <mmeurer@student.42belgium.be>
# Created: 2026/01/15 18:33:22
# Updated: 2026/01/15 18:33:22


"""Docstring to write."""

import sys
import math
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
        self.walls: Dict[str, int] = {"W": 0, "S": 0, "E": 0, "N": 0}
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

    offset: Dict[str, tuple) = {
            "N": (0, -1),
            "S": (0, 1),
            "E": (1, 0),
            "W": (-1, 0)
            }
    adjacent: Dict[str, str] = {"N": "S", "S": "N", "E": "W", "W": "E"}

    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialise the attributes of the maze with the loaded config."""
        self.cols: int = 42
        self.rows: int = 42
        self.tot_size: int = self.cols * self.rows
        self.entry: tuple = (0, 0)
        self.exit: tuple = (self.cols - 1, self.rows - 1)
        self.path: str = ""
        self.grid: List[List[Cell]] = [[Cell(x, y) for x in range(self.cols)]
                                       for y in range(self.rows)]
        self.seed: Union[int, None] = None

    def configure_maze(self, config: Dict[str, Any]) -> None:
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

    def external_walls(self):
        """To put external walls and print the map empty"""
        for x in range(self.cols):
            self.grid[0][x].walls["N"] = 1
            self.grid[self.rows - 1][x].walls["S"] = 1
        for y in range(self.rows):
            self.grid[y][0].walls["W"] = 1
            self.grid[y][self.cols - 1].walls["E"] = 1

    def fill_grid(self) -> None:
        """Set all the walls of the grid to closed."""
        for row in self.grid:
            for cell in row:
                cell.walls = {"W": 1, "S": 1, "E": 1, "N": 1}
                cell.visited = False

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
        """Check if entry/exit is within bounds and out of the blocked 42 cells."""

        # Check if entry/exit are within bounds
        entry_x, entry_y = self.entry
        exit_x, exit_y = self.exit
        w = self.cols
        h = self.rows
        if entry_x < 0 or entry_y < 0 or entry_x > w - 1 or entry_y > h - 1:
            print("Error: Entry point exceeds borders of the maze.")
            return False
        if exit_x < 0 or exit_y < 0 or exit_x > w - 1 or exit_y > h - 1:
            print("Error: Exit point exceeds borders of the maze.")
            return False
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
        for direction, (ox, oy) in offset:
            nx, ny = x + ox, y + oy
            common: Cell = self.get_cell(nx, ny)
            if common and not common.visited:
                commons.append(direction, common)
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
        # close all walls in the grid
        self.fill_grid()
        # block access to 42 walls

    def print_grid_hexa(self):
        """To print in hexa the grid of the maze"""
        for y in range(self.rows):
            row = ""
            for x in range(self.cols):
                row += self.grid[y][x].hex_repr
            print(row)



def load_config(file: str) -> Dict[str, Any]:
    """Parse the config file and return the key,value pairs."""
    dict_config: dict[str, Any] = {}
    if file is None:
        print("Error: Cannot take None as config file")
        return None

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
        return None
    except (FileNotFoundError, PermissionError) as e:
        print(f"Error: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

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
            return None

    return dict_config


def main() -> None:
    """Docstring to write."""
    # check the arguments
    if len(sys.argv) != 2:
        print("Please pass a config file as argument")
        return

    # take the path to the config file
    config_file: str = sys.argv[1]

    # parse config file into a dict
    config: Dict[str, Any] = load_config(config_file)
    if config is None:
        return

    my_maze: Maze = Maze(config)

    print("=== First Parsing Test ===\n")

    # print the config dictionary
    print("The config dict:\n")
    for key, value in config.items():
        print(f"  {key}: {value}")
    print()
    
    print("The maze hex representation:\n")
    my_maze.external_walls()
    my_maze.print_grid_hexa()


if __name__ == "__main__":
    main()

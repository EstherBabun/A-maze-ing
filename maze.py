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
        common (list): list adjacent cells (x-1,y)(x+1,y)(x,y-1)(x,y+1)
        is_extry (bool): True if the cell is the entry or the exit
        current (bool): True if this is the current cell
        visited (bool): True if the cell has been checked already
    """

    def __init__(self, x: int, y: int) -> None:
        """Initialise the attributes of a cell."""
        self.coord: tuple = (x, y)
        self.walls: Dict[str, int] = {"W": 0, "S": 0, "E": 0, "N": 0}
        self.common: List[Cell] = []
        self.is_extry: bool = False
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

    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialise the attributes of the maze with the loaded config."""
        self.cols: int = config["WIDTH"]
        self.rows: int = config["HEIGHT"]
        self.tot_size: int = config["WIDTH"]*config["HEIGHT"]
        self.entry: tuple = config["ENTRY"]
        self.exit: tuple = config["EXIT"]
        self.path: str = ""
        self.grid: List[List[Cell]] = [[Cell(x, y) for x in range(self.cols)]
                                       for y in range(self.rows)]
        # self.maze: ?

    def external_walls(self) -> None:
        """To put external walls and print the map empty"""
        for x in range(self.cols):
            self.grid[0][x].walls["N"] = 1
            self.grid[self.rows - 1][x].walls["S"] = 1
        for y in range(self.rows):
            self.grid[y][0].walls["W"] = 1
            self.grid[y][self.cols - 1].walls["E"] = 1

    def print_grid_hexa(self) -> None:
        """To print in hexa the grid of the maze"""
        for y in range(self.rows):
            row = ""
            for x in range(self.cols):
                row += self.grid[y][x].hex_repr
            print(row)

    def block_42_walls(self) -> bool:
        """Prevent access to the 42 walls in the center of the maze."""
        w = self.cols
        h = self.rows
        if w < 9 or h < 7:
            return True  # No 42_walls, maze too small
        if w % 2 == 0:
            cx = math.floor(w / 2) - 1
        else:
            cx = math.floor(w / 2)
        if h % 2 == 0:
            cy = math.floor(h / 2) - 1
        else:
            cy = math.floor(h / 2)

        four_walls: List[tuple] = [
            (cx - 1, cy), (cx - 2, cy), (cx - 3, cy),
            (cx - 1, cy + 1), (cx - 1, cy + 2),
            (cx - 3, cy - 1), (cx - 3, cy - 2),
            ]
        two_walls: List[tuple] = [
            (cx + 1, cy), (cx + 2, cy), (cx + 3, cy),
            (cx + 1, cy + 1), (cx + 1, cy + 2),
            (cx + 3, cy - 1), (cx + 3, cy - 2),
            (cx + 1, cy - 2), (cx + 2, cy - 2), (cx + 3, cy - 2),
            (cx + 2, cy + 2), (cx + 3, cy + 2)
            ]

        ft_walls = four_walls + two_walls

        if self.entry in ft_walls:
            print(f"Wrong entry point: {self.entry}")
            print(f"Forbiden: {ft_walls}")
            return False  # return false to stop execution !
        if self.exit in ft_walls:
            print(f"Wrong exit point: {self.exit}")
            print(f"Forbiden: {ft_walls}")
            return False  # return false to stop execution
        for item in ft_walls:
            x, y = item
            self.grid[y][x].visited = True
        return True


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
            elif k.upper() == "OUTPUT_FILE":
                dict_config[k] = v

            # discard invalid keys
            else:
                raise ValueError(
                        "Expected: WIDTH, HEIGHT, ENTRY, "
                        "EXIT, OUTPUT_FILE, PERFECT"
                        )

        except Exception as e:
            print(f"Error in config file: {k}={v}\n{e}")
            return None

    # Handle invalid entry and exit points
    entry_x, entry_y = dict_config["ENTRY"]
    exit_x, exit_y = dict_config["EXIT"]
    w = dict_config["WIDTH"]
    h = dict_config["HEIGHT"]
    if entry_x < 0 or entry_y < 0 or entry_x > w - 1 or entry_y > h - 1:
        print("Error: Entry point exceeds borders of the maze.")
        return None
    if exit_x < 0 or exit_y < 0 or exit_x > w - 1 or exit_y > h - 1:
        print("Error: Exit point exceeds borders of the maze.")
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

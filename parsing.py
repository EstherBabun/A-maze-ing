#!/usr/bin/env python3
# File: parsing.py
# Author: ebabun <ebabun@student.42belgium.be>
# Author: mmeurer <mmeurer@student.42belgium.be>
# Created: 2026/01/15 18:33:22
# Updated: 2026/01/15 18:33:22


"""Docstring to write."""

import sys
from typing import Dict, List, Any


class Cell(object):
    """Class that holds the cell attributes in a 2D maze.

    Attributes:
        coord (tuple): the (x, y) coordinates or (col, row) coordinates
        walls (list): dict of the 4 wall status[W,S,E,N] (1=closed, 0=open)
        common (list): list adjacent cells (x-1,y)(x+1,y)(x,y-1)(x,y+1)
        is_extry (bool): True if the cell is the entry or the exit
        current (bool): True if this is the current cell
        checked (bool): True if the cell has been checked already
    """

    def __init__(self, x: int, y: int) -> None:
        """Initialise the attributes of a cell."""
        self.coord: tuple = (x, y)
        self.walls: Dict[str, int] = {"W": 0, "S": 0, "E": 0, "N": 0}
        self.common: List[Cell] = []
        self.is_extry: bool = False
        self.current: bool = False
        self.checked: bool = False

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

    def external_walls(self):
        """To put external walls and print the map empty"""
        for x in range(self.cols):
            self.grid[0][x].walls["N"] = 1
            self.grid[self.rows - 1][x].walls["S"] = 1
        for y in range(self.rows):
            self.grid[y][0].walls["W"] = 1
            self.grid[y][self.cols - 1].walls["E"] = 1

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
    print("The config dict:")
    for key, value in config.items():
        print(f"  {key}: {value}")
    print()

    # print the attributes of my maze:
    print("The maze attributes:")
    for key, value in vars(my_maze).items():
        print(f"  {key}: {value}")
    print()
    my_maze.external_walls()
    my_maze.print_grid_hexa()


if __name__ == "__main__":
    main()

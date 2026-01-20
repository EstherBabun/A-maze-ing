#!/usr/bin/env python3
# File: maze.py
# Author: ebabun <ebabun@student.42belgium.be>
# Author: mmeurer <mmeurer@student.42belgium.be>
# Created: 2026/01/15 18:33:22
# Updated: 2026/01/15 18:33:22

"""Docstring to write. Version Morgane"""

import sys
import math
from typing import Dict, List, Any
import random


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
        self.walls: Dict[str, int] = {"W": 1, "S": 1, "E": 1, "N": 1}
        self.visited: bool = False
        self.untouchable: bool = False

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
    DX = {"E": 1, "W": -1, "N": 0, "S": 0}
    DY = {"E": 0, "W": 0, "N": -1, "S": 1}

    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialise the attributes of the maze with the loaded config."""
        self.cols: int = config["WIDTH"]
        self.rows: int = config["HEIGHT"]
        self.seed: int | None = None
        self.perfect: bool = config["PERFECT"]
        self.algorithm = config["ALGORITHM"]
        self.grid: List[List[Cell]] = [[Cell(x, y) for x in range(self.cols)]
                                       for y in range(self.rows)]
        self.block_42_walls()
        self.non_visited: List[Cell] = [
            cell for row in self.grid
            for cell in row if not cell.untouchable
            ]
        self.start = self.grid[config["ENTRY"][1]][config["ENTRY"][0]]
        self.exit = self.grid[config["EXIT"][1]][config["EXIT"][0]]

    def set_visited(self, x, y):
        self.grid[y][x].visited = True
        self.non_visited.remove(self.grid[y][x])

    def set_walls(self, x, y, dir):
        OPPOSITE = {"E": "W", "W": "E", "N": "S", "S": "N"}
        nx, ny = x + Maze.DX[dir], y + Maze.DY[dir]
        self.grid[y][x].walls[dir] = 0
        self.grid[ny][nx].walls[OPPOSITE[dir]] = 0

    def random_cell(self) -> Cell:
        """To randomly choice a non visited cell in the grid"""
        return random.choice(self.non_visited)

    def neighbors_cells(self, cell: Cell) -> tuple[Cell, str]:
        """To pick a random cell in allowed neighbors and her direction"""
        nearby_cell = []
        x, y = cell

        if x > 0 and not self.grid[y][x - 1].untouchable:
            nearby_cell.append((self.grid[y][x - 1], "W"))
        if x < self.cols - 1 and not self.grid[y][x + 1].untouchable:
            nearby_cell.append((self.grid[y][x + 1], "E"))
        if y > 0 and not self.grid[y - 1][x].untouchable:
            nearby_cell.append((self.grid[y - 1][x], "N"))
        if y < self.rows - 1 and not self.grid[y + 1][x].untouchable:
            nearby_cell.append((self.grid[y + 1][x], "S"))
        return random.choice(nearby_cell)

    def Wilson_algorithm(self):
        """Generate an uniform random maze using Wilson algorithm"""
        # Premier îlot du labyrinthe
        x, y = self.entry
        self.set_visited(x, y)

        # walk until every cell is visited
        while len(self.non_visited) != 0:
            random_cell = self.random_cell()
            for x, y, dir in self.walk(random_cell):
                self.set_visited(x, y)
                self.set_walls(x, y, dir)

    def walk(self, start_cell: Cell) -> List[tuple[int, int, str]]:
        """walk on until founding a visited cell without looping"""
        cx, cy = start_cell.coord
        cell_visited = {}
        path = []
        walking = True
        curr_cell = start_cell

        while walking:
            # random choice in neighbors cells
            next, dir = self.neighbors_cells(curr_cell.coord)
            cell_visited[curr_cell.coord] = dir
            if next.visited:
                break

            # Loop detection
            if next.coord in path:
                loop_start_idx = path.index(next.coord)
                path = path[:loop_start_idx + 1]
            else:
                path.append(next.coord)
            curr_cell = next

        # final way reconstruction
        path = []
        x, y = cx, cy
        while (x, y) in cell_visited:
            dir = cell_visited[(x, y)]
            path.append((x, y, dir))
            x, y = x + Maze.DX[dir], y + Maze.DY[dir]
        return path

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

        for x, y in ft_walls:
            if self.algorithm == "Wilson":
                self.grid[y][x].untouchable = True
            elif self.algorithm == "DFS":
                self.grid[y][x].visited = True
        return True

    def export_to_txt(self, filename="maze.txt"):
        """To generate a file with the maze in hexadecimal"""
        try:
            with open(filename, "w") as f:
                for y in range(self.rows):
                    line = ""
                    for x in range(self.cols):
                        line += self.grid[y][x].hex_repr
                    f.write(line + "\n")
        except Exception as e:
            print(f"Erreur lors de l'écriture du fichier: {e}")

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


class MazeGenerator:
    """??? A quoi ça sert ???"""


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
            # which algo is choosen
            elif k == "ALGORITHM":
                if v == "Wilson" or v == "DFS":
                    dict_config[k] == v
                else:
                    raise ValueError(f'{k} expects "Wilson" or "DFS"')

            # discard invalid keys
            else:
                raise ValueError(
                        "Expected: WIDTH, HEIGHT, ENTRY, "
                        "EXIT, OUTPUT_FILE, PERFECT", "ALGORITHM"
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
    print("\n=== Test pour Wilson ===\n")
    print(len(my_maze.non_visited))
    # my_maze.Wilson_algorithm()
    print(my_maze.algorithm)


if __name__ == "__main__":
    main()

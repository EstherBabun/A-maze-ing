#!/usr/bin/env python3
# File: cell.py
# Author: ebabun <ebabun@student.42belgium.be>
# Author: mmeurer <mmeurer@student.42belgium.be>
# Created: 2026/01/20 18:33:22
# Updated: 2026/01/20 18:02:15

from __future__ import annotations
from typing import Dict
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from a_maze_ing import MazeGenerator


class Cell(object):
    """Class that holds the cell attributes in a 2D maze.

    Attributes:
        coord (tuple): the (x, y) coordinates or (col, row) coordinates
        walls (list): dict of the 4 wall status[W,S,E,N] (1=closed, 0=open)
        visited (bool): True if the cell has been checked already
        _is_42 (bool): True if the cell is a part of the 42 block
    """

    OPPOSITE = {"E": "W", "W": "E", "N": "S", "S": "N"}
    OFFSET: Dict[str, tuple] = {
            "N": (0, -1),
            "S": (0, 1),
            "E": (1, 0),
            "W": (-1, 0)
            }

    def __init__(self, x: int, y: int, maze: MazeGenerator) -> None:
        """Initialise the attributes of a cell."""
        self.maze = maze
        self.coord: tuple = (x, y)
        self.walls: Dict[str, int] = {"W": 1, "S": 1, "E": 1, "N": 1}
        self.visited: bool = False
        self._is_42: bool = False

    def __sub__(self, other) -> tuple[int, int]:
        """sub two coordonates"""
        return (self.coord[0] - other.coord[0], self.coord[1] - other.coord[1])

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

    def set_visited(self) -> None:
        """set a cell to visited and remove it from unvisited list"""
        self.visited = True
        self.maze.unvisited.remove(self)

    def set_walls(self, dir) -> None:
        """Delete the two walls in direction of the given path"""
        neighbor_cell = self.get_neighbor(dir)
        self.walls[dir] = 0
        neighbor_cell.walls[self.OPPOSITE[dir]] = 0

    def get_direction(self, neighbor) -> str:
        """Return the direction between two cells"""
        dx, dy = neighbor - self
        for k, v in self.OFFSET.items():
            if v == (dx, dy):
                return k

    def get_neighbor(self, dir) -> Cell:
        """Get the adjacent cell in the direction given"""
        x, y = self.coord
        nx, ny = x + self.OFFSET[dir][0], y + self.OFFSET[dir][1]
        return self.maze.grid[ny][nx]

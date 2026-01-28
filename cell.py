#!/usr/bin/env python3
# File: cell.py
# Author: ebabun <ebabun@student.42belgium.be>
# Author: mmeurer <mmeurer@student.42belgium.be>
# Created: 2026/01/20 18:33:22
# Updated: 2026/01/28 18:02:15

from __future__ import annotations
from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from maze_generator import MazeGenerator


class Cell(object):
    """Represent a cell in a 2D maze grid."""
    OPPOSITE = {"E": "W", "W": "E", "N": "S", "S": "N"}
    OFFSET: Dict[str, tuple] = {
            "N": (0, -1),
            "S": (0, 1),
            "E": (1, 0),
            "W": (-1, 0)
            }

    def __init__(self, x: int, y: int, maze: MazeGenerator) -> None:
        """
        Initialize a cell at the given coordinates.

        Args:
            x (int): Column index of the cell.
            y (int): Row index of the cell.
            maze (MazeGenerator): Maze instance that owns the cell.
        """
        self.maze = maze
        self.coord: tuple = (x, y)
        self.walls: Dict[str, int] = {"W": 1, "S": 1, "E": 1, "N": 1}
        self.visited: bool = False
        self._is_42: bool = False

    def __sub__(self, other: Cell) -> tuple[int, int]:
        """
        Compute the coordinate difference between two cells.

        Args:
            other (Cell): The cell to subtract from the self one.

        Returns:
            tuple[int, int]: Difference in (x, y) coordinates.
        """
        return (self.coord[0] - other.coord[0], self.coord[1] - other.coord[1])

    @property
    def hex_repr(self) -> str:
        """
        Convert the wall configuration into a hexadecimal value.

        Returns:
            str: Hexadecimal representation of the cell walls.
        """
        # store binary representation of walls into a string
        str_bin: str = "".join(str(v) for v in self.walls.values())

        # convert string from binary to decimal with int(str, 2)
        dec_repr: int = int(str_bin, 2)

        # Convert to hex (without '0x' prefix)
        hex_repr: str = hex(dec_repr)[2:].upper()
        return hex_repr

    def set_visited(self) -> None:
        """
        Mark the cell as visited and remove it from the unvisited list
        """
        self.visited = True
        self.maze.unvisited.remove(self)

    def set_walls(self, dir: str) -> None:
        """
        Remove the wall between this cell and its neighbor in a direction.

        Args:
            dir (str): Direction of the neighbor cell (N, S, E, or W)
        """
        neighbor_cell = self.get_neighbor(dir)
        if neighbor_cell:
            self.walls[dir] = 0
            neighbor_cell.walls[self.OPPOSITE[dir]] = 0

    def get_direction(self, neighbor: Cell) -> str | None:
        """
        Determine the direction of a neighboring cell.

        Args:
            neighbor (Cell): Adjacent cell.

        Returns:
            str | None: Direction of the neighbor (N, S, E, or W),
            or None if the cell is not adjacent.
        """
        dx, dy = neighbor - self
        for k, v in self.OFFSET.items():
            if v == (dx, dy):
                return k
        return None

    def get_neighbor(self, dir: str) -> Cell | None:
        """
         Get the neighboring cell in the given direction.

        Args:
            dir (str): Direction to look for (N, S, E, or W).

        Returns:
            Cell | None: The neighboring cell if it exists,
            otherwise None.
        """
        x, y = self.coord
        nx, ny = x + self.OFFSET[dir][0], y + self.OFFSET[dir][1]
        if 0 <= nx < self.maze.cols and 0 <= ny < self.maze.rows:
            neighbor: Cell = self.maze.grid[ny][nx]
            return neighbor
        return None

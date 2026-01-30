#!/usr/bin/env python3
# File: cell.py
# Author: ebabun <ebabun@student.42belgium.be>
# Author: mmeurer <mmeurer@student.42belgium.be>
# Created: 2026/01/20 18:33:22
# Updated: 2026/01/28 18:02:15

from typing import Dict


class Cell(object):
    """Represent a cell in a 2D maze grid."""

    def __init__(self, x: int, y: int) -> None:
        """
        Initialize a cell at the given coordinates.

        Args:
            x (int): Column index of the cell.
            y (int): Row index of the cell.
        """
        self.coord: tuple = (x, y)
        self.walls: Dict[str, int] = {"W": 1, "S": 1, "E": 1, "N": 1}
        self.visited: bool = False
        self._is_42: bool = False


    @property
    def hex_repr(self) -> str:
        """Convert the status of the walls to an hex representation."""
        # store binary representation of walls into a string
        binary_str = "".join(str(v) for v in self.walls.values())
        # convert string from binary to decimal with int(binary_str, 2)
        # convert to hex using format specifier :X
        return f"{int(binary_str, 2):X}"


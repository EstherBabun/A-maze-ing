# File: mazegen/cell.py
# Author: ebabun <ebabun@student.42belgium.be>
# Author: mmeurer <mmeurer@student.42belgium.be>
# Created: 2026/01/20 18:33:22
# Updated: 2026/01/28 18:02:15

"""Simple module for the cell class of a maze."""


class Cell:
    """Represent a cell in a 2D maze grid."""

    def __init__(self, x: int, y: int) -> None:
        """
        Initialize a cell at the given coordinates.

        Args:
            x (int): Column index of the cell.
            y (int): Row index of the cell.

        Attributes:
            coord (tuple(int, int)): coordinates of the cell
            walls (dict(str | None, int): directions of the walls
            mapped to a binary representations (1: closed, 0: opened)
            visited (bool): marks the cell as visited
            is_42 (bool): marks the cell as part of the 42 pattern
        """
        self.coord: tuple[int, int] = (x, y)
        self.walls: dict[str | None, int] = {"W": 1, "S": 1, "E": 1, "N": 1}
        self.visited: bool = False
        self.is_42: bool = False

    @property
    def hex_repr(self) -> str:
        """
        Convert the status of the walls to a hexadecimal representation.

        Walls are encoded in West, South, East, North order
        as a 4-bit binary number, then converted to hexadecimal (0-F).

        Returns:
            str: Single hexadecimal character representing wall configuration.
        """
        binary_str = "".join(str(v) for v in self.walls.values())
        return f"{int(binary_str, 2):X}"

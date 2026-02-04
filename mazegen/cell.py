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
        """
        self.coord: tuple[int, int] = (x, y)
        self.walls: dict[str | None, int] = {"W": 1, "S": 1, "E": 1, "N": 1}
        self.visited: bool = False
        self._is_42: bool = False

    @property
    def hex_repr(self) -> str:
        """
        Convert the status of the walls to a hexadecimal representation.

        Walls are encoded in WSEN order as a 4-bit binary number, then
        converted to hexadecimal (0-F).

        For example:
            - 0xF (1111) = all walls intact
            - 0x0 (0000) = all walls removed
            - 0x5 (0101) = West and East walls only

        Returns:
            str: Single hexadecimal character representing wall configuration.
        """
        # store binary representation of walls into a string
        binary_str = "".join(str(v) for v in self.walls.values())
        # convert string from binary to decimal with int(binary_str, 2)
        # convert to hex using format specifier :X
        return f"{int(binary_str, 2):X}"

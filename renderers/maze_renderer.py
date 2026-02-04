# File: renderers/maze_renderer.py
# Author: ebabun <ebabun@student.42belgium.be>
# Author: mmeurer <mmeurer@student.42belgium.be>
# Created: 2026/02/02 10:46:59
# Updated: 2026/02/02 10:46:59

"""
Parent class for maze rendering.

This module provides the abstract MazeRenderer class that contains
common functionality shared between ASCII and MLX renderers.
"""

from abc import ABC, abstractmethod
from mazegen import Cell, MazeGenerator, OFFSET


class MazeRenderer(ABC):
    """
    Abstract base class for maze renderers.

    This class contains common attributes and methods shared by
    ASCII and MLX renderers, providing a unified interface for
    maze rendering operations.

    Attributes:
        maze (MazeGenerator): The maze generator instance
        maze_hex (str): Hexadecimal representation of the maze
        show_soluce (bool): flag to know if solution path is shown or hidden
    """

    def __init__(self, maze: MazeGenerator) -> None:
        """
        Initialize the renderer with a maze.

        Args:
            maze (MazeGenerator): The maze generator instance
        """
        self.maze: MazeGenerator = maze
        self.maze_hex: str = maze.hex_repr
        self.show_soluce: bool = False
        self.path_coord: list[tuple[int, int]] = []
        self.set_path_coord()
        # remove exit form soluce path for mlx renderer
        self.soluce_path: list[tuple[int, int]] = self.path_coord[:-1]
        # reset current cell for navigation in mlx renderer
        self.current_cell: Cell | None = self.maze.entry_cell
        self.navigation_path: list[tuple[int, int]] = [self.maze.entry]

    def set_path_coord(self) -> None:
        """
        Convert the string solution path into coordinates.

        Populates the self.path_coord attribute with the coordinate sequence
        representing the shortest path from entry to exit.
        """
        path: list[tuple[int, int]] = []
        cx, cy = self.maze.entry
        for direction in self.maze.path:
            x, y = OFFSET[direction]
            cx += x
            cy += y
            path.append((cx, cy))
        self.path_coord = path

    @abstractmethod
    def new_maze(self) -> None:
        """Generate a new maze (to be implemented by subclasses)."""
        ...

    @abstractmethod
    def display_maze(self) -> None:
        """
        Display the maze (to be implemented by subclasses).

        Each renderer has its own display method.
        """
        ...

    @abstractmethod
    def handle_user_interaction(self) -> None:
        """
        Handle user interactions (to be implemented by subclasses).

        Each renderer has its own interaction handling.
        """
        ...

# File: mazegen/__init__.py
# Author: ebabun <ebabun@student.42belgium.be>
# Created: 2026/02/03 17:16:14
# Updated: 2026/02/03 17:16:14

"""mazegen - maze generation package.

This package provides tools for generating and solving a maze.

Example usage:
    >>> from mazegen import Cell, MazeGenerator, ...
"""

__version__ = "1.0.0"
__author__ = "ebabun, mmeurer"

from .cell import Cell
from .maze_generator import MazeGenerator, OFFSET

# Optional: explicitly define what gets exported
__all__ = [
    'Cell',
    'MazeGenerator',
    'OFFSET',
    '__version__',
    '__author__'
]

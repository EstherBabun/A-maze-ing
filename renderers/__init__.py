# File: renderers/__init__.py
# Author: ebabun <ebabun@student.42belgium.be>
# Created: 2026/02/04 13:43:26
# Updated: 2026/02/04 13:43:26

"""renderers - maze rendering package.

This package provides rendering implementations for displaying mazes
in different formats (ASCII terminal, MLX graphics).

Example usage:
    >>> from renderers import AsciiRenderer, MlxRenderer
"""

__version__ = "1.0.0"
__author__ = "ebabun, mmeurer"

from .maze_renderer import MazeRenderer
from .ascii_renderer import AsciiRenderer
from .mlx_renderer import MlxRenderer

__all__ = [
    'MazeRenderer',
    'AsciiRenderer',
    'MlxRenderer',
    '__version__',
    '__author__'
]

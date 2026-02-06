#!/usr/bin/env python3
# File: a_maze_ing.py
# Author: ebabun <ebabun@student.42belgium.be>
# Author: mmeurer <mmeurer@student.42belgium.be>
# Created: 2026/01/22 09:44:42
# Updated: 2026/01/28 09:44:42

"""
Entry point of the A-Maze-Ing program.

This module handles the file passed as a command-line argument,
creates a maze and launches the appropriate maze renderer
based on the configuration file.
"""

import sys
from mazegen import MazeGenerator


def main() -> None:
    """Create maze with config(optional) and launch the renderer."""
    # if no config file
    if len(sys.argv) == 1:
        maze = MazeGenerator()

    # if config file
    elif len(sys.argv) == 2:
        config_file: str = sys.argv[1]
        maze = MazeGenerator(config_file)
    else:
        print("Usage: python3 a_maze_ing.py config_file(optional)")
        return

    # launch selected display mode
    if maze.display == "ascii":
        from renderers import AsciiRenderer
        AsciiRenderer(maze)
    elif maze.display == "mlx":
        from renderers import MlxRenderer
        MlxRenderer(maze)


if __name__ == "__main__":
    main()

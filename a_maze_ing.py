#!/usr/bin/env python3
# File: a_maze_ing.py
# Author: ebabun <ebabun@student.42belgium.be>
# Author: mmeurer <mmeurer@student.42belgium.be>
# Created: 2026/01/22 09:44:42
# Updated: 2026/01/28 09:44:42

"""
Entry point of the A-Maze-Ing program.

This module parses command-line arguments and launches the
appropriate maze renderer based on the configuration file.
"""

import sys
from maze_parser import MazeParser
from maze_generator import MazeGenerator


def main() -> None:
    """
    Parse command-line arguments and launch the maze renderer.

    This function selects the appropriate renderer based on the
    configuration file and starts the maze display.
    """
    # if no config file: no display
    if len(sys.argv) == 1:
        maze = MazeGenerator()

    # if config file:
    elif len(sys.argv) == 2:
        config_file: str = sys.argv[1]
        maze = MazeGenerator(config_file)
    else:
        print("Usage: python3 a_maze_ing.py config_file(optional)")

    # check if display mode is activated
    # and if maze size can be rendered
    if maze.display != "none" and maze.is_displayable:
        from mlx_renderer import MlxRenderer
        from ascii_renderer import AsciiRenderer
        # launch selected display mode
        if maze.display == "ascii":
            ascii_d = AsciiRenderer(maze)
        else:
            mlx_d = MlxRenderer(maze)
        return

    maze.generate_maze()

if __name__ == "__main__":
    main()

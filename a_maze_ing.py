#!/usr/bin/env python3
# File: a_maze_ing.py
# Author: ebabun <ebabun@student.42belgium.be>
# Author: mmeurer <mmeurer@student.42belgium.be>
# Created: 2026/01/22 09:44:42
# Updated: 2026/01/28 09:44:42

import sys
from maze_generator import MazeGenerator

"""
Entry point of the A-maze-ing program.

This module parses command-line arguments and launches the
appropriate maze renderer based on the configuration file.
"""


def main() -> None:
    """
    Parse command-line arguments and launch the maze renderer.

    This function selects the appropriate renderer based on the
    configuration file and starts the maze display.
    """
    config = ""
    if sys.argv[1]:
    	config += sys.argv[1]
    maze: MazeGenerator = MazeGenerator(config)
    if len(sys.argv) == 1:
        print(1)
        # renderer = MazeRenderer()
    elif len(sys.argv) == 2:
        maze.generate_maze()
        maze.display_maze()
    else:
        print("Usage: python3 a_maze_ing.py config_file(optional)")
        return


if __name__ == "__main__":
    main()

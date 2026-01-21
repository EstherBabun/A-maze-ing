#!/usr/bin/env python3
# File: main.py
# Author: ebabun <ebabun@student.42belgium.be>
# Author: mmeurer <mmeurer@student.42belgium.be>
# Created: 2026/01/15 18:33:22
# Updated: 2026/01/21 22:21:15

"""Docstring to write. Version Morgane"""

import sys
from a_maze_ing import MazeGenerator


def main() -> None:
    """Docstring to write."""
    # check the arguments
    if len(sys.argv) == 1:
        # Init maze with default settings
        my_maze: MazeGenerator = MazeGenerator()
    elif len(sys.argv) == 2:
        # take the path to the config file
        config_file: str = sys.argv[1]
        # create maze instance
        my_maze: MazeGenerator = MazeGenerator(config_file)
    else:
        print("Usage: python3 a_maze_ing.py config_file(optional)")
        return

    # generate maze
    my_maze.generate_maze()


if __name__ == "__main__":
    main()

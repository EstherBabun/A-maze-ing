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
from mlx_renderer import MlxRenderer
from ascii_renderer import AsciiRenderer


def main() -> None:
    """
    Parse command-line arguments and launch the maze renderer.

    This function selects the appropriate renderer based on the
    configuration file and starts the maze display.
    """
    # if no config file:
    if len(sys.argv) == 1:
        mlx_d = MlxRenderer()

    # if config file:
    elif len(sys.argv) == 2:
        config_file: str = sys.argv[1]

        # instanciate parser
        parser: MazeParser = MazeParser(config_file, False)

        # check if maze size can be rendered
        if parser.is_displayable:

            # launch selected display mode
            if parser.display == "ascii":
                ascii_d = AsciiRenderer(config_file)
            else:
                mlx_d = MlxRenderer(config_file)

        # Generate maze without display
        else:
            from maze_generator import MazeGenerator
            maze = MazeGenerator(config_file)
            maze.generate_maze()
            return
    else:
        print("Usage: python3 a_maze_ing.py config_file(optional)")
        return


if __name__ == "__main__":
    main()

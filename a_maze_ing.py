#!/usr/bin/env python3
# File: a_maze_ing.py
# Author: ebabun <ebabun@student.42belgium.be>
# Author: mmeurer <mmeurer@student.42belgium.be>
# Created: 2026/01/22 09:44:42
# Updated: 2026/01/22 09:44:42

"""Docstring to write."""

import sys
from maze_renderer import MazeRenderer


def main() -> None:
    """Docstring to write."""
    # check the arguments
    if len(sys.argv) == 1:
        renderer = MazeRenderer()
    elif len(sys.argv) == 2:
        config_file: str = sys.argv[1]
        renderer = MazeRenderer(config_file)
    else:
        print("Usage: python3 a_maze_ing.py config_file(optional)")
        return


    # Affichage avec MiniLibX

    #my_maze.print_maze_visual()


if __name__ == "__main__":
    main()

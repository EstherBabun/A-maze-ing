#!/usr/bin/env python3
# File: a_maze_ing.py
# Author: ebabun <ebabun@student.42belgium.be>
# Author: mmeurer <mmeurer@student.42belgium.be>
# Created: 2026/01/22 09:44:42
# Updated: 2026/01/28 09:44:42

import sys
# from maze_generator import MazeGenerator
# from maze_renderer import MazeRenderer
from ascii_renderer import AsciiRenderer

"""
Entry point of the A-Maze-Ing program.

This module parses command-line arguments and launches the
appropriate maze renderer based on the configuration file.
"""


def check_display(config_file: str) -> str:
    """
    Read the configuration file and extract the display mode.

    Args:
        config_file (str): Path to the configuration file.

    Returns:
        str: the whole string wrote by the user.
    """
    try:
        with open(config_file, "r") as f:
            content = f.readlines()
    except Exception as e:
        print(f"Error: {e}")
    display = ""
    for line in content:
        line = line.upper()
        if "DISPLAY" in line:
            line = line.split("=")
            display = line[1].upper().strip()
    return display


def main() -> None:
    """
    Parse command-line arguments and launch the maze renderer.

    This function selects the appropriate renderer based on the
    configuration file and starts the maze display.
    """
    if len(sys.argv) == 1:
        print(1)
        # renderer = MazeRenderer()
    elif len(sys.argv) == 2:
        config_file: str = sys.argv[1]
        display = check_display(config_file)
        if display == "MLX":
            print("mlx")
            # renderer = MazeRenderer(config_file)
        else:
            ascii_d = AsciiRenderer(config_file)
            ascii_d.main()

    else:
        print("Usage: python3 a_maze_ing.py config_file(optional)")
        return


if __name__ == "__main__":
    main()

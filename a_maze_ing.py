#!/usr/bin/env python3
# File: a_maze_ing.py
# Author: ebabun <ebabun@student.42belgium.be>
# Author: mmeurer <mmeurer@student.42belgium.be>
# Created: 2026/01/22 09:44:42
# Updated: 2026/01/28 09:44:42

import sys
from maze_generator import MazeGenerator
from typing import List

"""
Entry point of the A-maze-ing program.

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
    content: List[str] = []
    try:
        with open(config_file, "r") as f:
            content = f.readlines()
    except Exception as e:
        return f"Error: {e}"
    display: str = ""
    for line in content:
        line_upper: str = line.upper()
        if "DISPLAY" in line_upper:
            parts: List[str] = line_upper.split("=")
            if len(parts) > 1:
                display = parts[1].strip()
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
        display: str = check_display(config_file)
        maze: MazeGenerator = MazeGenerator(config_file)
        maze.generate_maze()
        maze.display_maze()

        # peut etre mis dans la classe directement et du coup plus besoin de la première fonction
        if display == "MLX":
            print("mlx")
            # renderer = MazeRenderer(config_file)
        else:
            maze.display_maze()

    else:
        print("Usage: python3 a_maze_ing.py config_file(optional)")
        return


if __name__ == "__main__":
    main()

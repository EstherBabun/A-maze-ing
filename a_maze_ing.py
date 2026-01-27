#!/usr/bin/env python3
# File: a_maze_ing.py
# Author: ebabun <ebabun@student.42belgium.be>
# Author: mmeurer <mmeurer@student.42belgium.be>
# Created: 2026/01/22 09:44:42
# Updated: 2026/01/22 09:44:42

"""Docstring to write."""

import sys
# from maze_generator import MazeGenerator
# from maze_renderer import MazeRenderer
from ascii_renderer import AsciiRenderer


def check_display(config_file: str) -> str:
    """Check which display is choosen in the config file"""
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
    """Docstring to write."""
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
            ascii_d.create_maze()
        
    else:
        print("Usage: python3 a_maze_ing.py config_file(optional)")
        return


if __name__ == "__main__":
    main()

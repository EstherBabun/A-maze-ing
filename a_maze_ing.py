#!/usr/bin/env python3
# File: main.py
# Author: ebabun <ebabun@student.42belgium.be>
# Author: mmeurer <mmeurer@student.42belgium.be>
# Created: 2026/01/15 18:33:22
# Updated: 2026/01/21 22:21:15

"""Docstring to write. Version Morgane"""

import sys
from maze_generator import MazeGenerator
# from maze_renderer import MazeRenderer


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

    # generate maze passing "DFS" or "Wilson" as argument
    my_maze.generate_maze()
    my_maze.print_maze_visual()

    # Affichage avec MiniLibX
    """ renderer = MazeRenderer(my_maze.output_file)

    renderer.m.mlx_clear_window(renderer.ptr, renderer.win_ptr)
    renderer.create_image()
    # renderer.m.mlx_string_put(renderer.ptr, renderer.win_ptr,
    # 20, 20, 255, lines[0])  # pour les commandes

    stuff = [1, 2]
    renderer.m.mlx_mouse_hook(renderer.win_ptr, renderer.mymouse, None)
    renderer.m.mlx_key_hook(renderer.win_ptr, renderer.mykey, stuff)
    renderer.m.mlx_hook(renderer.win_ptr, 33, 0, renderer.gere_close, None)

    renderer.m.mlx_loop(renderer.ptr)
 """


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# File: test_mlx.py
# Author: ebabun <ebabun@student.42belgium.be>
# Created: 2026/01/20 16:09:10
# Updated: 2026/01/20 16:09:10

from mlx import Mlx
from typing import List, Dict, Tuple, Optional

class MazeRenderer:
    """Renders maze using MLX Python bindings."""

    def __init__(self, width: int, height: int, cell_size: int = 30):
        """
        Initialize MLX renderer.

        Args:
            width: Maze width in cells
            height: Maze height in cells
            cell_size: Size of each cell in pixels
        """
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.wall_thickness = 3

        # Window dimensions
        self.win_width = width * cell_size
        self.win_height = height * cell_size

        # Initialize MLX
        self.m = Mlx()
        self.ptr = self.m.mlx_init()

        # Colors
        self.COLOR_BLACK = 0x000000
        self.COLOR_WHITE = 0xFFFFFF
        self.COLOR_RED = 0xFF0000
        self.COLOR_GREEN = 0x00FF00
        self.COLOR_BLUE = 0x0066FF
        self.COLOR_YELLOW = 0xFFFF00
        self.COLOR_GRAY = 0xC0C0C0


    def mymouse(self, button, x, y, mystuff):
        print(f"Got mouse event! button {button} at {x},{y}.")

    def mykey(self, keynum, mystuff):
        print(f"Got key {keynum}, and got my stuff back:")
        print(mystuff)
        if keynum == 32:
            self.m.mlx_mouse_hook(win_ptr, None, None)

    def gere_close(self, dummy):
        self.m.mlx_loop_exit(self.ptr)


def main() -> None:
    renderer = MazeRenderer(20, 10)
    win_ptr = renderer.m.mlx_new_window(renderer.ptr, renderer.win_width, renderer.win_height, "A-maze-ing!")
    renderer.m.mlx_clear_window(renderer.ptr, win_ptr)
    renderer.m.mlx_string_put(renderer.ptr, win_ptr, 20, 20, 255, "Hello PyMlx!")
    (ret, w, h) = renderer.m.mlx_get_screen_size(renderer.ptr)
    print(f"Got screen size: {w} x {h} .")

    stuff = [1, 2]
    renderer.m.mlx_mouse_hook(win_ptr, renderer.mymouse, None)
    renderer.m.mlx_key_hook(win_ptr, renderer.mykey, stuff)
    renderer.m.mlx_hook(win_ptr, 33, 0, renderer.gere_close, None)

    renderer.m.mlx_loop(renderer.ptr)


if __name__ == "__main__":
    main()

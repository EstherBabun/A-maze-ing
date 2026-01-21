#!/usr/bin/env python3
# File: test_mlx.py
# Author: ebabun <ebabun@student.42belgium.be>
# Created: 2026/01/20 16:09:10
# Updated: 2026/01/20 16:09:10

from mlx import Mlx

class MazeRenderer:
    """Renders maze using MLX Python bindings."""

    CELL_SIZE = 30
    COLOR_WALL = 0xFFFFFF
    COLOR_BG = 0x222222

    def __init__(self, width: int, height: int):
        """
        Initialize MLX renderer.

        Args:
            width: Maze width in cells
            height: Maze height in cells
            wall_thickness: width of walls
        """
        self.width = width
        self.height = height
        self.wall_thickness = 3

        # Window dimensions
        self.win_width = width * self.CELL_SIZE
        self.win_height = height * self.CELL_SIZE

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

    def mykey(self, keynum, mystuff, win_ptr):
        print(f"Got key {keynum}, and got my stuff back:")
        print(mystuff)
        if keynum == 32:
            self.m.mlx_mouse_hook(win_ptr, None, None)

    def gere_close(self, dummy):
        self.m.mlx_loop_exit(self.ptr)

    def draw_square(self, mlx, win, x, y, size, color):
        for i in range(size):
            for j in range(size):
                self.m.mlx_pixel_put(mlx, win, x + i, y + j, color)

    def draw_maze(self, mlx, win, maze):
        for y, row in enumerate(maze):
            for x, cell in enumerate(row):
                if cell == '1':
                    color = self.COLOR_WALL
                else:
                    color = self.COLOR_BG

                self.draw_square(
                    mlx,
                    win,
                    x * self.TILE_SIZE,
                    y * self.TILE_SIZE,
                    self.TILE_SIZE,
                    color
                )


def open_file(filename):
    try:
        with open(filename, "r") as f:
            lines = [line.rstrip("\n") for line in f.readlines()]
    except FileNotFoundError:
        print(f"Erreur: le fichier {filename} est introuvable")
        return
    return lines




def main() -> None:
    lines = open_file("maze.txt")
    renderer = MazeRenderer(1080, 720)
    #renderer = MazeRenderer(len(lines), len(lines[0]))
    win_ptr = renderer.m.mlx_new_window(renderer.ptr, renderer.win_width, renderer.win_height, "A-maze-ing!")
    renderer.m.mlx_clear_window(renderer.ptr, win_ptr)
    renderer.m.mlx_string_put(renderer.ptr, win_ptr, 20, 20, 255, lines[0])  # pour les commandes
    (ret, w, h) = renderer.m.mlx_get_screen_size(renderer.ptr)
    print(f"Got screen size: {w} x {h} .")

    stuff = [1, 2]
    renderer.m.mlx_mouse_hook(win_ptr, renderer.mymouse, None)
    renderer.m.mlx_key_hook(win_ptr, renderer.mykey, stuff)
    renderer.m.mlx_hook(win_ptr, 33, 0, renderer.gere_close, None)

    renderer.m.mlx_loop(renderer.ptr)


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
# File: maze_renderer.py
# Author: ebabun <ebabun@student.42belgium.be>
# Author: mmeurer <mmeurer@student.42belgium.be>
# Created: 2026/01/20 16:09:10
# Updated: 2026/01/20 16:09:10

from mlx import Mlx


class MazeRenderer:
    """Renders maze using MLX Python bindings."""

    CELL_SIZE = 30
    COLOR_WALL = 0x00CC00
    COLOR_BG = 0x999999
    COLOR_42 = 0x003300
    WALL_THICKNESS = 3

    def __init__(self, width: int, height: int, hexa: list[list]):
        """
        Initialize MLX renderer.

        Args:
            width: Maze width in cells
            height: Maze height in cells
        Attributes:
            width, height : size of the window
            img_width, img_height : size of the maze
            wall_thickness: width of walls
            ptr: MLX instance
            win_ptr: Window identifier
            img_ptr: Image identifier
        """

        if height > width:
            self.height = height * self.CELL_SIZE
            self.width = int(width * self.CELL_SIZE * 1.60)
        else:
            self.width = width * self.CELL_SIZE
            self.height = int(height * self.CELL_SIZE * 1.60)
        self.content = hexa

        # Maze dimensions
        self.img_width = width * self.CELL_SIZE
        self.img_height = height * self.CELL_SIZE

        # Initialize MLX
        self.m = Mlx()
        self.ptr = self.m.mlx_init()
        self.win_ptr = self.m.mlx_new_window(
            self.ptr, self.width, self.height, "=== A-maze-ing ===")
        self.img_ptr = self.m.mlx_new_image(
            self.ptr, self.img_width, self.img_height)

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

    def my_mlx_pixel_put(self, data, x, y, color, line_length, bpp):
        """Fast pixel writing to image buffer."""
        if x >= 0 and y >= 0:  # Basic bounds checking
            offset = y * line_length + x * (bpp // 8)
            # Write color in BGR format
            data[offset] = color & 0xFF                 # Blue
            data[offset + 1] = (color >> 8) & 0xFF      # Green
            data[offset + 2] = (color >> 16) & 0xFF     # Red
            data[offset + 3] = 255                      # Alpha

    def draw_cell(self, data, size_line, bpp, i, j, color):
        """Fast pixel writing to image buffer."""
        start_y = i * self.CELL_SIZE
        start_x = j * self.CELL_SIZE

        for y in range(start_y, start_y + self.CELL_SIZE):
            for x in range(start_x, start_x + self.CELL_SIZE):
                self.my_mlx_pixel_put(data, x, y, color, size_line, bpp)

    def draw_north_wall(self, data, size_line, bpp, i, j):
        start_y = i * self.CELL_SIZE
        start_x = j * self.CELL_SIZE
        end_x = start_x + self.CELL_SIZE
        wall = self.COLOR_WALL
        t = self.WALL_THICKNESS

        for y in range(start_y, start_y + t):
            for x in range(start_x, end_x):
                self.my_mlx_pixel_put(data, x, y, wall, size_line, bpp)

    def draw_south_wall(self, data, size_line, bpp, i, j):
        start_x = j * self.CELL_SIZE
        end_y = i * self.CELL_SIZE + self.CELL_SIZE
        end_x = start_x + self.CELL_SIZE
        wall = self.COLOR_WALL
        t = self.WALL_THICKNESS

        for y in range(end_y - t, end_y):
            for x in range(start_x, end_x):
                self.my_mlx_pixel_put(data, x, y, wall, size_line, bpp)

    def draw_east_wall(self, data, size_line, bpp, i, j):
        start_y = i * self.CELL_SIZE 
        end_y = start_y + self.CELL_SIZE
        end_x = j * self.CELL_SIZE + self.CELL_SIZE
        wall = self.COLOR_WALL
        t = self.WALL_THICKNESS

        for x in range(end_x - t, end_x):
            for y in range(start_y, end_y):
                self.my_mlx_pixel_put(data, x, y, wall, size_line, bpp)

    def draw_west_wall(self, data, size_line, bpp, i, j):
        start_y = i * self.CELL_SIZE
        start_x = j * self.CELL_SIZE
        end_y = start_y + self.CELL_SIZE
        wall = self.COLOR_WALL
        t = self.WALL_THICKNESS

        for x in range(start_x, start_x + t):
            for y in range(start_y, end_y):
                self.my_mlx_pixel_put(data, x, y, wall, size_line, bpp)

    def create_image(self, lines):
        data, bpp, size_line, endian = self.m.mlx_get_data_addr(self.img_ptr)

        # Draw cases
        for i, line in enumerate(lines):
            for j, cell in enumerate(line):
                if cell == 'F':
                    self.draw_cell(data, size_line, bpp, i, j, self.COLOR_42)
                else:
                    self.draw_cell(data, size_line, bpp, i, j, self.COLOR_BG)
                # Draw walls
                if cell in "13579BD":
                    self.draw_north_wall(data, size_line, bpp, i, j)
                if cell in "4567CDE":
                    self.draw_south_wall(data, size_line, bpp, i, j)
                if cell in "2367ABE":
                    self.draw_east_wall(data, size_line, bpp, i, j)
                if cell in "89ABCDE":
                    self.draw_west_wall(data, size_line, bpp, i, j)

        # Display the image
        self.m.mlx_put_image_to_window(
            self.ptr, self.win_ptr, self.img_ptr, 0, 0)

    def open_file(filename):
        try:
            with open(filename, "r") as f:
                lines = [line.rstrip("\n") for line in f.readlines()]
        except FileNotFoundError:
            print(f"Erreur: le fichier {filename} est introuvable")
            return
        return lines

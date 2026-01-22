#!/usr/bin/env python3
# File: my_renderer.py
# Author: ebabun <ebabun@student.42belgium.be>
# Created: 2026/01/22 12:35:09
# Updated: 2026/01/22 12:35:09

from mlx import Mlx
from typing import List

class MazeRenderer:
    """A class holding the renderer's specifications."""
    
    COLOR_WALL = 0x00CC00
    COLOR_BG = 0x1A1A1A 
    COLOR_42 = 0x00CC00
    WALL_THICKNESS = 1

    def __init__(self, output_file: str) -> None:
        """
        Initialize MLX renderer.
        
        Args:
            output_file: Path to the maze file from MazeGenerator
            
        Attributes:
            cell_size: size of a cell in pixels
            width, height: size of the window
            img_width, img_height: size of the maze
            content: maze data
            ptr: MLX instance
            win_ptr: Window identifier
            img_ptr: Image identifier
        """
        # Initialize MLX
        self.m = Mlx()
        self.ptr = self.m.mlx_init()
 
        # Extract data from output file
        info: tuple = self.extract_info(output_file)
        content, maze_w, maze_h = info
        self.content = content

        # Get screen dimensions
        ret, screen_width, screen_height = self.m.mlx_get_screen_size(self.ptr)
        print(f"Screen size = {screen_width} x {screen_height}")
        if ret != 0:
            screen_width, screen_height = 1920, 1080
            print("Warning: Using default screen size")

        # Calculate optimal cell size ACCOUNTING FOR EXTRA SPACE
        # set default to 30
        self.cell_size = 30

        # Calculate usable screen space (90% of total scren size)
        usable_width = int(screen_width * 0.90)
        usable_height = int(screen_height * 0.90)

        # Determine which dimension gets the extra space
        # The extra space is 300 pixels wide
        # Remove 300 pixels from the available space for the maze image
        if maze_h > maze_w:
            # Tall maze: extra space goes vertically
            # Available space for maze image = usable_width - 300 pixels
            available_width = usable_width - 300
            available_height = usable_height
        else:
            # Wide maze: extra space goes horizontaly
            available_width = usable_width
            available_height = usable_height - 200

        # Check if maze fits with default cell size
        if (self.cell_size * maze_w) > available_width:
            self.cell_size = int(available_width // maze_w)

        if (self.cell_size * maze_h) > available_height:
            self.cell_size = min(self.cell_size, int(available_height // maze_h))

        # Enforce minimum
        if self.cell_size < 12:
            print("Warning: Maze is too large!")
            print("Consider generating a smaller maze for better visibility")
            print("Recommended maze size: 120x60")
            self.cell_size = 12

        # Calculate maze image size
        self.img_width = maze_w * self.cell_size
        self.img_height = maze_h * self.cell_size

        # Calculate window size with the extra space
        # use +300 instead of * 1.60 for a consistent empty space
        if maze_h > maze_w:
            # Tall maze: add vertical space
            self.height = self.img_height
            self.width = int(self.img_width + 300)
        else:
            # Wide/square maze: add horiz space
            self.width = self.img_width
            self.height = int(self.img_height + 200)

        # Create window and image
        self.win_ptr = self.m.mlx_new_window(
            self.ptr, self.width, self.height, "=== A-maze-ing ==="
        )
        self.img_ptr = self.m.mlx_new_image(
            self.ptr, self.img_width, self.img_height
        )

        # Additional colors
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
        start_y = i * self.cell_size
        start_x = j * self.cell_size

        for y in range(start_y, start_y + self.cell_size):
            for x in range(start_x, start_x + self.cell_size):
                self.my_mlx_pixel_put(data, x, y, color, size_line, bpp)

    def draw_north_wall(self, data, size_line, bpp, i, j):
        start_y = i * self.cell_size
        start_x = j * self.cell_size
        end_x = start_x + self.cell_size
        wall = self.COLOR_WALL
        t = self.WALL_THICKNESS

        for y in range(start_y, start_y + t):
            for x in range(start_x, end_x):
                self.my_mlx_pixel_put(data, x, y, wall, size_line, bpp)

    def draw_south_wall(self, data, size_line, bpp, i, j):
        start_x = j * self.cell_size
        end_y = i * self.cell_size + self.cell_size
        end_x = start_x + self.cell_size
        wall = self.COLOR_WALL
        t = self.WALL_THICKNESS

        for y in range(end_y - t, end_y):
            for x in range(start_x, end_x):
                self.my_mlx_pixel_put(data, x, y, wall, size_line, bpp)

    def draw_east_wall(self, data, size_line, bpp, i, j):
        start_y = i * self.cell_size
        end_y = start_y + self.cell_size
        end_x = j * self.cell_size + self.cell_size
        wall = self.COLOR_WALL
        t = self.WALL_THICKNESS

        for x in range(end_x - t, end_x):
            for y in range(start_y, end_y):
                self.my_mlx_pixel_put(data, x, y, wall, size_line, bpp)

    def draw_west_wall(self, data, size_line, bpp, i, j):
        start_y = i * self.cell_size
        start_x = j * self.cell_size
        end_y = start_y + self.cell_size
        wall = self.COLOR_WALL
        t = self.WALL_THICKNESS

        for x in range(start_x, start_x + t):
            for y in range(start_y, end_y):
                self.my_mlx_pixel_put(data, x, y, wall, size_line, bpp)

    def create_image(self):
        data, bpp, size_line, endian = self.m.mlx_get_data_addr(self.img_ptr)

        # Draw cases
        for i, line in enumerate(self.content):
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

    def extract_info(self, filename: str) -> tuple:
        """Extract the content of the output file."""
        try:
            with open(filename, "r") as f:
                lines = [line.rstrip("\n") for line in f.readlines()]
        except (FileNotFoundError, PermissionError) as e:
            print(f"Error: {e}")
            return ([], 0, 0)
        
        if not lines:
            print("Error: Empty maze file")
            return ([], 0, 0)
        
        height: int = len(lines)
        width: int = len(lines[0]) if lines else 0
        
        return (lines, width, height)

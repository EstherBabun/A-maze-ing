#!/usr/bin/env python3
# File: maze_renderer.py
# Author: ebabun <ebabun@student.42belgium.be>
# Author: mmeurer <mmeurer@student.42belgium.be>
# Created: 2026/01/22 12:35:09
# Updated: 2026/01/22 12:35:09

from mlx import Mlx
from typing import List, Tuple, Dict, Optional
from maze_generator import MazeGenerator

class MazeRenderer:
    """A class holding the renderer's specifications."""
    
    YELLOW = 0xFFFF00
    BLUE = 0x00FFFF
    OFFSET: Dict[str, tuple] = {
            "N": (0, -1),
            "S": (0, 1),
            "E": (1, 0),
            "W": (-1, 0)
            }

    def __init__(self, config: Optional[str] = None) -> None:
        """
        Initialize MLX renderer.
        
        Args:
            output_file: Path to the maze file from MazeGenerator
            
        Attributes:
            content: parsed content of maze output file
            width, height: size of the window
            img_width, img_height: size of the maze img
            cell_size: size of a cell in pixels
            wall_thickness: thickness of the walls in pixels
            ptr: MLX instance
            win_ptr: Window identifier
            img_ptr: Image identifier
        """
        # Initialize MLX
        self.m = Mlx()
        self.ptr = self.m.mlx_init()
        self.maze_gen: MazeGenerator = None
 
        # declare maze data
        self.config_file: str = ""
        self.maze_w: int = 0
        self.maze_h: int = 0
        self.content: List[str] = []
        self.entry = (0, 0)
        self.exit = (0, 0)
        self.coord_path: List[Tuples[int, int]] = []

        # create a maze
        self.create_maze(config)

        # declare dimensions for MLX objects
        self.window_w: int = 0
        self.window_h: int = 0
        self.margin: Tuple[str, int] = ("", 0)
        self.img_w: int = 0
        self.img_h: int = 0
        self.cell_size: int = 30
        self.wall_thickness: int = 3

        # Additional colors and color counter
        green: Dict[str, int] = {
                "wall": 0x00CC00,
                "path": 0x106050
                }
        cyan: Dict[str, int] = {
                "wall": 0x00ECFF,
                "path": 0x156055
                }
        pink: Dict[str, int] = {
                "wall": 0xFF15F0,
                "path": 0x850065
                }
        red: Dict[str, int] = {
                "wall": 0xFF0020,
                "path": 0x506020
                }
        orange: Dict[str, int] = {
                "wall": 0xFF7F50,
                "path": 0x852520
                }
        # original = 0x00CC00
        # red = 0xFF0000
        # orange = 0xFF7F50
        # pink = 0xFF10F0
        self.color_palettes: List[Dict[str,int]] = [green, cyan, pink, orange] 
        self.palette_names: List[str] = ["green", "cyan", "pink", "orange"]
        self.color_idx: int = 0
        self.color_wall = green["wall"]
        self.color_bg = 0x1A1A1A
        self.color_path = green["path"]
        self.color_cursor = 0x1F1F1F

        # create configure and launch renderer
        self.config_launch_renderer()

    def convert_path(self, path) -> None:
        """Convert directions to coordinates."""
        coord_path: List[Tuple[int, int]] = []
        x, y = self.entry
        for direction in path:
            ox, oy = self.OFFSET[direction]
            next_coord = (x + ox, y + oy)
            coord_path.append(next_coord)
            x, y = next_coord
        self.coord_path = coord_path[:-1]

    def create_maze(self, config: str) -> None:
        self.config_file = config
        maze_gen = MazeGenerator(config)
        self.maze_gen = maze_gen
        # generate maze
        maze_gen.generate_maze()
        # store maze data
        self.maze_w = maze_gen.cols
        self.maze_h = maze_gen.rows
        self.content = [
                line.strip() for line
                in maze_gen.hex_repr.split("\n")
                if line.strip()
                ]
        self.entry = maze_gen.entry
        self.exit = maze_gen.exit
        self.convert_path(maze_gen.path)
        self.toggle_path: bool = False

    def set_cell_size_and_wall_thickness(self) -> None:
        """Calculate cell size according to screen and maze size."""
        # Get screen dimensions or switch to default on failure
        ret, screen_width, screen_height = self.m.mlx_get_screen_size(self.ptr)
        if ret != 0:
            screen_width, screen_height = 1920, 1080
            print("Warning: Using default screen size")

        # Calculate usable screen space (90% of total scren size)
        usable_width: int = int(screen_width * 0.90)
        usable_height: int = int(screen_height * 0.90)

        # Determine which dimension gets the extra space
        # The extra space is 300(width) or 200(height) pixels wide
        # Remove those pixels from the available space for the maze image
        if self.maze_h > self.maze_w:
            # Tall maze: extra space goes to the right
            # Available space for maze image = usable_width - 300 pixels
            self.margin = ("right", 300)
            available_width = usable_width - self.margin[1]
            available_height = usable_height
        else:
            # Wide maze: extra space goes to the bottom
            # Available space for maze image = usable_height - 200 pixels
            self.margin = ("bot", 200)
            available_width = usable_width
            available_height = usable_height - self.margin[1]

        # Calculate optimal cell size ACCOUNTING FOR EXTRA SPACE
        if (self.cell_size * self.maze_w) > available_width:
            self.cell_size = int(available_width // self.maze_w)

        if (self.cell_size * self.maze_h) > available_height:
            self.cell_size = min(self.cell_size, int(available_height // self.maze_h))

        # Enforce minimum
        if self.cell_size < 12:
            print("Warning: Maze is too large!")
            print("Consider generating a smaller maze for better visibility")
            print("Recommended maze size: 120x60\n")
            self.cell_size = 12

        # adapt wall thickness to cell size
        self.wall_thickness = self.cell_size // 10

        # debug
        # print(f"Cell size: {self.cell_size}")
        # print(f"Wall thickness: {self.wall_thickness}")

    def set_window_and_img_size(self) -> None:
        """Calculate window and image sizes."""
        # Calculate maze image size
        self.img_w = self.maze_w * self.cell_size
        self.img_h = self.maze_h * self.cell_size

        # Calculate window size with the extra space
        # use +300 instead of * 1.60 for a consistent empty space
        if self.margin[0] == "right":
            # Tall maze: add vertical space
            self.window_h = self.img_h
            self.window_w = int(self.img_w + self.margin[1])
        else:
            # Wide/square maze: add horiz space
            self.window_w = self.img_w
            self.window_h = int(self.img_h + self.margin[1])

    def config_launch_renderer(self) -> None:
        self.set_cell_size_and_wall_thickness()
        self.set_window_and_img_size()

        # Create window and images
        self.win_ptr = self.m.mlx_new_window(
            self.ptr, self.window_w, self.window_h, "=== A-maze-ing ==="
        )
        self.img_ptr = self.m.mlx_new_image(
            self.ptr, self.img_w, self.img_h
        )
        # store img data in the renderer object for faster results
        self.img_data = self.m.mlx_get_data_addr(self.img_ptr)


        self.define_mlx_operations()

    def my_string_put(self, offset: int, color: int, msg: str) -> None: 
        if self.margin[0] == "bot":
            self.m.mlx_string_put(self.ptr, self.win_ptr, 15, self.img_h + offset, color, msg)
        else:
            self.m.mlx_string_put(self.ptr, self.win_ptr, self.img_w + 15, offset, color, msg)

    def put_commands(self) -> None:
        self.my_string_put(10, 0xFFFF00, "Start")
        self.my_string_put(30, 0x00FFFF, "Finish")
        self.my_string_put(50, 0xFFFFFF, "s: toggle solution")
        self.my_string_put(70, 0xFFFFFF, "c: toggle colors")
        self.my_string_put(90, 0xFFFFFF, "r: generate new maze")
        self.my_string_put(110, 0xFFFFFF, "q: quit")

    def my_mlx_pixel_put(self, x, y, color):
        """Fast pixel writing to image buffer."""
        data, bpp, size_line, endian = self.img_data
        if x >= 0 and y >= 0:  # Basic bounds checking
            offset = y * size_line + x * (bpp // 8)
            # extract RGB components
            r = (color >> 16) & 0xFF
            g = (color >> 8) & 0xFF
            b = color & 0xFF
            # write bytes in BGR order
            data[offset] = b
            data[offset + 1] = g
            data[offset + 2] = r
            data[offset + 3] = 255

    def draw(self, start_x, end_x, start_y, end_y, color) -> None:
        """draw pixels in specified area."""
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                self.my_mlx_pixel_put(x, y, color)

    def draw_cell(self, i, j, color):
        """Fast pixel writing to image buffer."""
        start_x = j * self.cell_size
        end_x = start_x + self.cell_size
        start_y = i * self.cell_size
        end_y = start_y + self.cell_size
        self.draw(start_x, end_x, start_y, end_y, color)

    def draw_entry_exit(self, i, j, color) -> None:
        fraction: int = self.cell_size // 3
        start_x = j * self.cell_size + fraction
        end_x = start_x + fraction
        start_y = i * self.cell_size + fraction
        end_y = start_y + fraction
        self.draw(start_x, end_x, start_y, end_y, color)

    def draw_north_wall(self, i, j, color):
        start_x = j * self.cell_size
        end_x = start_x + self.cell_size
        start_y = i * self.cell_size
        end_y = start_y + self.wall_thickness
        self.draw(start_x, end_x, start_y, end_y, color)

    def draw_south_wall(self, i, j, color):
        start_x = j * self.cell_size
        end_x = start_x + self.cell_size
        end_y = i * self.cell_size + self.cell_size
        start_y = end_y - self.wall_thickness
        self.draw(start_x, end_x, start_y, end_y, color)

    def draw_east_wall(self, i, j, color):
        end_x = j * self.cell_size + self.cell_size
        start_x = end_x - self.wall_thickness
        start_y = i * self.cell_size
        end_y = start_y + self.cell_size
        self.draw(start_x, end_x, start_y, end_y, color)

    def draw_west_wall(self, i, j, color):
        start_x = j * self.cell_size
        end_x = start_x + self.wall_thickness
        start_y = i * self.cell_size
        end_y = start_y + self.cell_size
        self.draw(start_x, end_x, start_y, end_y, color)

    def create_image(self):
        # Draw cases
        for i, line in enumerate(self.content):
            for j, cell in enumerate(line):
                if cell == 'F':
                    self.draw_cell(i, j, self.color_wall)
                elif self.toggle_path:
                    if (j, i) in self.coord_path:
                        self.draw_cell(i, j, self.color_path)
                else:
                    self.draw_cell(i, j, self.color_bg)
                # Draw walls
                if cell in "13579BD":
                    self.draw_north_wall(i, j, self.color_wall)
                if cell in "4567CDE":
                    self.draw_south_wall(i, j, self.color_wall)
                if cell in "2367ABE":
                    self.draw_east_wall(i, j, self.color_wall)
                if cell in "89ABCDE":
                    self.draw_west_wall(i, j, self.color_wall)
                if (j, i) == self.entry: 
                    self.draw_entry_exit(i, j, self.BLUE)
                if (j, i) == self.exit:
                    self.draw_entry_exit(i, j, self.YELLOW)

        # Display the image
        self.m.mlx_put_image_to_window(
            self.ptr, self.win_ptr, self.img_ptr, 0, 0)

    def mymouse(self, button, x, y, mystuff):
        print(f"Got mouse event! button {button} at {x},{y}.")
    
    def toggle_solution(self, color) -> None:
        # Draw(COLOR_PATH) or erase(COLOR_BG) solution
        for i, line in enumerate(self.content):
            for j, cell in enumerate(line):
                if (j, i) in self.coord_path:
                    self.draw_cell(i, j, color)
                    if cell in "13579BD":
                        self.draw_north_wall(i, j, self.color_wall)
                    if cell in "4567CDE":
                        self.draw_south_wall(i, j, self.color_wall)
                    if cell in "2367ABE":
                        self.draw_east_wall(i, j, self.color_wall)
                    if cell in "89ABCDE":
                        self.draw_west_wall(i, j, self.color_wall)

        # Display the image
        self.m.mlx_put_image_to_window(
            self.ptr, self.win_ptr, self.img_ptr, 0, 0)

    def toggle_colors(self) -> None:
        for i, line in enumerate(self.content):
            for j, cell in enumerate(line):
                if (j, i) in self.coord_path and self.toggle_path:
                    self.draw_cell(i, j, self.color_path)
                if cell == 'F':
                    self.draw_cell(i, j, self.color_wall)
                if cell in "13579BD":
                    self.draw_north_wall(i, j, self.color_wall)
                if cell in "4567CDE":
                    self.draw_south_wall(i, j, self.color_wall)
                if cell in "2367ABE":
                    self.draw_east_wall(i, j, self.color_wall)
                if cell in "89ABCDE":
                    self.draw_west_wall(i, j, self.color_wall)

        # Display the image
        self.m.mlx_put_image_to_window(
            self.ptr, self.win_ptr, self.img_ptr, 0, 0)

    def mykey(self, keynum, param):
        #navigation: Dict[str, int] = {
        #        65361: "W",
        #        65364: "S",
        #        65363: "E",
        #        65362: "N"
        #        }
        #print(f"Got keynum {keynum}")
        # s key
        if keynum == 115:
            self.toggle_path = not self.toggle_path
            if self.toggle_path:
                print("Showing solution")
                self.toggle_solution(self.color_path)
            else:
                print("Hiding solution")
                self.toggle_solution(self.color_bg)
        # c key
        elif keynum == 99:
            next_idx = (self.color_idx + 1) % len(self.color_palettes)
            self.color_idx = next_idx
            palette = self.color_palettes[next_idx]
            self.color_wall = palette["wall"]
            self.color_path = palette["path"]
            self.toggle_colors()
            print(f"Switched to {self.palette_names[next_idx]} color palette")
        # r key
        elif keynum == 114:
            print("Generating new maze...")
            self.m.mlx_clear_window(self.ptr, self.win_ptr)
            self.m.mlx_destroy_image(self.ptr, self.img_ptr)
            self.m.mlx_destroy_window(self.ptr, self.win_ptr)
            self.m.mlx_loop_exit(self.ptr)
            # create new maze
            self.create_maze(self.config_file)
            # create configure and launch renderer
            self.config_launch_renderer()
        #elif keynum in navigation.keys():
        #        self.navigate(navigation[keynum])
        elif keynum == 113:
            self.gere_close(None)
             
    def gere_close(self, dummy):
        self.m.mlx_loop_exit(self.ptr)

    def define_mlx_operations(self) -> None:
        """Define series of operations to perform."""
        self.m.mlx_clear_window(self.ptr, self.win_ptr)
        self.put_commands()
        self.create_image()
        self.m.mlx_mouse_hook(self.win_ptr, self.mymouse, None)
        self.m.mlx_key_hook(self.win_ptr, self.mykey, None)
        self.m.mlx_hook(self.win_ptr, 33, 0, self.gere_close, None)
        self.m.mlx_loop(self.ptr)

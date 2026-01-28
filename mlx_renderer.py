#!/usr/bin/env python3
# File: maze_renderer.py
# Author: ebabun <ebabun@student.42belgium.be>
# Author: mmeurer <mmeurer@student.42belgium.be>
# Created: 2026/01/22 12:35:09
# Updated: 2026/01/22 12:35:09

from __future__ import annotations
from maze_generator import MazeGenerator
from mlx import Mlx
from typing import List, Tuple, Dict, Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from cell import CELL

class MlxRenderer:
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
        self.grid: List[List[Cell]] = []
        self.entry = (0, 0)
        self.exit = (0, 0)
        self.solution: bool = False
        self.soluce_path: List[Tuples[int, int]] = []

        # declare current coordinates and path for navigation
        self.current_cell: Cell = None
        self.navigation_path: List[Tuple[int, int]] = []

        # create a maze
        self.create_maze(config)

        # declare dimensions for MLX objects
        self.screen_w: int = 0
        self.screen_h: int = 0
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
        self.color_cursor = 0x005080


        # create configure and launch renderer
        self.config_launch_renderer()

    def convert_soluce_path(self, path) -> None:
        """Convert directions to coordinates."""
        soluce_path: List[Tuple[int, int]] = []
        x, y = self.entry
        for direction in path:
            ox, oy = self.OFFSET[direction]
            next_coord = (x + ox, y + oy)
            soluce_path.append(next_coord)
            x, y = next_coord
        self.soluce_path = soluce_path[:-1]

    def create_maze(self, config: str) -> None:
        self.config_file = config
        maze_gen = MazeGenerator(config)
        self.maze_gen = maze_gen
        # generate maze
        maze_gen.generate_maze()
        # store maze data
        self.maze_w = maze_gen.cols
        self.maze_h = maze_gen.rows
        self.grid = maze_gen.grid
        self.entry = maze_gen.entry
        self.exit = maze_gen.exit
        self.convert_soluce_path(maze_gen.path)
        self.solution: bool = False
        self.current_cell = maze_gen.entry_cell
        self.navigation_path: List[Tuple[int, int]] = [maze_gen.entry]

    def set_cell_size_and_wall_thickness(self) -> None:
        """Calculate cell size according to screen and maze size."""
        # Get screen dimensions or switch to default on failure
        ret, screen_width, screen_height = self.m.mlx_get_screen_size(self.ptr)
        if ret != 0:
            screen_width, screen_height = 1920, 1080
            print("Warning: Using default screen size")
        
        # store screen dimensions as attributes
        self.screen_w = screen_width
        self.screen_h = screen_height

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

        # enforce minimum window size 
        if self.window_h < 180:
            self.window_h = 180
        if self.window_w < 240:
            self.window_w = 240

        # Warning against oversized window
        if self.window_h >= self.screen_h or self.window_w >= self.screen_w:
            print("Warning: Maze is too large!")
            print("Consider generating a smaller maze for better visibility")
            print("Recommended maze size: 120x60\n")

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
        self.my_string_put(50, 0xFFFFFF, "Arrow keys: navigate")
        self.my_string_put(70, 0xFFFFFF, "d: delete path")
        self.my_string_put(90, 0xFFFFFF, "c: toggle colors")
        self.my_string_put(110, 0xFFFFFF, "s: toggle solution")
        self.my_string_put(130, 0xFFFFFF, "r: generate new maze")
        self.my_string_put(150, 0xFFFFFF, "q: quit")

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

    def draw_cell(self, x, y, color):
        """Fast pixel writing to image buffer."""
        start_x = x * self.cell_size
        end_x = start_x + self.cell_size
        start_y = y * self.cell_size
        end_y = start_y + self.cell_size
        self.draw(start_x, end_x, start_y, end_y, color)

    def draw_north_wall(self, x, y, color):
        start_x = x * self.cell_size
        end_x = start_x + self.cell_size
        start_y = y * self.cell_size
        end_y = start_y + self.wall_thickness
        self.draw(start_x, end_x, start_y, end_y, color)

    def draw_south_wall(self, x, y, color):
        start_x = x * self.cell_size
        end_x = start_x + self.cell_size
        end_y = y * self.cell_size + self.cell_size
        start_y = end_y - self.wall_thickness
        self.draw(start_x, end_x, start_y, end_y, color)

    def draw_east_wall(self, x, y, color):
        end_x = x * self.cell_size + self.cell_size
        start_x = end_x - self.wall_thickness
        start_y = y * self.cell_size
        end_y = start_y + self.cell_size
        self.draw(start_x, end_x, start_y, end_y, color)

    def draw_west_wall(self, x, y, color):
        start_x = x * self.cell_size
        end_x = start_x + self.wall_thickness
        start_y = y * self.cell_size
        end_y = start_y + self.cell_size
        self.draw(start_x, end_x, start_y, end_y, color)

    def draw_walls(self, x: int, y: int) -> None:
        """Draw all walls of the cell at given coordinates."""
        cell: Cell = self.maze_gen.get_cell(x, y)
        if cell is not None:
            if cell.walls["W"] == 1:
                self.draw_west_wall(x, y, self.color_wall)
            if cell.walls["S"] == 1:
                self.draw_south_wall(x, y, self.color_wall)
            if cell.walls["E"] == 1:
                self.draw_east_wall(x, y, self.color_wall)
            if cell.walls["N"] == 1:
                self.draw_north_wall(x, y, self.color_wall)

    def draw_entry_exit(self, x, y) -> None:
        fraction: int = self.cell_size // 3
        start_x = x * self.cell_size + fraction
        end_x = start_x + fraction
        start_y = y * self.cell_size + fraction
        end_y = start_y + fraction
        if (x, y) == self.entry:
            self.draw(start_x, end_x, start_y, end_y, self.BLUE)
        elif (x, y) == self.exit:
            self.draw(start_x, end_x, start_y, end_y, self.YELLOW)

    def create_image(self):
        # Draw cases
        for row in self.grid:
            for cell in row:
                x, y = cell.coord
                # draw cells
                if cell._is_42:
                    self.draw_cell(x, y, self.color_wall)
                elif self.solution:
                    if (x, y) in self.soluce_path:
                        self.draw_cell(x, y, self.color_path)
                else:
                    self.draw_cell(x, y, self.color_bg)
                # Draw walls
                self.draw_walls(x, y)
                # Draw entry and exit
                if (x, y) == self.entry or (x, y) == self.exit: 
                    self.draw_entry_exit(x, y,)

        # Display the image
        self.m.mlx_put_image_to_window(
            self.ptr, self.win_ptr, self.img_ptr, 0, 0)

    def mymouse(self, button, x, y, mystuff):
        print(f"Got mouse event! button {button} at {x},{y}.")
    
    def toggle_solution(self, color) -> None:
        # Draw(COLOR_PATH) or erase(COLOR_BG) solution
        for row in self.grid:
            for cell in row:
                x, y = cell.coord
                if (x, y) in self.soluce_path:
                    self.draw_cell(x, y, color)
                    if not self.solution and (x, y) in self.navigation_path:
                        self.draw_cell(x, y, self.color_cursor)
                    self.draw_walls(x, y)

        # Display the image
        self.m.mlx_put_image_to_window(
            self.ptr, self.win_ptr, self.img_ptr, 0, 0)

    def toggle_colors(self) -> None:
        for row in self.grid:
            for cell in row:
                x, y = cell.coord
                if (x, y) in self.navigation_path and (x, y) != self.entry:
                    self.draw_cell(x, y, self.color_cursor)
                if self.solution and (x, y) in self.soluce_path:
                    self.draw_cell(x, y, self.color_path)
                if cell._is_42:
                    self.draw_cell(x, y, self.color_wall)
                self.draw_walls(x, y)

        # Display the image
        self.m.mlx_put_image_to_window(
            self.ptr, self.win_ptr, self.img_ptr, 0, 0)


    def delete_navigation_path(self) -> None:
        """Remove the entire navigation path."""
        for (x, y) in self.navigation_path:
            if (x, y) != self.entry:
                if self.solution and (x, y) not in self.soluce_path:
                    self.draw_cell(x, y, self.color_bg)
                    self.draw_walls(x, y)
                else:
                    self.draw_cell(x, y, self.color_bg)
                    self.draw_walls(x, y)
        # reset starting point and navigation path
        self.current_cell = self.maze_gen.entry_cell
        self.navigation_path = [self.entry]

        # Display the image
        self.m.mlx_put_image_to_window(
            self.ptr, self.win_ptr, self.img_ptr, 0, 0)

    def navigate(self, direction) -> None:
        """Navigate in the maze, coloring cell in given direction."""
        current = self.current_cell
        next_cell = current.get_neighbor(direction)
        if next_cell is not None and current.walls[direction] == 0:
            x, y = next_cell.coord
            if next_cell.coord == self.exit:
                return
            if next_cell.coord in self.navigation_path:
                idx = self.navigation_path.index(next_cell.coord)
                to_delete = self.navigation_path[idx + 1:]
                self.navigation_path = self.navigation_path[:idx + 1]
                for (dx, dy) in to_delete:
                    if self.solution and (dx, dy) in self.soluce_path:
                        self.draw_cell(dx, dy, self.color_path)
                    else:
                        self.draw_cell(dx, dy, self.color_bg)
                    if (x, y) == self.entry or (x, y) == self.exit: 
                        self.draw_entry_exit(x, y,)
                    self.draw_walls(dx, dy)
            else:
                if self.solution and (x, y) in self.soluce_path:
                    self.draw_cell(x, y, self.color_path)
                else:
                    self.draw_cell(x, y, self.color_cursor)
                self.draw_walls(x, y)
                self.navigation_path.append(next_cell.coord)
            self.current_cell = next_cell

        # Display the image
        self.m.mlx_put_image_to_window(
            self.ptr, self.win_ptr, self.img_ptr, 0, 0)

    def mykey(self, keynum, param):
        """Record key events and trigger associated method."""
        # debug
        # print(f"Got keynum {keynum}")
        navigation: Dict[str, int] = {
                65361: "W",
                65364: "S",
                65363: "E",
                65362: "N"
                }

        # s key -> toggle solution
        if keynum == 115:
            self.solution = not self.solution
            if self.solution:
                print("Showing solution")
                self.toggle_solution(self.color_path)
            else:
                print("Hiding solution")
                self.toggle_solution(self.color_bg)

        # c key -> toggle colors
        elif keynum == 99:
            next_idx = (self.color_idx + 1) % len(self.color_palettes)
            self.color_idx = next_idx
            palette = self.color_palettes[next_idx]
            self.color_wall = palette["wall"]
            self.color_path = palette["path"]
            self.toggle_colors()
            print(f"Switched to {self.palette_names[next_idx]} color palette")

        # r key -> re-generate new maze
        elif keynum == 114:
            print("Generating new maze...")
            self.m.mlx_clear_window(self.ptr, self.win_ptr)
            self.m.mlx_destroy_image(self.ptr, self.img_ptr)
            self.m.mlx_destroy_window(self.ptr, self.win_ptr)
            self.m.mlx_loop_exit(self.ptr)
            # create new maze
            self.create_maze(self.config_file)
            self.navigation_path = [self.entry]
            # create configure and launch renderer
            self.config_launch_renderer()

        # arrow keys -> create navigation path
        elif keynum in navigation.keys():
                self.navigate(navigation[keynum])
        # d key -> delete navigation path
        elif keynum == 100:
            self.delete_navigation_path()
        # q key
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

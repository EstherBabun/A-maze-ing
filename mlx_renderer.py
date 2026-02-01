#!/usr/bin/env python3
# File: maze_renderer.py
# Author: ebabun <ebabun@student.42belgium.be>
# Author: mmeurer <mmeurer@student.42belgium.be>
# Created: 2026/01/22 12:35:09
# Updated: 2026/01/22 12:35:09

"""Module to render a maze with mlx graphics library."""

from maze_generator import MazeGenerator
from mlx import Mlx
from typing import List, Tuple, Dict, Optional
from ctypes import c_void_p, POINTER, c_char


class MlxRenderer:
    """A class holding the renderer's specifications."""

    YELLOW = 0xFFFF00
    BLUE = 0x00FFFF

    def __init__(self, maze: MazeGenerator) -> None:
        """
        Initialize MLX renderer.

        Args:
            config (str | None): Path to the config file if there is one

        Attributes:
            mlx instance:
            m (Mlx): Mlx instance
            ptr (c_void_p): Mlx instance pointer

            maze data:
            maze_gen (MazeGenerator): MazeGenerator instance
            maze_w (int): width of the maze
            maze_h (int): height of the maze
            grid(list(list(Cell))): structure of the maze
            entry (tuple(int)): entry coordinates
            exit (tuple(int)): exit coordinates
            solution (bool): flag to know if solution path is shown or hidden
            soluce_path (list(tuple(int, int)): coordinates of the soluce path
            current_cell (Cell): current cell of the user's navigation
            navigation_path (list(tuple(int, int)): coordinates of navigation

            mlx data:
            screen_w (int): width of the screen in pixels
            screen_h (int): height of the screen in pixels
            window_w (int): width of the window (including optional margin)
            window_h (int): height of the window (including optional margin)
            margin (tuple(str, int)): margin for the commands strings
            cell_size: size of a cell in pixels (default=30)
            wall_thickness: thickness of the walls in pixels (default=3)
            img_w (int): width of the image (cell_size * maze_w)
            img_h (int): height of the image (cell_size * maze_h)

            win_ptr (c_void_p): Window identifier
            img_ptr (c_void_p): Image identifier
            img_data (Tuple(POINTER(c_char), int, int, int): the image data
        """
        # Initialize MLX
        self.m = Mlx()
        self.ptr = self.m.mlx_init()

        # Initialize maze
        self.maze: MazeGenerator = maze

        # declare attributes for solution toggling
        self.solution: bool = False
        self.convert_soluce_path()

        # declare current coordinates and path for navigation
        self.current_cell: Cell = self.maze.entry_cell
        self.navigation_path: List[Tuple[int, int]] = [self.maze.entry]

        # declare MLX data
        self.screen_w: int = 0
        self.screen_h: int = 0
        self.window_w: int = 0
        self.window_h: int = 0
        self.margin: Tuple[str, int] = ("", 0)
        self.cell_size: int = 30
        self.wall_thickness: int = 3
        self.img_w: int = 0
        self.img_h: int = 0
        self.win_ptr: c_void_p
        self.img_ptr: c_void_p
        self.img_data: Tuple[POINTER(c_char), int, int, int]

        # colors and color counter
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
                "path": 0x700550
                }
        orange: Dict[str, int] = {
                "wall": 0xFF7F50,
                "path": 0x852520
                }
        self.color_palettes: List[Dict[str, int]] = [
                green, cyan, pink, orange, red
                ]
        self.palette_names: List[str] = [
                "green", "cyan", "pink", "orange", "red"
                ]
        self.color_idx: int = 0
        self.color_wall = green["wall"]
        self.color_bg = 0x1A1A1A
        self.color_path = green["path"]
        self.color_cursor = 0x005080

        # create and configure renderer
        self.configure_renderer()
        # execute rendering operations
        self.display()

    def convert_soluce_path(self) -> None:
        """Convert directions to coordinates."""
        soluce_path: List[Tuple[int, int]] = []
        x, y = self.maze.entry
        for direction in self.maze.path:
            ox, oy = MazeGenerator.offset[direction]
            next_coord = (x + ox, y + oy)
            soluce_path.append(next_coord)
            x, y = next_coord
        self.soluce_path = soluce_path[:-1]

    def create_maze(self) -> bool:
        """Create maze instance and initialize maze data."""
        new_maze = MazeGenerator(self.maze._config_file)
        self.maze = new_maze
        self.convert_soluce_path()
        self.solution: bool = False
        self.current_cell = self.maze.entry_cell
        self.navigation_path = [self.maze.entry]

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
        if self.maze.rows > self.maze.cols:
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
        if (self.cell_size * self.maze.cols) > available_width:
            self.cell_size = int(available_width // self.maze.cols)

        if (self.cell_size * self.maze.rows) > available_height:
            self.cell_size = min(
                    self.cell_size, int(available_height // self.maze.rows)
                    )

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
        self.img_w = self.maze.cols * self.cell_size
        self.img_h = self.maze.rows * self.cell_size

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

    def configure_renderer(self) -> None:
        """Configure renderer attributes based on maze data."""
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

    def my_string_put(self, offset: int, color: int, msg: str) -> None:
        """Put a string to the window."""
        if self.margin[0] == "bot":
            self.m.mlx_string_put(
                    self.ptr, self.win_ptr, 15, self.img_h + offset, color, msg
                    )
        else:
            self.m.mlx_string_put(
                    self.ptr, self.win_ptr, self.img_w + 15, offset, color, msg
                    )

    def put_commands(self) -> None:
        """Put all command strings to window."""
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
        """Draw pixels in specified area."""
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                self.my_mlx_pixel_put(x, y, color)

    def draw_cell(self, x, y, color):
        """Draw background pixels of a cell."""
        start_x = x * self.cell_size
        end_x = start_x + self.cell_size
        start_y = y * self.cell_size
        end_y = start_y + self.cell_size
        self.draw(start_x, end_x, start_y, end_y, color)

    def draw_north_wall(self, x, y, color):
        """Draw pixels of the north wall."""
        start_x = x * self.cell_size
        end_x = start_x + self.cell_size
        start_y = y * self.cell_size
        end_y = start_y + self.wall_thickness
        self.draw(start_x, end_x, start_y, end_y, color)

    def draw_south_wall(self, x, y, color):
        """Draw pixels of the south wall."""
        start_x = x * self.cell_size
        end_x = start_x + self.cell_size
        end_y = y * self.cell_size + self.cell_size
        start_y = end_y - self.wall_thickness
        self.draw(start_x, end_x, start_y, end_y, color)

    def draw_east_wall(self, x, y, color):
        """Draw pixels of the east wall."""
        end_x = x * self.cell_size + self.cell_size
        start_x = end_x - self.wall_thickness
        start_y = y * self.cell_size
        end_y = start_y + self.cell_size
        self.draw(start_x, end_x, start_y, end_y, color)

    def draw_west_wall(self, x, y, color):
        """Draw pixels of the west wall."""
        start_x = x * self.cell_size
        end_x = start_x + self.wall_thickness
        start_y = y * self.cell_size
        end_y = start_y + self.cell_size
        self.draw(start_x, end_x, start_y, end_y, color)

    def draw_walls(self, x: int, y: int) -> None:
        """Draw all walls of the given cell."""
        cell: Cell = self.maze.get_cell(x, y)
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
        """Draw entry square or exit square."""
        fraction: int = self.cell_size // 3
        start_x = x * self.cell_size + fraction
        end_x = start_x + fraction
        start_y = y * self.cell_size + fraction
        end_y = start_y + fraction
        if (x, y) == self.maze.entry:
            self.draw(start_x, end_x, start_y, end_y, self.BLUE)
        elif (x, y) == self.maze.exit:
            self.draw(start_x, end_x, start_y, end_y, self.YELLOW)

    def create_image(self):
        """Create original maze image."""
        # Draw cases
        for row in self.maze.grid:
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
                if (x, y) == self.maze.entry or (x, y) == self.maze.exit:
                    self.draw_entry_exit(x, y,)

        # Display the image
        self.m.mlx_put_image_to_window(
            self.ptr, self.win_ptr, self.img_ptr, 0, 0)

    def toggle_solution(self, color) -> None:
        """Toggle solution path on and off."""
        # Draw(COLOR_PATH) or erase(COLOR_BG) solution
        for row in self.maze.grid:
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
        """Toggle maze colors."""
        for row in self.maze.grid:
            for cell in row:
                x, y = cell.coord
                if (x, y) in self.navigation_path and (x, y) != self.maze.entry:
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
        """Delete the entire navigation path."""
        for (x, y) in self.navigation_path:
            if (x, y) != self.maze.entry:
                if self.solution and (x, y) not in self.soluce_path:
                    self.draw_cell(x, y, self.color_bg)
                    self.draw_walls(x, y)
                elif not self.solution:
                    self.draw_cell(x, y, self.color_bg)
                    self.draw_walls(x, y)
        # reset starting point and navigation path
        self.current_cell = self.maze.entry_cell
        self.navigation_path = [self.maze.entry]

        # Display the image
        self.m.mlx_put_image_to_window(
            self.ptr, self.win_ptr, self.img_ptr, 0, 0)

    def navigate(self, direction) -> None:
        """Navigate in the maze, coloring cell in given direction."""
        current = self.current_cell
        next_cell = self.maze.get_neighbor(current, direction)
        if next_cell is not None and current.walls[direction] == 0:
            x, y = next_cell.coord
            if next_cell.coord == self.maze.exit:
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
                    if (x, y) == self.maze.entry or (x, y) == self.maze.exit:
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
            print("\nGenerating new maze...")
            self.m.mlx_clear_window(self.ptr, self.win_ptr)
            self.m.mlx_destroy_image(self.ptr, self.img_ptr)
            self.m.mlx_destroy_window(self.ptr, self.win_ptr)
            self.m.mlx_loop_exit(self.ptr)
            # create new maze
            self.create_maze()
            # configure and launch renderer
            self.configure_renderer()
            self.display()

        # arrow keys -> create navigation path
        elif keynum in navigation.keys():
            self.navigate(navigation[keynum])
        # d key -> delete navigation path
        elif keynum == 100:
            self.delete_navigation_path()
        # q key
        elif keynum == 113:
            print("Bye! Thanks for playing ~")
            self.gere_close(None)

    def gere_close(self, dummy):
        """Close window with close button."""
        self.m.mlx_loop_exit(self.ptr)

    def display(self) -> None:
        """Define mlx operations to display the maze."""
        self.m.mlx_clear_window(self.ptr, self.win_ptr)
        self.put_commands()
        self.create_image()
        self.m.mlx_key_hook(self.win_ptr, self.mykey, None)
        self.m.mlx_hook(self.win_ptr, 33, 0, self.gere_close, None)
        self.m.mlx_loop(self.ptr)

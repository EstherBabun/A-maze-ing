#!/usr/bin/env python3
# File: my_maze.py
# Author: ebabun <ebabun@student.42belgium.be>
# Created: 2026/01/19 08:42:20
# Updated: 2026/01/19 08:42:21

"""Docstring to write."""

import sys
import random
from typing import Dict, List, Any, Optional


class Cell:
    """Class that holds the cell attributes in a 2D maze.

    Attributes:
        coord (tuple): the (x, y) coordinates or (col, row) coordinates
        walls (list): dict of the 4 wall status[W,S,E,N] (1=closed, 0=open)
        is_entry (bool): True if the cell is the entry
        is_exit (bool): True if the cell is the exit
        current (bool): True if this is the current cell
        visited (bool): True if the cell has been checked already
    """

    def __init__(self, x: int, y: int) -> None:
        """Initialise the attributes of a cell."""
        self.coord: tuple = (x, y)
        self.walls: Dict[str, int] = {"W": 1, "S": 1, "E": 1, "N": 1}
        self.is_entry: bool = False
        self.is_exit: bool = False
        self.visited: bool = False

    @property
    def hex_repr(self) -> str:
        """Convert the status of the walls to an hex representation."""
        # store binary representation of walls into a string
        binary_str = "".join(str(v) for v in self.walls.values())
        # convert string from binary to decimal with int(binary_str, 2)
        # convert to hex using format specifier :X
        return f"{int(binary_str, 2):X}"


class Maze:
    """A class for the maze attributes and methods."""

    offset: Dict[str, tuple] = {
            "N": (0, -1),
            "S": (0, 1),
            "E": (1, 0),
            "W": (-1, 0)
            }
    adjacent: Dict[str, str] = {"N": "S", "S": "N", "E": "W", "W": "E"}


    def __init__(self, config_file: Optional[str] = None) -> None:
        """Initialise the attributes of the maze with the default config."""
        # Set defaults first
        self.cols: int = 20
        self.rows: int = 10
        self.seed: int | None = None
        self.perfect: bool = True
        self.entry: tuple = (0, 0)
        self.exit: tuple = (19, 9)
        self.output_file = "maze.txt"

        # Track which settings came from config file
        custom: List[str] = []
        # Load config file if provided
        if config_file is not None:
            custom = self.load_config(config_file)
        else:
            print("No config file, switching to default settings.")
            self.print_config(custom)

        # Initialize remaining attributes
        self.tot_size: int = self.cols * self.rows
        self.path: str = ""
        self.grid: List[List[Cell]] = [[Cell(x, y) for x in range(self.cols)]
                                       for y in range(self.rows)]

    def print_config(self, custom: List[str]) -> None:
        """Print final settings of the maze."""
        print("\nMaze configuration:")
        config_items = {
            "WIDTH": self.cols,
            "HEIGHT": self.rows,
            "ENTRY": self.entry,
            "EXIT": self.exit,
            "SEED": self.seed,
            "PERFECT": self.perfect,
            "OUTPUT_FILE": self.output_file
        }

        for k, v in config_items.items():
            if k in custom:
                print(f"  {k}: {v}")
            else:
                print(f"  {k}: {v} (default)")

    def load_config(self, file: str) -> List[str]:
        """Parse the config file and update maze attributes. Returns list of custom keys."""
        custom: List[str] = []
        raw_config: Dict[str, str] = {}

        # Read and parse the config file
        raw_config = self._read_config_file(file)
        if raw_config is None:
            print("Switching to default settings")
            self.print_config(custom)
            return custom

        # Parse each configuration value
        custom = self._parse_config_values(raw_config)

        # Validate and adjust entry/exit points
        self._validate_entry_exit(custom)

        # Error message for "42" pattern if maze too small
        if self.cols < 9 or self.rows < 7:
            print("Error: Maze too small for “42” pattern")

        self.print_config(custom)
        return custom

    def _read_config_file(self, file: str) -> Dict[str, str] | None:
        """Read config file and return raw key-value pairs. Returns None on error."""
        try:
            with open(file, "r") as f:
                content: str = f.read()
                if content == '':
                    print(f"Config file is empty")
                    return None

                print(f"Loading settings from config file {file}...")
                raw_config: Dict[str, str] = {}

                for line in content.splitlines():
                    try:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            key, value = line.split('=', 1)
                            key = key.strip().upper()
                            raw_config[key] = value.strip()
                    except ValueError:
                        print(f'Error in line {line} - Expected syntax: "KEY=value"')
                        continue

                return raw_config

        except (FileNotFoundError, PermissionError) as e:
            print(f"Error: {e}")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None

    def _parse_config_values(self, raw_config: Dict[str, str]) -> List[str]:
        """Parse and validate each config value. Returns list of successfully parsed keys."""
        custom: List[str] = []

        for k, v in raw_config.items():
            try:
                if k == "WIDTH":
                    self.cols = int(v)
                    custom.append(k)
                elif k == "HEIGHT":
                    self.rows = int(v)
                    custom.append(k)
                elif k == "ENTRY":
                    self.entry = self._parse_coordinate(v, k)
                    custom.append(k)
                elif k == "EXIT":
                    self.exit = self._parse_coordinate(v, k)
                    custom.append(k)
                elif k == "PERFECT":
                    self.perfect = self._parse_boolean(v, k)
                    custom.append(k)
                elif k == "SEED":
                    self.seed = int(v)
                    custom.append(k)
                elif k == "OUTPUT_FILE":
                    self.output_file = v
                    custom.append(k)
                else:
                    print(
                            f"Error: Invalid keyword {k} - "
                            "Allowed: WIDTH, HEIGHT, ENTRY, "
                            "EXIT, OUTPUT_FILE, PERFECT, SEED"
                            )
            except Exception as e:
                print(f'Error in {k}: {e}\nSwitching to default value')

        return custom

    def _parse_coordinate(self, value: str, key: str) -> tuple:
        """Parse a coordinate string 'x,y' into a tuple."""
        coord_tuple = tuple(int(i.strip()) for i in value.split(','))
        if len(coord_tuple) != 2:
            raise ValueError(f'coordinates expect 2 values "x,y"')
        return coord_tuple

    def _parse_boolean(self, value: str, key: str) -> bool:
        """Parse a boolean string 'True' or 'False'."""
        if value.upper() == "TRUE":
            return True
        elif value.upper() == "FALSE":
            return False
        else:
            raise ValueError(f'boolean expects "True" or "False"')

    def _is_within_bounds(self, coord: tuple) -> bool:
        """Check if a coordinate is within maze bounds."""
        x, y = coord
        return 0 <= x < self.cols and 0 <= y < self.rows

    def reset_default_extry(self, point_type: str, custom: List[str]) -> None:
        """Reset entry or exit to default value and remove from custom list."""
        if point_type == "ENTRY":
            self.entry = (0, 0)
        elif point_type == "EXIT":
            self.exit = (self.cols - 1, self.rows - 1)
        if point_type in custom:
            custom.remove(point_type)

    def _validate_entry_exit(self, custom: List[str]) -> None:
        """Validate and adjust entry/exit points based on maze dimensions and 42 cells."""
        # Adjust exit defaults if WIDTH/HEIGHT changed
        if "EXIT" not in custom and ("WIDTH" in custom or "HEIGHT" in custom):
            self.exit = (self.cols - 1, self.rows - 1)

        # Check if entry/exit coordinates are within maze bounds
        if not self._is_within_bounds(self.entry):
            print(
                "Error: Entry point exceeds borders of the maze.\n"
                'Switching to default entry'
            )
            self.reset_default_extry("ENTRY", custom)
        if not self._is_within_bounds(self.exit):
            print(
                "Error: Exit point exceeds borders of the maze.\n"
                'Switching to default exit'
            )
            self.reset_default_extry("EXIT", custom)

        # Check if entry/exit coordinates conflict with 42 blocked cells
        ft_walls: List[tuple] = self.get_42_cells(self.cols, self.rows)
        if self.entry in ft_walls:
            print(
                    f"Error: Entry point is stuck in the 42 cells\n"
                    "Switching to default entry"
                    )
            self.reset_default_extry("ENTRY", custom)
        if self.exit in ft_walls:
            print(
                    f"Error: Exit point is stuck in the 42 cells\n"
                    "Switching to default exit"
                    )
            self.reset_default_extry("EXIT", custom)

        if self.entry == self.exit:
            print("Error: Entry and exit cannot have the same coordinates")
            if self.entry != (0, 0):
                self.reset_default_extry("ENTRY", custom)
                print("Switching to default entry")
            if self.entry == self.exit:
                self.reset_default_extry("EXIT", custom)
                print("Switching to default exit")
        


    def get_42_cells(self, w: int, h: int) -> List[tuple]:
        """Calculate the coordinates of the 42 cells."""
        if w < 9 or h < 7:
            return [] #  No 42_walls, maze too small
        cx: int = (w - 1) // 2 if w % 2 == 0 else w // 2
        cy: int = (h - 1) // 2 if h % 2 == 0 else h // 2

        four_walls: List[tuple] = [(cx - 1, cy), (cx - 2, cy), (cx - 3, cy),
                        (cx - 1, cy + 1), (cx - 1, cy + 2),
                        (cx - 3, cy - 1), (cx - 3, cy - 2)]
        two_walls: List[tuple] = [(cx + 1, cy), (cx + 2, cy), (cx + 3, cy),
                        (cx + 1, cy + 1), (cx + 1, cy + 2),
                        (cx + 3, cy - 1), (cx + 3, cy - 2),
                        (cx + 1, cy - 2), (cx + 2, cy - 2), (cx + 3, cy - 2),
                        (cx + 2, cy + 2), (cx + 3, cy + 2)]

        ft_walls = four_walls + two_walls
        return ft_walls
    
    def block_42_walls(self) -> None:
        """Prevent access to the 42 walls in the center of the maze."""
        for x, y in self.get_42_cells(self.cols, self.rows):
            self.grid[y][x].visited = True

    def get_cell(self, x: int, y: int) -> Cell | None:
        """Get cell at (x, y), return None if out of borders."""
        if 0 <= x < self.cols and 0 <= y < self.rows:
            return self.grid[y][x]
        return None

    def get_all_neighbors(self, cell: Cell) -> List[tuple]:
        """get all neighbor cells of a given cell."""
        neighbors: List[tuple] = []
        x, y = cell.coord
        for direction, (ox, oy) in self.offset.items():
            nx, ny = x + ox, y + oy
            neighbor: Cell = self.get_cell(nx, ny)
            if neighbor:
                neighbors.append((direction, neighbor))
        return neighbors

    def get_unvisited_neighbors(self, cell: Cell) -> List[tuple]:
        """get all unvisited cells that have common wall with current cell."""
        neighbors: List[tuple] = self.get_all_neighbors(cell)
        unvisited: List[tuple] = []
        for direction, neighbor in neighbors:
            if not neighbor.visited:
                unvisited.append((direction, neighbor))
        return unvisited
    
    def get_walled_neighbors(self, cell: Cell) -> List[tuple]:
        """Get all the neighbors that still have a wall."""
        neighbors: List[tuple] = self.get_all_neighbors(cell)
        walled: List[tuple] = []
        for direction, neighbor in neighbors:
            if cell.walls[direction] == 1:
                walled.append((direction, neighbor))
        return walled

    def delete_wall(self, cell: Cell, neighbor: Cell, direction: str) -> None:
        """Delete wall between two cells."""
        cell.walls[direction] = 0
        adj: str = self.adjacent[direction]
        neighbor.walls[adj] = 0

   # # Note: I tried to use flood fill to calculate the max area 
   # # but it doesn't produce imperfect maze anymore... why?

   # def get_open_area(self, start_x: int, start_y: int) -> tuple:
   #     """Calculeate the area of the opened corridor."""
   #     checked: set = set()
   #     queue = [(start_x, start_y)]
   #     checked.add(self.get_cell(start_x, start_y))

   #     max_x = min_x = start_x
   #     max_y = min_y = start_y

   #     while queue:
   #         x, y = queue.pop(0)
   #         current = self.get_cell(x, y)
   #         min_x = min(x, min_x)
   #         max_x = max(x, max_x)
   #         min_y = min(y, min_y)
   #         max_y = max(y, max_y)
   #         neighbors: List[tuples] = self.get_all_neighbors(current)
   #         for direction, neighbor in neighbors:
   #             if neighbor not in checked and current.walls[direction] == 0:
   #                 checked.add(neighbor)
   #                 queue.append(neighbor.coord)
   #     width = max_x - min_x + 1
   #     height = max_y - min_y + 1
   #     return (width, height)

   # def check_bad_area(self, cell: Cell, neighbor: Cell, direction: str) -> bool:
   #     """Check if removing the wall would create a too large area."""
   #     # Temporarily remove the wall
   #     self.delete_wall(cell, neighbor, direction)

   #     # Check the open area size from both cells
   #     x1, y1 = cell.coord
   #     x2, y2 = neighbor.coord

   #     width, height = self.get_open_area(x1, y1)

   #     # Restore the wall
   #     cell.walls[direction] = 1
   #     adj = self.adjacent[direction]
   #     neighbor.walls[adj] = 1

   #     # Check if area exceeds 2x3 or 3x2
   #     if width > 2 and height > 2:
   #         return True

   #     return False

   # def make_imperfect(self) -> None:
   #     """Remove additional walls to make the maze imperfect."""
   #     blocked_cells: int = len(self.get_42_cells(self.cols, self.rows))
   #     tot_cells: int = self.tot_size
   #     valid_cells: int = tot_cells - blocked_cells

   #     # remove walls in 10% of accessible cells
   #     max_removable: int = int(valid_cells * 0.9)

   #     # Collect all cells (excluding 42 cells)
   #     all_cells: List[Cell] = []
   #     ft_walls = self.get_42_cells(self.cols, self.rows)
   #     for y in range(self.rows):
   #         for x in range(self.cols):
   #             if (x, y) not in ft_walls:
   #                 all_cells.append(self.grid[y][x])

   #     random.shuffle(all_cells)
   #     walls_removed = 0

   #     for cell in all_cells:
   #         if walls_removed >= max_removable:
   #             break
   #         walled_neighbors = self.get_walled_neighbors(cell)
   #         if walled_neighbors:
   #             # Randomly pick a wall to remove
   #             random.shuffle(walled_neighbors)
   #             for direction, neighbor in walled_neighbors:
   #                 # check that it's not in the 42 pattern and that it wouldn't create a too large area
   #                 if neighbor.coord not in ft_walls and not self.check_bad_area(cell, neighbor, direction):
   #                     self.delete_wall(cell, neighbor, direction)
   #                     walls_removed += 1
   #                     break

    def make_imperfect(self) -> None:
        """Remove additional walls to make the maze imperfect."""
        blocked_cells: int = len(self.get_42_cells(self.cols, self.rows))
        tot_cells: int = self.tot_size
        valid_cells: int = tot_cells - blocked_cells

        # remove walls in 20% of accessible cells
        max_removable: int = int(valid_cells * 0.2)

        # Collect all cells (excluding 42 cells)
        all_cells: List[Cell] = []
        ft_walls = self.get_42_cells(self.cols, self.rows)
        for y in range(self.rows):
            for x in range(self.cols):
                if (x, y) not in ft_walls:
                    all_cells.append(self.grid[y][x])
        random.shuffle(all_cells)
        walls_removed = 0

        for cell in all_cells:
            if walls_removed >= max_removable:
                break

            walled_neighbors = self.get_walled_neighbors(cell) 
            if walled_neighbors:
                # Randomly pick a wall to remove
                direction, neighbor = random.choice(walled_neighbors)
                if neighbor.coord not in ft_walls:
                    self.delete_wall(cell, neighbor, direction)
                    walls_removed += 1


    def _recursive_DFS(self, cell: Cell) -> None:
        """Apply recursive DFS algo."""
        cell.visited = True

        while True:
            neighbors = self.get_unvisited_neighbors(cell)
            if not neighbors:
                return
            direction, neighbor = random.choice(neighbors)
            self.delete_wall(cell, neighbor, direction)
            self._recursive_DFS(neighbor)

    def _iter_DFS(self, entry: tuple) -> None:
        """Apply iterative DFS algo."""
        stack: List[Cell] = []
        entry_x, entry_y = entry
        current = self.get_cell(entry_x, entry_y)
        current.visited = True
        n_visited = 1

        while n_visited < self.tot_size:
            neighbors = self.get_unvisited_neighbors(current)
            if neighbors:
                direction, next_cell = random.choice(neighbors)
                self.delete_wall(current, next_cell, direction)
                stack.append(current)
                current = next_cell
                current.visited = True
                n_visited += 1
            else:
                if stack:
                    current = stack.pop()
                else:
                    break

    
    def generate_maze(self, algo: str) -> None:
        """Generate maze with dfs backtracking."""
        # block access to 42 walls
        self.block_42_walls()

        # set seed: custom if configured else None
        random.seed(self.seed)

        # select algo
        if algo.upper() == "DFS":
            self._iter_DFS(self.entry)
        # elif algo.upper() == "WILSON": call wilson's algo
        if not self.perfect:
            self.make_imperfect()

        # mark entry and exit:
        entry_cell = self.get_cell(*self.entry)
        entry_cell.is_entry = True
        exit_cell = self.get_cell(*self.exit)
        exit_cell.is_exit = True
        self.export_to_txt()

    @property
    def hex_repr(self):
        """To print in hexa the grid of the maze"""
        maze_hex: str = ""
        for y in range(self.rows):
            maze_hex += "".join(self.grid[y][x].hex_repr for x in range(self.cols))
            maze_hex += "\n"
        return maze_hex

    def print_maze_visual(self):
        """Print a visual ASCII representation of the maze."""
        # Top border
        print("┌" + "─" * (self.cols * 2 - 1) + "┐")

        for y in range(self.rows):
            # Print vertical walls
            row = "│"
            for x in range(self.cols):
                cell = self.grid[y][x]

                # Cell marker (entry/exit)
                row += "S" if cell.is_entry else "E" if cell.is_exit else " "

                # East wall
                if cell.walls['E']:
                    row += "│"
                else:
                    row += " "
            print(row)

            # Print horizontal walls (except after last row)
            if y < self.rows - 1:
                row = "├"
                for x in range(self.cols):
                    cell = self.grid[y][x]

                    # South wall
                    if cell.walls['S']:
                        row += "─"
                    else:
                        row += " "

                    # Corner
                    if x < self.cols - 1:
                        row += "┼"
                    else:
                        row += "┤"
                print(row)

        # Bottom border
        print("└" + "─" * (self.cols * 2 - 1) + "┘")

    def export_to_txt(self):
        """To generate a file with the maze in hexadecimal"""
        try:
            with open(self.output_file, "w") as f:
                    f.write(self.hex_repr)
        except Exception as e:
            print(f"Erreur lors de l'écriture du fichier: {e}")

   

def main() -> None:
    """Docstring to write."""
    # check the arguments
    if len(sys.argv) == 1:
        # Init maze with default settings
        my_maze: maze = Maze()
    elif len(sys.argv) == 2:
        # take the path to the config file
        config_file: str = sys.argv[1]
        # create maze instance
        my_maze: Maze = Maze(config_file)
    else:
        print("Usage: python3 a_maze_ing.py config_file(optional)")
        return

    # generate maze passing "DFS" or "Wilson" as argument
    my_maze.generate_maze("DFS")
    my_maze.print_maze_visual()


if __name__ == "__main__":
    main()

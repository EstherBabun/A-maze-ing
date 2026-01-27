#!/usr/bin/env python3
# File: maze_generator.py
# Author: ebabun <ebabun@student.42belgium.be>
# Author: mmeurer <mmeurer@student.42belgium.be>
# Created: 2026/01/20 18:33:22
# Updated: 2026/01/20 18:02:15

"""Docstring to write."""

from typing import Dict, List, Optional
import random
from collections import deque
from cell import Cell


class MazeGenerator:
    """A class for the maze attributes and methods.

    Attributes:
    - Attributes define by the loaded config:
        cols (int): define the width of the maze
        rows (int): define the height of the maze
        seed (int | None): the seed passed to random
        perfect (bool): True if there is juste one path between exit and start
        algorithm (str) : define which algorithm to use to generate the maze
    - Attributes created:
        grid (list(list(Cell))): Create a Cell in every cell of the maze
        unvisited (list(Cell)): a list of every unvisited cell without 42 block
        start (Cell): Keep the starting Cell
        exit (Cell): Keep the exit Cell
    """

    offset: Dict[str, tuple] = {
            "N": (0, -1),
            "S": (0, 1),
            "E": (1, 0),
            "W": (-1, 0)
            }

    def __init__(self, config_file: str | None) -> None:
        """Initialise the attributes of the maze with the default config."""
        # Set defaults first
        self.cols: int = 20
        self.rows: int = 10
        self.seed: int | None = None
        self.perfect: bool = True
        self.entry: tuple = (0, 0)
        self.exit: tuple = (19, 9)
        self.output_file: str = "maze.txt"
        self.algorithm: str = "WILSON"
        self.display: str = "ASCII"

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

        # create utils lists
        self.grid: List[List[Cell]] = [
                [Cell(x, y, self) for x in range(self.cols)]
                for y in range(self.rows)
                ]
        self.block_42_walls()

        self.unvisited: List[Cell] = [
            cell for row in self.grid
            for cell in row if not cell._is_42
            ]
        # save to total amout of valid cells
        self.valid_cells: int = len(self.unvisited)

        # store entry and exit cell objects
        self.entry_cell: Cell = self.get_cell(*self.entry)
        self.exit_cell: Cell = self.get_cell(*self.exit)

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
            "ALGORITHM": self.algorithm,
            "OUTPUT_FILE": self.output_file,
            "DISPLAY": self.display
        }

        for k, v in config_items.items():
            if k in custom:
                print(f"  {k}: {v}")
            else:
                print(f"  {k}: {v} (default)")
        print()

    def _read_config_file(self, file: str) -> Dict[str, str] | None:
        """Read config file and return raw dict or None on error."""
        try:
            with open(file, "r") as f:
                content: str = f.read()
                if content == '':
                    print("Config file is empty")
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
                        print(
                                f'Error in line {line} - '
                                f'Expected syntax: "KEY=value"'
                                )
                        continue
            if not len(raw_config.keys()):
                raise ValueError(f"No valid settings in {file}")
            return raw_config

        except (FileNotFoundError, PermissionError) as e:
            print(f"Error: {e}")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None

    def _parse_config_values(self, raw_config: Dict[str, str]) -> List[str]:
        """
        Parse and validate each config value.

        Return: list of successfully parsed keys.
        """
        custom: List[str] = []

        for k, v in raw_config.items():
            try:
                if k == "WIDTH":
                    if int(v) < 0 or int(v) == 1:
                        raise ValueError("width cannot be one or negative")
                    self.cols = int(v)
                    custom.append(k)
                elif k == "HEIGHT":
                    if int(v) < 0 or int(v) == 1:
                        raise ValueError("height cannot be one or negative")
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
                elif k == "ALGORITHM":
                    if v.upper() not in ["DFS", "WILSON"]:
                        raise ValueError(
                                "Invalid algorithm: pick DFS or WILSON"
                                )
                    self.algorithm = v.upper()
                    custom.append(k)
                elif k == "DISPLAY":
                    if v.upper() not in ["ASCII", "MLX"]:
                        raise ValueError(
                                "Invalid display mode: pick ASCII or MLX"
                                )
                    self.display = v.upper()
                    custom.append(k)
                else:
                    print(
                            f"Error: Invalid keyword {k} - "
                            "Allowed: WIDTH, HEIGHT, ENTRY, EXIT"
                            "OUTPUT_FILE, PERFECT, SEED, ALGORITHM, DISPLAY"
                            )
            except Exception as e:
                print(f'Error in {k}: {e}\nSwitching to default value')

        return custom

    def _parse_coordinate(self, value: str, key: str) -> tuple:
        """Parse a coordinate string 'x,y' into a tuple."""
        coord_tuple = tuple(int(i.strip()) for i in value.split(','))
        if len(coord_tuple) != 2:
            raise ValueError('coordinates expect 2 values "x,y"')
        return coord_tuple

    def _parse_boolean(self, value: str, key: str) -> bool:
        """Parse a boolean string 'True' or 'False'."""
        if value.upper() == "TRUE":
            return True
        elif value.upper() == "FALSE":
            return False
        else:
            raise ValueError('boolean expects "True" or "False"')

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
        """Validate entry/exit by checking maze bounds and 42 cells."""
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
                    "Error: Entry point is stuck in the 42 pattern\n"
                    "Switching to default entry"
                    )
            self.reset_default_extry("ENTRY", custom)
        if self.exit in ft_walls:
            print(
                    "Error: Exit point is stuck in the 42 pattern\n"
                    "Switching to default exit"
                    )
            self.reset_default_extry("EXIT", custom)

        if self.entry == self.exit:
            print(
                    "Error: Entry and exit cannot have "
                    "the same coordinates"
                    )
            if self.entry != (0, 0):
                self.reset_default_extry("ENTRY", custom)
                print("Switching to default entry")
            if self.entry == self.exit:
                self.reset_default_extry("EXIT", custom)
                print("Switching to default exit")

    def load_config(self, file: str) -> List[str]:
        """
        Parse the config file and update maze attributes.

        Return: list of custom keys.
        """
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
        if self.cols < 11 or self.rows < 9:
            print("Warning: Maze too small for “42” pattern")

        self.print_config(custom)
        return custom

    def get_cell(self, x: int, y: int) -> Cell | None:
        """Get cell at (x, y), return None if out of borders."""
        if 0 <= x < self.cols and 0 <= y < self.rows:
            return self.grid[y][x]
        return None

    def get_42_cells(self, w: int, h: int) -> List[tuple]:
        """Calculate the coordinates of the 42 cells."""
        if w < 11 or h < 9:
            return []  # No 42_walls, maze too small
        cx: int = (w - 1) // 2 if w % 2 == 0 else w // 2
        cy: int = (h - 1) // 2 if h % 2 == 0 else h // 2

        four_walls: List[tuple] = [
                (cx - 1, cy), (cx - 2, cy), (cx - 3, cy),
                (cx - 1, cy + 1), (cx - 1, cy + 2),
                (cx - 3, cy - 1), (cx - 3, cy - 2)
                ]
        two_walls: List[tuple] = [
                (cx + 1, cy), (cx + 2, cy), (cx + 3, cy),
                (cx + 1, cy + 1), (cx + 1, cy + 2),
                (cx + 3, cy - 1), (cx + 3, cy - 2),
                (cx + 1, cy - 2), (cx + 2, cy - 2), (cx + 3, cy - 2),
                (cx + 2, cy + 2), (cx + 3, cy + 2)
                ]

        ft_walls = four_walls + two_walls
        return ft_walls

    def block_42_walls(self) -> None:
        """Prevent access to the 42 walls in the center of the maze."""
        for x, y in self.get_42_cells(self.cols, self.rows):
            self.grid[y][x]._is_42 = True

    def get_neighbors_cells(self, cell: Cell) -> List[Cell]:
        """Return all allowed neighbored cells without the 42 block cells."""
        neighbors: List[Cell] = []
        x, y = cell.coord
        for direction, (ox, oy) in cell.OFFSET.items():
            neighbor: Cell = self.get_cell(x + ox, y + oy)
            if neighbor and not neighbor._is_42:
                neighbors.append(neighbor)
        return neighbors

    def wilson(self) -> None:
        """Generate an uniform random maze using Wilson's algorithm."""
        # Premier îlot du labyrinthe
        self.entry_cell.set_visited()

        # walk until every cell is visited
        while self.unvisited:
            random_cell = random.choice(self.unvisited)
            for cell, dir in self.walk(random_cell):
                cell.set_visited()
                cell.set_walls(dir)

    def walk(self, start_cell: Cell) -> List[tuple[Cell, str]]:
        """Walk until finding a path of unvisited cell without looping."""
        cell_visited = {}
        draft_path = []
        walking = True
        curr_cell = start_cell

        while walking:
            # random choice in neighbors cells
            next = random.choice(self.get_neighbors_cells(curr_cell))
            dir = curr_cell.get_direction(next)
            cell_visited[curr_cell] = dir
            if next.visited:
                break

            # Loop detection
            if next in draft_path:
                loop_start_idx = draft_path.index(next)
                draft_path = draft_path[:loop_start_idx + 1]
            else:
                draft_path.append(next)
            curr_cell = next

        # final way reconstruction
        path = []
        curr_cell = start_cell
        while curr_cell in cell_visited:
            dir = cell_visited[curr_cell]
            path.append((curr_cell, dir))
            curr_cell = curr_cell.get_neighbor(dir)
        return path

    def _iter_DFS(self) -> None:
        """Apply iterative DFS algo."""
        stack: List[Cell] = []
        current: Cell = self.entry_cell
        current.set_visited()

        while self.unvisited:
            neighbors = self.get_neighbors_cells(current)
            unvisited_neighbors = [cell for cell in neighbors
                                   if cell in self.unvisited]
            if unvisited_neighbors:
                neighbor = random.choice(unvisited_neighbors)
                direction = current.get_direction(neighbor)
                current.set_walls(direction)
                stack.append(current)
                current = neighbor
                current.set_visited()
            else:
                if stack:
                    current = stack.pop()
                else:
                    break

    def get_walled_neighbors(self, cell: Cell) -> List[tuple]:
        """Get all the neighbors that still have a wall."""
        neighbors: List[Cell] = self.get_neighbors_cells(cell)
        walled: List[tuple] = []
        for neighbor in neighbors:
            direction = cell.get_direction(neighbor)
            if cell.walls[direction] == 1:
                walled.append((direction, neighbor))
        return walled

    def get_dead_ends(self) -> List[Cell]:
        """Find all cells with exactly 3 standing walls(dead-ends)."""
        dead_ends: List[Cell] = []
        for row in self.grid:
            for cell in row:
                x, y = cell.coord
                if cell._is_42 :
                    continue
                wall_count = sum(cell.walls.values())
                if wall_count == 3:
                    dead_ends.append(cell)
        return dead_ends

    def make_imperfect(self) -> None:
        """Remove walls from dead-end cells to make the maze imperfect."""
        percentage: float = 0.08
        dead_ends: List[Cell] = self.get_dead_ends()
        max_removable: int = int(len(dead_ends) * percentage)

        random.shuffle(dead_ends)
        removed: int = 0

        for cell in dead_ends:
            if removed >= max_removable:
                break
            for direction, binary in cell.walls.items():
                if binary == 0:
                    neighbor = cell.get_neighbor(cell.OPPOSITE[direction])
                    if neighbor and not neighbor._is_42:
                        cell.set_walls(cell.OPPOSITE[direction])
                        removed += 1
                        break

        if removed == 0:
            for cell in dead_ends:
                if removed == 1:
                    break
                for direction, binary in cell.walls.items():
                    if binary == 0:
                        neighbor = cell.get_neighbor(cell.OPPOSITE[direction])
                        if neighbor and not neighbor._is_42:
                            cell.set_walls(cell.OPPOSITE[direction])
                            removed += 1
                            break

        # print(f"Dead-ends found: {len(dead_ends)}")
        # print(f"Target walls to remove: {max_removable}")
        # print(f"Actually removed: {removed}")
        # print()


    def bfs(self):
        # deque containing cells to explore
        queue = deque([self.entry_cell])
        # store visited cells to prevent loops or backward
        visited = set([self.entry_cell])
        # dict storing parent for each visited cell
        # To reach key I come from value
        parent = {self.entry_cell: None}  

        while queue:
            current = queue.popleft()
            if current == self.exit_cell:
                return parent
            for direction, binary in current.walls.items():
                if binary == 0:
                    neighbor = current.get_neighbor(direction)
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
                        parent[neighbor] = current

    def shortest_path(self, parent):
        path = ""
        current = self.exit_cell

        # store path starting from exit
        while current is not None:
            next = parent[current]
            if not next:
                break
            path += next.get_direction(current)
            current = next

        # set path attribute reversing stored path
        self.path = path[::-1]

    def generate_maze(self) -> None:
        """Generate maze with the choosen algo."""
        # set seed: custom if configured else None
        random.seed(self.seed)

        # select algo
        if self.algorithm == "DFS":
            self._iter_DFS()
        elif self.algorithm == "WILSON":
            self.wilson()

        if not self.perfect:
            self.make_imperfect()

        # Search solution path
        self.shortest_path(self.bfs())

        # export hex representation of the maze
        self.export_to_txt()

    @property
    def hex_repr(self):
        """Hex representation of the maze."""
        maze_hex: str = ""
        for y in range(self.rows):
            maze_hex += "".join(cell.hex_repr for cell in self.grid[y])
            maze_hex += "\n"
        return maze_hex

    def export_to_txt(self) -> None:
        """Generate a file with the maze in hexadecimal."""
        try:
            with open(self.output_file, "w") as f:
                f.write(self.hex_repr + "\n")
                x, y = self.entry
                f.write(f'{x},{y}\n')
                x, y = self.exit
                f.write(f'{x},{y}\n')
                f.write(self.path + "\n")
        except Exception as e:
            print(f"Error writing file: {e}")

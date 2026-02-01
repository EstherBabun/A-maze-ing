#!/usr/bin/env python3
# File: maze_generator.py
# Author: ebabun <ebabun@student.42belgium.be>
# Author: mmeurer <mmeurer@student.42belgium.be>
# Created: 2026/01/20 18:33:22
# Updated: 2026/01/20 18:02:15

"""A module to parse a config file, generate a maze and solve it."""

from typing import Dict, List, Optional
import random
from collections import deque
from cell import Cell
from maze_parser import MazeParser


class MazeGenerator:
    """A class for the maze attributes and methods.

    Attributes:
    - Attributes defined by the loaded config:
        cols (int): define the width of the maze
        rows (int): define the height of the maze
        seed (int | None): the seed passed to random
        perfect (bool): True if the maze is perfect
        entry (tuple(int, int)): the entry coordinates
        exit (tuple(int, int)): the exit coordinates
        output_file (str): the name of the output file
        algorithm (str) : define which algorithm to use to generate the maze
        display (str): The selected display (mlx or ascii)

    - Attributes created:
        tot_size (int): the area of the maze
        path (str): solution path stored as a string of W, S, E, N directions
        grid (list(list(Cell))): Create a Cell in every cell of the maze
        unvisited (list(Cell)): a list of every unvisited cell without 42 block
        valid_cells (int): total amout of accessible cells in the maze
        entry_cell (Cell): the starting Cell
        exit_cell (Cell): the exit Cell
    """

    offset: Dict[str, tuple] = {
            "N": (0, -1),
            "S": (0, 1),
            "E": (1, 0),
            "W": (-1, 0)
            }
    opposite: Dict[str, str] = {"E": "W", "W": "E", "N": "S", "S": "N"}

    def __init__(self, config_file: Optional[str] = None) -> None:
        """
        Initialise the maze generator with configuration.

        Args:
            config_file (str | None): Path to configuration file,
                                     or None for defaults
        """
        # Parse configuration using MazeParser
        parser = MazeParser(config_file)

        # Store parser for later use (to print final config)
        self._parser = parser
        self._config_file = config_file

        # Set configuration attributes directly from parser
        self.cols: int = parser.cols
        self.rows: int = parser.rows
        self.seed: Optional[int] = parser.seed
        self.perfect: bool = parser.perfect
        self.entry: tuple = parser.entry
        self.exit: tuple = parser.exit
        self.output_file: str = parser.output_file
        self.algorithm: str = parser.algorithm
        self.display: str = parser.display
        self.is_displayable: bool = parser.is_displayable

        # Initialize remaining attributes
        self.tot_size: int = self.cols * self.rows
        self.path: str = ""

        # create utils lists
        self.grid: List[List[Cell]] = [
                [Cell(x, y) for x in range(self.cols)]
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
        self.entry_cell: Cell | None = self.get_cell(*self.entry)
        self.exit_cell: Cell | None = self.get_cell(*self.exit)

        # generate maze structure
        self.generate_maze()

    def get_cell(self, x: int, y: int) -> Cell | None:
        """Get cell at (x, y), return None if out of borders."""
        if 0 <= x < self.cols and 0 <= y < self.rows:
            return self.grid[y][x]
        return None

    def get_neighbor(self, cell: Cell, direction: str) -> Cell | None:
        """
         Get the neighboring cell in the given direction.

        Args:
            dir (str): Direction to look for (N, S, E, or W).

        Returns:
            Cell | None: The neighboring cell if it exists,
            otherwise None.
        """
        x, y = cell.coord
        ox, oy = self.offset[direction]
        return self.get_cell(x + ox, y + oy)

    def set_visited(self, cell: Cell) -> None:
        """
        Mark the cell as visited and remove it from the unvisited list
        """
        cell.visited = True
        self.unvisited.remove(cell)

    def get_direction(self, cell: Cell, neighbor: Cell) -> str | None:
        """
        Determine the direction between cell and a neighboring cell.

        Args:
            cell (Cell): cell of reference
            neighbor (Cell): Adjacent cell.

        Returns:
            str | None: Direction of the neighbor (N, S, E, or W),
            or None if the cells are not adjacent.
        """
        x, y = cell.coord
        nx, ny = neighbor.coord
        offset: Tuple[int, int] = (nx - x, ny - y)
        for k, v in self.offset.items():
            if v == offset:
                return k
        return None

    def set_walls(self, cell: Cell, direction: str) -> None:
        """
        Remove the wall between this cell and its neighbor in a direction.

        Args:
            dir (str): Direction of the neighbor cell (N, S, E, or W)
        """
        neighbor = self.get_neighbor(cell, direction)
        if neighbor:
            cell.walls[direction] = 0
            neighbor.walls[self.opposite[direction]] = 0


    def block_42_walls(self) -> None:
        """Prevent access to the 42 walls in the center of the maze."""
        for x, y in self._parser.ft_walls:
            self.grid[y][x]._is_42 = True

    def get_neighbors_cells(self, cell: Cell) -> List[Cell]:
        """Return all allowed neighbored cells without the 42 block cells."""
        neighbors: List[Cell] = []
        x, y = cell.coord
        for direction, (ox, oy) in self.offset.items():
            neighbor: Cell | None = self.get_cell(x + ox, y + oy)
            if neighbor and not neighbor._is_42:
                neighbors.append(neighbor)
        return neighbors

    def wilson(self) -> None:
        """Generate an uniform random maze using Wilson's algorithm."""
        # Premier îlot du labyrinthe
        if self.entry_cell:
            self.set_visited(self.entry_cell)

        # walk until every cell is visited
        while self.unvisited:
            random_cell = random.choice(self.unvisited)
            for cell, direction in self.walk(random_cell):
                self.set_visited(cell)
                self.set_walls(cell, direction)

    def walk(self, start_cell: Cell) -> List[tuple[Cell, str]]:
        """Walk until finding a path of unvisited cell without looping."""
        cell_visited: Dict = {}
        draft_path: List = []
        walking: bool = True
        current: Cell = start_cell

        while walking:
            # random choice in neighbors cells
            neighbor: Cell = random.choice(self.get_neighbors_cells(current))
            direction: str = self.get_direction(current, neighbor)
            cell_visited[current] = direction
            if neighbor.visited:
                break

            # Loop detection
            if neighbor in draft_path:
                loop_start_idx: int = draft_path.index(neighbor)
                draft_path = draft_path[:loop_start_idx + 1]
            else:
                draft_path.append(neighbor)
            current = neighbor

        # final way reconstruction
        path = []
        current = start_cell
        while current in cell_visited:
            direction = cell_visited[current]
            path.append((current, direction))
            current = self.get_neighbor(current, direction)
        return path

    def _iter_DFS(self) -> None:
        """Apply iterative DFS algo."""
        stack: List[Cell] = []
        current: Cell = self.entry_cell
        self.set_visited(current)

        while self.unvisited:
            neighbors = self.get_neighbors_cells(current)
            unvisited_neighbors = [cell for cell in neighbors
                                   if cell in self.unvisited]
            if unvisited_neighbors:
                neighbor = random.choice(unvisited_neighbors)
                direction = self.get_direction(current, neighbor)
                self.set_walls(current, direction)
                stack.append(current)
                current = neighbor
                self.set_visited(current)
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
            direction = self.get_direction(cell, neighbor)
            if cell.walls[direction] == 1:
                walled.append((direction, neighbor))
        return walled

    def get_dead_ends(self) -> List[Cell]:
        """Find all cells with exactly 3 standing walls(dead-ends)."""
        dead_ends: List[Cell] = []
        for row in self.grid:
            for cell in row:
                x, y = cell.coord
                if cell._is_42:
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
                    neighbor = self.get_neighbor(cell, self.opposite[direction])
                    if neighbor and not neighbor._is_42:
                        self.set_walls(cell, self.opposite[direction])
                        removed += 1
                        break

        if removed == 0:
            for cell in dead_ends:
                if removed == 1:
                    break
                for direction, binary in cell.walls.items():
                    if binary == 0:
                        neighbor = self.get_neighbor(cell, self.opposite[direction])
                        if neighbor and not neighbor._is_42:
                            self.set_walls(cell, self.opposite[direction])
                            removed += 1
                            break

        # print(f"Dead-ends found: {len(dead_ends)}")
        # print(f"Target walls to remove: {max_removable}")
        # print(f"Actually removed: {removed}")
        # print()

    def bfs(self):
        """Breadth-first-search algorithm to solve the maze."""
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
                    neighbor = self.get_neighbor(current, direction)
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
                        parent[neighbor] = current

    def shortest_path(self, parent):
        """Store the shortest path to exit as a maze attribute."""
        path = ""
        current = self.exit_cell

        # store path starting from exit
        while current is not None:
            neighbor = parent[current]
            if not neighbor:
                break
            path += self.get_direction(neighbor, current)
            current = neighbor

        # set path attribute reversing stored path
        self.path = path[::-1]

    def generate_maze(self) -> None:
        """Generate maze with the choosen algo."""
        # set seed: custom if configured else None
        random.seed(self.seed)

        # select algo
        if self.algorithm == "dfs":
            self._iter_DFS()
        else:
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

if __name__ == "__main__":
    import sys
    # if no config file:
    if len(sys.argv) == 1:
        maze = MazeGenerator()
        maze.generate_maze()

    # if config file:
    elif len(sys.argv) == 2:
        config_file: str = sys.argv[1]
        maze = MazeGenerator(config_file)
        maze.generate_maze()
    else:
        print("Usage: python3 a_maze_ing.py config_file(optional)")

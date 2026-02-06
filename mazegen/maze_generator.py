# File: mazegen/maze_generator.py
# Author: ebabun <ebabun@student.42belgium.be>
# Author: mmeurer <mmeurer@student.42belgium.be>
# Created: 2026/01/20 18:33:22
# Updated: 2026/01/20 18:02:15

"""A module to parse a config file, generate a maze and solve it."""

import random
from collections import deque
from .cell import Cell
from .maze_parser import MazeParser

OFFSET: dict[str | None, tuple[int, int]] = {
            "N": (0, -1),
            "S": (0, 1),
            "E": (1, 0),
            "W": (-1, 0)
            }

OPPOSITE: dict[str | None, str | None] = {
        "E": "W", "W": "E", "N": "S", "S": "N"
        }


class MazeGenerator:
    """A class for the maze generation and resolution.

    Attributes:
        config_file (str | None): optional config file
        _parser (MazeParser): MazeParser instance

    - Attributes defined by the parser:
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
        grid (list(list(Cell))): Maze structure as rows of Cell objects
        unvisited (list(Cell)): list of all unvisited cell (excluding 42 block)
        valid_cells (int): total amout of accessible cells in the maze
        entry_cell (Cell): the starting Cell
        exit_cell (Cell): the exit Cell
    """

    def __init__(self, config_file: str | None = None) -> None:
        """
        Initialise the maze generator with the parsed configuration.

        Args:
            config_file (str | None): Path to configuration file,
                                     or None for defaults
        """
        # Parse configuration using MazeParser
        parser = MazeParser(config_file)

        # Store parser for later use
        self._parser: MazeParser = parser
        self.config_file: str | None = config_file

        # Set configuration attributes directly from parser
        self.cols: int = parser.cols
        self.rows: int = parser.rows
        self.seed: int | None = parser.seed
        self.perfect: bool = parser.perfect
        self.entry: tuple[int, int] = parser.entry
        self.exit: tuple[int, int] = parser.exit
        self.output_file: str = parser.output_file
        self.algorithm: str = parser.algorithm
        self.display: str | None = parser.display
        self.is_displayable: bool = parser.is_displayable

        # Initialize remaining attributes
        self.tot_size: int = self.cols * self.rows
        self.path: str = ""

        # create utils lists
        self.grid: list[list[Cell]] = [
                [Cell(x, y) for x in range(self.cols)]
                for y in range(self.rows)
                ]
        self.block_42_walls()

        self.unvisited: list[Cell] = [
            cell for row in self.grid
            for cell in row if not cell.is_42
            ]
        # save to total amout of valid cells
        self.valid_cells: int = len(self.unvisited)

        # store entry and exit cell objects
        self.entry_cell: Cell | None = self.get_cell(*self.entry)
        self.exit_cell: Cell | None = self.get_cell(*self.exit)

        # generate maze structure
        self.generate_maze()

    def get_cell(self, x: int, y: int) -> Cell | None:
        """Get cell at (x, y), return None if out of bounds."""
        if 0 <= x < self.cols and 0 <= y < self.rows:
            return self.grid[y][x]
        return None

    def get_neighbor(
            self,
            cell: Cell | None,
            direction: str | None
            ) -> Cell | None:
        """
        Get the neighboring cell in the given direction.

        Args:
            cell (Cell): The current cell.
            direction (str): Direction to look for (N, S, E, or W).

        Returns:
            Cell | None: The neighboring cell if it exists, otherwise None.
        """
        if cell is not None:
            x, y = cell.coord
        ox, oy = OFFSET[direction]
        return self.get_cell(x + ox, y + oy)

    def set_visited(self, cell: Cell | None) -> None:
        """Mark the cell as visited and remove it from the unvisited list."""
        if cell is not None:
            cell.visited = True
            self.unvisited.remove(cell)

    def get_direction(
            self,
            cell: Cell | None,
            neighbor: Cell | None
            ) -> str | None:
        """
        Determine the direction between cell and a neighboring cell.

        Args:
            cell (Cell): cell of reference
            neighbor (Cell): Adjacent cell.

        Returns:
            str | None: Direction of the neighbor (N, S, E, or W),
            or None if the cells are not adjacent.
        """
        if cell is not None:
            x, y = cell.coord
        if neighbor is not None:
            nx, ny = neighbor.coord
        offset: tuple[int, int] = (nx - x, ny - y)
        for k, v in OFFSET.items():
            if v == offset:
                return k
        return None

    def set_walls(self, cell: Cell | None, direction: str | None) -> None:
        """
        Remove the wall between this cell and its neighbor in a direction.

        Args:
            cell (Cell): The current cell.
            direction (str): Direction of the neighbor cell (N, S, E, or W).
        """
        neighbor = self.get_neighbor(cell, direction)
        if neighbor is not None and cell is not None:
            cell.walls[direction] = 0
            neighbor.walls[OPPOSITE[direction]] = 0

    def block_42_walls(self) -> None:
        """Mark cells in 42 pattern as inaccessible."""
        for x, y in self._parser.ft_walls:
            self.grid[y][x].is_42 = True

    def get_neighbors_cells(self, cell: Cell | None) -> list[Cell | None]:
        """
        Return all allowed neighboring cells without the 42 block cells.

        Args:
            cell (Cell): The cell to get neighbors for.

        Returns:
            list[Cell]: List of valid neighboring cells (excludes 42 block).
        """
        neighbors: list[Cell | None] = []
        if cell is not None:
            x, y = cell.coord
        for direction, (ox, oy) in OFFSET.items():
            neighbor: Cell | None = self.get_cell(x + ox, y + oy)
            if neighbor and not neighbor.is_42:
                neighbors.append(neighbor)
        return neighbors

    def wilson(self) -> None:
        """Generate a uniform random maze using Wilson's algorithm."""
        # Premier îlot du labyrinthe
        if self.entry_cell:
            self.set_visited(self.entry_cell)

        # walk until every cell is visited
        while self.unvisited:
            random_cell = random.choice(self.unvisited)
            for cell, direction in self.walk(random_cell):
                self.set_visited(cell)
                self.set_walls(cell, direction)

    def walk(self, start_cell: Cell) -> list[tuple[Cell | None, str | None]]:
        """
        Perform a loop-erased random walk until reaching a visited cell.

        Args:
            start_cell (Cell): The random cell to start walking from.

        Returns:
            list[tuple[Cell, str]]: List of (cell, direction) pairs
            representing the loop-erased path
            from start_cell to the visited tree.
        """
        cell_visited: dict[Cell | None, str | None] = {}
        draft_path: list[Cell] = []
        walking: bool = True
        current: Cell | None = start_cell

        while walking:
            # random choice in neighbors cells
            neighbor: Cell | None = random.choice(
                    self.get_neighbors_cells(current)
                    )
            direction: str | None = self.get_direction(current, neighbor)
            cell_visited[current] = direction
            if neighbor is not None and neighbor.visited:
                break

            # Loop detection
            if neighbor in draft_path:
                loop_start_idx: int = draft_path.index(neighbor)
                draft_path = draft_path[:loop_start_idx + 1]
            elif neighbor is not None:
                draft_path.append(neighbor)
            current = neighbor

        # final way reconstruction
        path: list[tuple[Cell | None, str | None]] = []
        current = start_cell
        while current in cell_visited:
            direction = cell_visited[current]
            path.append((current, direction))
            current = self.get_neighbor(current, direction)
        return path

    def iter_dfs(self) -> None:
        """Generate a random maze using Depth-First Search algorithm."""
        stack: list[Cell] = []
        current: Cell | None = self.entry_cell
        self.set_visited(current)

        while self.unvisited:
            neighbors = self.get_neighbors_cells(current)
            unvisited_neighbors = [cell for cell in neighbors
                                   if cell in self.unvisited]
            if unvisited_neighbors:
                neighbor = random.choice(unvisited_neighbors)
                direction = self.get_direction(current, neighbor)
                self.set_walls(current, direction)
                if current is not None:
                    stack.append(current)
                current = neighbor
                self.set_visited(current)
            else:
                if stack:
                    current = stack.pop()
                else:
                    break

    def get_walled_neighbors(
            self,
            cell: Cell | None
            ) -> list[tuple[str | None, Cell | None]]:
        """
        Get all the neighbors that still have a common wall with the cell.

        Args:
            cell (Cell): The cell to check neighbors for.

        Returns:
            list[tuple[str, Cell]]: List of (direction, neighbor) pairs where
            a wall still exists between cell and neighbor.
        """
        neighbors: list[Cell | None] = self.get_neighbors_cells(cell)
        walled: list[tuple[str | None, Cell | None]] = []
        for neighbor in neighbors:
            direction = self.get_direction(cell, neighbor)
            if cell and cell.walls[direction] == 1:
                walled.append((direction, neighbor))
        return walled

    def get_dead_ends(self) -> list[Cell]:
        """
        Find all cells with exactly 3 standing walls (dead ends).

        Returns:
            list[Cell]: All cells that have exactly three walls intact,
            making them dead ends in the maze.
        """
        dead_ends: list[Cell] = []
        for row in self.grid:
            for cell in row:
                x, y = cell.coord
                if cell.is_42:
                    continue
                wall_count = sum(cell.walls.values())
                if wall_count == 3:
                    dead_ends.append(cell)
        return dead_ends

    def make_imperfect(self) -> None:
        """
        Remove walls from dead-end cells to make the maze imperfect.

        An imperfect maze contains multiple paths between two points.
        This method removes approximately 10% of dead-end walls to create
        loops or alternative paths in the maze (if the maze is big enough).
        """
        percentage: float = 0.1  # 10%
        dead_ends: list[Cell] = self.get_dead_ends()
        max_removable: int = int(len(dead_ends) * percentage)

        random.shuffle(dead_ends)
        removed: int = 0

        for cell in dead_ends:
            if removed >= max_removable:
                break
            for direction, binary in cell.walls.items():
                if binary == 0:
                    neighbor = self.get_neighbor(cell, OPPOSITE[direction])
                    if neighbor and not neighbor.is_42:
                        self.set_walls(cell, OPPOSITE[direction])
                        removed += 1
                        break

        if removed == 0:
            for cell in dead_ends:
                if removed >= 1:
                    break
                for direction, binary in cell.walls.items():
                    if binary == 0:
                        neighbor = self.get_neighbor(cell, OPPOSITE[direction])
                        if neighbor and not neighbor.is_42:
                            self.set_walls(cell, OPPOSITE[direction])
                            removed += 1
                            break

        if removed == 0:
            print("Warning: maze might not be imperfect due to small size")

        # debug dead-end removal:
        # print(f"Dead-ends found: {len(dead_ends)}")
        # print(f"Target walls to remove: {max_removable}")
        # print(f"Actually removed: {removed}")
        # print()

    def bfs(self) -> dict[Cell | None, Cell | None]:
        """
        Breadth-first search algorithm to solve the maze.

        Returns:
            dict[Cell, Cell | None] | None: Dictionary mapping each cell to its
            parent, or None if exit is unreachable.
        """
        # deque containing cells to explore
        queue = deque([self.entry_cell])
        # store visited cells to prevent loops or backward
        visited = set([self.entry_cell])
        # dict storing parent for each visited cell
        # To reach key I come from value
        parent: dict[Cell | None, Cell | None] = {self.entry_cell: None}

        while queue:
            current = queue.popleft()
            if current == self.exit_cell:
                return parent
            if current:
                for direction, binary in current.walls.items():
                    if binary == 0:
                        neighbor = self.get_neighbor(current, direction)
                        if neighbor not in visited:
                            visited.add(neighbor)
                            queue.append(neighbor)
                            parent[neighbor] = current
        return parent

    def shortest_path(self, parent: dict[Cell | None, Cell | None]) -> None:
        """
        Store the shortest path to exit as a maze attribute.

        Args:
            parent (dict[Cell, Cell | None]): Dictionary mapping
            each cell to its parent.
        """
        path: str = ""
        current = self.exit_cell

        # store path starting from exit
        while current is not None:
            neighbor = parent[current]
            if not neighbor:
                break
            direction: str | None = self.get_direction(neighbor, current)
            if direction:
                path += direction
            current = neighbor

        # set path attribute reversing stored path
        self.path = path[::-1]

    def generate_maze(self) -> None:
        """
        Generate the maze using the chosen algorithm.

        Applies the configured algorithm (DFS or Wilson's), optionally makes
        the maze imperfect, solves it using BFS, and exports to file.
        """
        # set seed: custom if configured else None
        random.seed(self.seed)

        # select algo
        if self.algorithm == "dfs":
            self.iter_dfs()
        else:
            self.wilson()

        if not self.perfect:
            self.make_imperfect()

        # Search solution path
        self.shortest_path(self.bfs())

        # export hex representation of the maze
        self.export_to_txt()

    @property
    def hex_repr(self) -> str:
        """
        Hexadecimal representation of the maze.

        Each cell's walls are encoded as a 4-bit binary number (WSEN order),
        then converted to a single hexadecimal character (0-F).

        Returns:
            str: Multi-line string with hex representation, one row per line.
        """
        maze_hex: str = ""
        for y in range(self.rows):
            maze_hex += "".join(cell.hex_repr for cell in self.grid[y])
            maze_hex += "\n"
        return maze_hex

    def export_to_txt(self) -> None:
        """
        Export the maze to the output file in hexadecimal format.

        File format:
            - Lines 1-N: Hexadecimal maze representation (one row per line)
            - Line N+1: New line
            - Line N+2: Entry coordinates (x,y)
            - Line N+3: Exit coordinates (x,y)
            - Line N+4: Solution path as direction string (NSEW)
        """
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

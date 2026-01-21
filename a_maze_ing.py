#!/usr/bin/env python3
# File: maze.py
# Author: ebabun <ebabun@student.42belgium.be>
# Author: mmeurer <mmeurer@student.42belgium.be>
# Created: 2026/01/20 18:33:22
# Updated: 2026/01/20 18:02:15

import math
from typing import Dict, List, Any
import random

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

    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialise the attributes of the maze with the loaded config."""
        self.cols: int = config["WIDTH"]
        self.rows: int = config["HEIGHT"]
        self.seed: int | None = None
        self.perfect: bool = config["PERFECT"]
        self.algorithm: str = config["ALGORITHM"]
        self.grid: List[List[Cell]] = [
            [Cell(x, y, self) for x in range(self.cols)]
            for y in range(self.rows)]
        self.block_42_walls()
        self.unvisited: List[Cell] = [
            cell for row in self.grid
            for cell in row if not cell._is_42
            ]
        self.start: Cell = self.grid[config["ENTRY"][1]][config["ENTRY"][0]]
        self.exit: Cell = self.grid[config["EXIT"][1]][config["EXIT"][0]]

    def random_cell(self) -> Cell:
        """To randomly choice a non visited cell in the grid"""
        return random.choice(self.unvisited)

    def get_neighbors_cells(self, cell: Cell) -> List[Cell]:
        """Return all allowed neighbored cells without the 42 block cells"""
        nearby_cell = []
        x, y = cell.coord

        if x > 0 and not self.grid[y][x - 1]._is_42:
            nearby_cell.append(self.grid[y][x - 1])
        if x < self.cols - 1 and not self.grid[y][x + 1]._is_42:
            nearby_cell.append(self.grid[y][x + 1])
        if y > 0 and not self.grid[y - 1][x]._is_42:
            nearby_cell.append(self.grid[y - 1][x])
        if y < self.rows - 1 and not self.grid[y + 1][x]._is_42:
            nearby_cell.append(self.grid[y + 1][x])
        return nearby_cell

    def wilson(self) -> None:
        """Generate an uniform random maze using Wilson algorithm"""
        # Premier îlot du labyrinthe
        self.start.set_visited()

        # walk until every cell is visited
        while self.unvisited:
            random_cell = self.random_cell()
            for cell, dir in self.walk(random_cell):
                cell.set_visited()
                cell.set_walls(dir)

    def walk(self, start_cell: Cell) -> List[tuple[Cell, str]]:
        """walk on until founding a path of unvisited cell without looping"""
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
        current = self.start
        current.set_visited()

        while self.unvisited:
            neighbors = self.get_neighbors_cells(current)
            cells_unvisited = list(set(self.unvisited) & set(neighbors))
            if cells_unvisited:
                next_cell = random.choice(cells_unvisited)
                direction = current.get_direction(next_cell)
                current.set_walls(direction)
                stack.append(current)
                current = next_cell
                current.set_visited()
            else:
                if stack:
                    current = stack.pop()
                else:
                    break

    def generate_maze(self) -> None:
        """Generate maze with the choosen algo."""
        # set seed: custom if configured else None
        random.seed(self.seed)

        # select algo
        if self.algorithm == "DFS":
            self._iter_DFS()
        elif self.algorithm == "Wilson":
            self.wilson()

        # a voir pour qu'il soit perfect plus tard!

    def block_42_walls(self) -> None:
        """Prevent access to the 42 walls in the center of the maze."""
        w = self.cols
        h = self.rows
        if w < 9 or h < 7:
            return  # No 42_walls, maze too small
        if w % 2 == 0:
            cx = math.floor(w / 2) - 1
        else:
            cx = math.floor(w / 2)
        if h % 2 == 0:
            cy = math.floor(h / 2) - 1
        else:
            cy = math.floor(h / 2)

        four_walls: List[tuple] = [
            (cx - 1, cy), (cx - 2, cy), (cx - 3, cy),
            (cx - 1, cy + 1), (cx - 1, cy + 2),
            (cx - 3, cy - 1), (cx - 3, cy - 2),
            ]
        two_walls: List[tuple] = [
            (cx + 1, cy), (cx + 2, cy), (cx + 3, cy),
            (cx + 1, cy + 1), (cx + 1, cy + 2),
            (cx + 3, cy - 1), (cx + 3, cy - 2),
            (cx + 1, cy - 2), (cx + 2, cy - 2), (cx + 3, cy - 2),
            (cx + 2, cy + 2), (cx + 3, cy + 2)
            ]

        ft_walls = four_walls + two_walls

        for x, y in ft_walls:
            self.grid[y][x]._is_42 = True

    def print_maze_visual(self) -> None:
        """Print a visual ASCII representation of the maze."""
        # Top border
        print("┌" + "─" * (self.cols * 2 - 1) + "┐")

        for y in range(self.rows):
            # Print vertical walls
            row = "│"
            for x in range(self.cols):
                cell = self.grid[y][x]

                # Cell marker (entry/exit)
                if cell == self.start:
                    row += "S"
                elif cell == self.exit:
                    row += "E"
                elif cell._is_42:
                    row += "■"
                else:
                    row += " "

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

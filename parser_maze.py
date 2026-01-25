#!/usr/bin/env python3
# File: parser_maze.py
# Author: ebabun <ebabun@student.42belgium.be>
# Author: mmeurer <mmeurer@student.42belgium.be>
# Created: 2026/01/23 16:09:10
# Updated: 2026/01/24 16:09:10

from maze_generator import MazeGenerator


class MazeParser:
    """
    A class to display a maze in terminal ASCII rendering.
    """

    def __init__(self, filename, maze_size, config):
        """
        Attributs:
        - name (str): the name of the file to open
        - config (dict): config of the maze
        - maze_size (int): height of the maze

        From file.txt:
        - maze (list[list]): lines of hexadecimal
        - entry (tuple): coordinates of the entry cell
        - exit (tuple): coordinates of the exit cell
        - path (str): shortest path to the exit
        """

        self.name = filename
        self.config = config
        self.maze_size = maze_size
        self.maze: list[list] = []
        self.entry: tuple = ()
        self.exit: tuple = ()
        self.path = ""

    @staticmethod
    def show_menu():
        print("\n=== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. Rotate maze colors")
        print("4. Quit")

    @staticmethod
    def get_choice():
        wrong_choice = False
        while True:
            choice = input("Choice? (1-4): ")
            if choice in ("1", "2", "3", "4"):
                return choice, wrong_choice
            else:
                wrong_choice = True
                return choice, wrong_choice

    def open_file(self):
        try:
            with open(self.name, "r") as f:
                lines = [line.rstrip("\n") for line in f.readlines()]
                return lines
        except FileNotFoundError:
            print(f"Erreur: le fichier {self.name} est introuvable")
            return

    def parse_lines(self):
        lines = self.open_file()
        self.maze = lines[:self.maze_size]
        x, y = lines[self.maze_size + 1].split(',')
        self.entry = (int(x), int(y))
        x, y = lines[self.maze_size + 2].split(',')
        self.exit = (int(x), int(y))
        self.path = lines[self.maze_size + 3]

    def display_maze(self, display_path, w_color):
        acc_line = 0
        coor_path = self.coordinates_path()
        end_color = "\033[0m"
        line_border = (
            f"{w_color}+{end_color}"
            + f"{w_color}---+{end_color}" * len(self.maze[0])
        )

        print(line_border)
        for line in self.maze:
            line_walls = f"{w_color}|{end_color}"
            line_bottom = f"{w_color}+{end_color}"
            acc_hexa = 0
            for hexa in line:
                if (acc_hexa, acc_line) == self.entry:
                    cell_content = "\033[32m■\033[0m"
                elif (acc_hexa, acc_line) == self.exit:
                    cell_content = "\033[31m■\033[0m"
                elif hexa == "F":
                    cell_content = "■"
                elif display_path and (acc_hexa, acc_line) in coor_path:
                    cell_content = "\033[35m■\033[0m"
                else:
                    cell_content = " "

                if hexa == "F":
                    line_walls += f" {cell_content} {w_color}|{end_color}"
                    line_bottom += f"{w_color}---+{end_color}"
                else:
                    if hexa in "2367ABE":
                        line_walls += f" {cell_content} {w_color}|{end_color}"
                    else:
                        line_walls += f" {cell_content}  "
                    if hexa in "4567CDE":
                        line_bottom += f"{w_color}---+{end_color}"
                    else:
                        line_bottom += f"   {w_color}+{end_color}"
                acc_hexa += 1
            print(line_walls)
            print(line_bottom)
            acc_line += 1

    def coordinates_path(self):
        path = []
        cx, cy = self.entry
        for direction in self.path:
            x, y = MazeGenerator.offset[direction]
            cx += x
            cy += y
            path.append((cx, cy))
        return path

    def regenerate_maze(self):
        maze = MazeGenerator(self.config)
        maze.generate_maze()
        new_parsing = MazeParser(maze.output_file, maze.rows, self.config)
        new_parsing.display_ascii()

    def display_ascii(self):
        self.parse_lines()
        show_path = False
        wall_colors = ["\033[27m", "\033[33m", "\033[32m", "\033[36m"]
        acc_color = 0

        print("\033[2J")      # clear
        print("\033[H")       # curseur en haut à gauche
        while True:
            print("\033[H", end="")
            w_color = wall_colors[acc_color % 4]
            if show_path:
                self.display_maze(True, w_color)
            else:
                self.display_maze(False, w_color)

            self.show_menu()
            choice, wrong = self.get_choice()
            if wrong:
                while wrong:
                    print("Invalid choice, please enter a number from 1 to 4.")
                    choice, wrong = self.get_choice()
                print("\033[2J")

            # Commandes available
            if choice == '1':
                self.regenerate_maze()
                break
            elif choice == '2':
                show_path = not show_path
            elif choice == '3':
                acc_color += 1
            elif choice == '4':
                print("Bye! Thanks for playing ~")
                break

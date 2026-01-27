#!/usr/bin/env python3
# File: parser_maze.py
# Author: ebabun <ebabun@student.42belgium.be>
# Author: mmeurer <mmeurer@student.42belgium.be>
# Created: 2026/01/23 16:09:10
# Updated: 2026/01/27 16:09:10

"""A file for the renderer in ASCII"""

from maze_generator import MazeGenerator


class AsciiRenderer:
    """
    A class to display a maze in terminal ASCII rendering.
    """

    def __init__(self, config: str) -> None:
        """
        Attributs:
        - name (str): the name of the file to open
        - config (dict): config of the maze
        - maze_height (int): height of the maze
        - maze_width (int): width of the maze

        From file.txt:
        - maze (str): lines of hexadecimal
        - entry (tuple): coordinates of the entry cell
        - exit (tuple): coordinates of the exit cell
        - path (str): shortest path to the exit
        """

        self.name: str = ""
        self.config: str = config
        self.maze_height: int = 0
        self.maze_width: int = 0
        self.maze: str = ""
        self.entry: tuple = ()
        self.exit: tuple = ()
        self.path: str = ""

    @staticmethod
    def show_menu() -> None:
        """Describe commands available and their actions"""
        print("\n=== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. Rotate maze colors")
        print("4. Quit")

    @staticmethod
    def get_choice() -> tuple[str, bool]:
        """Take the user choice until it's valid"""
        wrong_choice = False
        while True:
            choice = input("Choice? (1-4): ")
            if choice in ("1", "2", "3", "4"):
                return choice, wrong_choice
            else:
                wrong_choice = True
                return choice, wrong_choice

    def create_maze(self) -> None:
        """Create an instance maze and display it"""
        maze = MazeGenerator(self.config)
        maze.generate_maze()
        self.name = maze.output_file
        self.maze_height = maze.rows
        self.maze_width = maze.cols
        self.maze = maze.hex_repr
        self.entry = maze.entry
        self.exit = maze.exit
        self.path = maze.path
        self.display_ascii()

    def coordinates_path(self) -> list[tuple]:
        """Tranform hex path in a list of coordinates travel"""
        path = []
        cx, cy = self.entry
        for direction in self.path:
            x, y = MazeGenerator.offset[direction]
            cx += x
            cy += y
            path.append((cx, cy))
        return path
    
    def display_maze(self, display_path: bool, wall_color:str) -> None:
        """To display the maze with walls and different contents : entrym exit and 42 block"""
        acc_line = 0
        coordinates_path = self.coordinates_path()
        end_color = "\033[0m"
        line_top_border = (
            f"{wall_color}+{end_color}"
            + f"{wall_color}---+{end_color}" * self.maze_width
        )
        print(line_top_border)
        for line in self.maze[:-1].split("\n"):
            line_walls = f"{wall_color}|{end_color}"
            line_bottom = f"{wall_color}+{end_color}"
            acc_hexa = 0
            for hexa in line:
                # check the content
                if (acc_hexa, acc_line) == self.entry:
                    cell_content = "\033[32m■\033[0m"
                elif (acc_hexa, acc_line) == self.exit:
                    cell_content = "\033[31m■\033[0m"
                elif hexa == "F":
                    cell_content = "■"
                elif display_path and (acc_hexa, acc_line) in coordinates_path:
                    cell_content = "\033[35m■\033[0m"
                else:
                    cell_content = " "

                # construct the maze with the content
                if hexa == "F":
                    line_walls += f" {cell_content} {wall_color}|{end_color}"
                    line_bottom += f"{wall_color}---+{end_color}"
                else:
                    if hexa in "2367ABE":
                        line_walls += f" {cell_content} {wall_color}|{end_color}"
                    else:
                        line_walls += f" {cell_content}  "
                    if hexa in "4567CDE":
                        line_bottom += f"{wall_color}---+{end_color}"
                    else:
                        line_bottom += f"   {wall_color}+{end_color}"
                acc_hexa += 1
            print(line_walls)
            print(line_bottom)
            acc_line += 1

    def display_ascii(self) -> None:
        """To display everything : maze and commands"""
        show_path = False
        wall_colors = ["\033[27m", "\033[33m", "\033[32m", "\033[36m"]
        acc_color = 0

        # clear and right placement (left corner)
        print("\033[2J")
        print("\033[H")
        print("Scroll up for configuration and errors feedback")
        while True:
            wall_color = wall_colors[acc_color % 4]
            if show_path:
                self.display_maze(True, wall_color)
            else:
                self.display_maze(False, wall_color)

            # commands available and catch if not
            self.show_menu()
            choice, wrong = self.get_choice()
            if wrong:
                while wrong:
                    print("Invalid choice, please enter a number from 1 to 4.")
                    choice, wrong = self.get_choice()
                print("\033[2J")
            if choice == '1':
                self.create_maze()
                break
            elif choice == '2':
                print("\033[2J")
                print("\033[H")
                show_path = not show_path
            elif choice == '3':
                print("\033[2J")
                print("\033[H")
                acc_color += 1
            elif choice == '4':
                print("Bye! Thanks for playing ~")
                break

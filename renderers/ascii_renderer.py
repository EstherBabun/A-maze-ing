# File: renderers/ascii_renderer.py
# Author: ebabun <ebabun@student.42belgium.be>
# Author: mmeurer <mmeurer@student.42belgium.be>
# Created: 2026/01/23 16:09:10
# Updated: 2026/01/28 16:09:10

"""A module to display a maze with ascii rendering."""
from .maze_renderer import MazeRenderer
from mazegen import MazeGenerator


class AsciiRenderer(MazeRenderer):
    """Render a maze in the terminal using ASCII characters."""

    def __init__(self, maze: MazeGenerator) -> None:
        """
        Initialize the ASCII renderer.

        Args:
            maze (MazeGenerator): The MazeGenerator instance to render.
        """
        super().__init__(maze)
        self.wall_colors = ["\033[27m", "\033[33m", "\033[32m", "\033[36m"]
        self.color_idx: int = 0
        self.w_col: str
        self.handle_user_interaction()

    @staticmethod
    def show_menu() -> None:
        """Display the list of available commands."""
        print("\n=== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. Rotate maze colors")
        print("4. Quit")

    @staticmethod
    def get_choice() -> tuple[str, bool]:
        """
        Get the user choice and check if it's valid.

        Returns:
            tuple[str, bool]: The selected choice and a flag indicating
            whether the choice is valid.
        """
        choice = input("Choice? (1-4): ")
        if choice in ("1", "2", "3", "4"):
            return choice, False
        else:
            return choice, True

    def new_maze(self) -> None:
        """Generate a new maze with the same configuration and display it."""
        new_maze: MazeGenerator = MazeGenerator(self.maze.config_file)
        if new_maze.display != "ascii":
            print(
                    "Info: exit program to switch "
                    f"to {new_maze.display} display"
                    )
        super().__init__(new_maze)
        self.handle_user_interaction()

    def display_maze(self) -> None:
        """Display the maze with entry, exit, and optional solution path."""
        acc_line = 0
        end_color = "\033[0m"
        line_top_border = (
            f"{self.w_col}+{end_color}"
            + f"{self.w_col}---+{end_color}" * self.maze.cols
        )
        print(line_top_border)
        for line in self.maze_hex[:-1].split("\n"):
            line_walls = f"{self.w_col}|{end_color}"
            line_bottom = f"{self.w_col}+{end_color}"
            acc_hexa = 0
            for hexa in line:
                # check the content
                if (acc_hexa, acc_line) == self.maze.entry:
                    cell_content = "\033[32m■\033[0m"
                elif (acc_hexa, acc_line) == self.maze.exit:
                    cell_content = "\033[31m■\033[0m"
                elif hexa == "F":
                    cell_content = "■"
                elif (self.show_soluce
                        and (acc_hexa, acc_line)
                        in self.path_coord):
                    cell_content = "\033[35m■\033[0m"
                else:
                    cell_content = " "

                # construct the maze with the content
                if hexa == "F":
                    line_walls += f" {cell_content} {self.w_col}|{end_color}"
                    line_bottom += f"{self.w_col}---+{end_color}"
                else:
                    if hexa in "2367ABE":
                        line_walls += (f" {cell_content} "
                                       f"{self.w_col}|{end_color}")
                    else:
                        line_walls += f" {cell_content}  "
                    if hexa in "4567CDE":
                        line_bottom += f"{self.w_col}---+{end_color}"
                    else:
                        line_bottom += f"   {self.w_col}+{end_color}"
                acc_hexa += 1
            print(line_walls)
            print(line_bottom)
            acc_line += 1

    def handle_user_interaction(self) -> None:
        """Display the maze and handle user interactions."""
        # clear and right placement (left corner)
        print("\033[2J")
        print("\033[H")
        print("Scroll up for configuration and errors feedback")
        while True:
            self.w_col = self.wall_colors[self.color_idx % 4]
            self.display_maze()
            # commands available and catch if not
            self.show_menu()
            choice, wrong = self.get_choice()
            if wrong:
                while wrong:
                    print("Invalid choice, please enter a number from 1 to 4.")
                    choice, wrong = self.get_choice()
                print("\033[2J")
            if choice == '1':
                self.new_maze()
                break
            elif choice == '2':
                print("\033[2J")
                print("\033[H")
                self.show_soluce = not self.show_soluce
            elif choice == '3':
                print("\033[2J")
                print("\033[H")
                self.color_idx += 1
            elif choice == '4':
                print("Bye! Thanks for playing ~")
                break

#!/usr/bin/env python3
# File: display_map.py
# Author: ebabun <ebabun@student.42belgium.be>
# Author: mmeurer <mmeurer@student.42belgium.be>
# Created: 2026/01/20 18:33:22
# Updated: 2026/01/20 18:02:15

# from mlx import Mlx
from enum import Enum
from a_maze_ing import MazeGenerator

TILE_SIZE = 30
COLOR_WALL = 0xFFFFFF
COLOR_BG = 0x222222


class Key(Enum):
    ESCAPE = 0xff1b


class MazeRenderer:
    """Create a window with a maze"""

    def __init__(self, config):
        self.maze = MazeGenerator(config)
        self.maze.generate_maze()
        self.filename = config["OUTPUT_FILE"]
        self.file = self.export_to_txt(config["OUTPUT_FILE"])

    def print_visual(self):
        self.maze.print_maze_visual()

    def export_to_txt(self) -> None:
        """To generate a file with the maze in hexadecimal"""
        try:
            with open(self.filename, "w") as f:
                for y in range(self.maze.rows):
                    line = ""
                    for x in range(self.maze.cols):
                        line += self.maze.grid[y][x].hex_repr
                    f.write(line + "\n")
        except Exception as e:
            print(f"Erreur lors de l'écriture du fichier: {e}")

    def open_file(self):
        try:
            with open(self.filename, "r") as f:
                lines = [line for line in f.readlines()]
        except FileNotFoundError:
            print(f"Erreur: le fichier {self.filename} est introuvable")
            return

        win_height = len(lines) * TILE_SIZE
        win_width = len(lines[0]) * TILE_SIZE


""" def main():
    m = Mlx()
    mlx_ptr = m.mlx_init()

    # Lire le fichier et calculer la taille
    try:
        with open(FILE_PATH, "r") as f:
            lines = [line for line in f.readlines()]
    except FileNotFoundError:
        print(f"Erreur: le fichier {FILE_PATH} est introuvable")
        return

    win_height = len(lines) * TILE_SIZE
    win_width = len(lines[0]) * TILE_SIZE

    # Créer la fenêtre
    win_ptr = m.mlx_new_window(mlx_ptr, win_width, win_height, "Title")

    # Gérer la fermeture (Echap pour quitter)
    def handle_key(key):
        if key == Key.ESCAPE:
            exit(0)

    m.mlx_key_hook(win_ptr, handle_key, None)

    # Lancer la boucle infinie
    m.mlx_loop(mlx_ptr) """


""" if __name__ == "__main__":
    main() """

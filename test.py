#!/usr/bin/env python3
# File: display_map.py
# Author: ebabun <ebabun@student.42belgium.be>
# Author: mmeurer <mmeurer@student.42belgium.be>
# Created: 2026/01/20 18:33:22
# Updated: 2026/01/20 18:02:15

from mlx import Mlx
from enum import Enum
# from a_maze_ing import MazeGenerator


def open_file(filename):
    try:
        with open(filename, "r") as f:
            lines = [line for line in f.readlines()]
    except FileNotFoundError:
        print(f"Erreur: le fichier {filename} est introuvable")
        return
    return lines

m = Mlx()
mlx_ptr = m.mlx_init()
win_ptr = m.mlx_new_window(mlx_ptr, 1080, 720, "=== A-Maze-ing ===")

class Key(Enum):
    ESCAPE = 65307
    FLECHE_HAUT = 65362
    FLECHE_DROITE = 65363
    FLECHE_BAS = 65364
    FLECHE_GAUCHE = 65361

"""
class MazeRenderer:
    Create a window with a maze

    def __init__(self, file):
        self.filename = file
        self.file = self.export_to_txt(file)

    def set_output():
        pass
"""


def mymouse(button, x, y, color):
    m.mlx_pixel_put(mlx_ptr, win_ptr, x, y, color)
    print(f"Got mouse event! button {button} at {x},{y}.")

def mykey(keynum, mystuff):
    print(f"Got key {keynum}, and got my stuff back:")
    print(mystuff)
    if keynum == 32:
        m.mlx_mouse_hook(win_ptr, None, None)
    elif keynum == Key.ESCAPE:
        gere_close()

def gere_close(dummy):
    m.mlx_destroy_window(mlx_ptr, win_ptr)
    m.mlx_loop_exit(mlx_ptr)
    
def main() -> None:
    lines = open_file("maze.txt")
    height = len(lines) * CELL_SIZE  # definir par rapport au reste
    width = len(lines[0]) * CELL_SIZE
    m.mlx_clear_window(mlx_ptr, win_ptr)
    m.mlx_string_put(mlx_ptr, win_ptr, width, height, 255, "Hello PyMlx!")  # commandes
    (ret, w, h) = m.mlx_get_screen_size(mlx_ptr)
    print(f"Got screen size: {w} x {h} .")

    stuff = [1, 2]
    m.mlx_mouse_hook(win_ptr, mymouse, 0x0000FF)
    m.mlx_key_hook(win_ptr, mykey, stuff)
    m.mlx_hook(win_ptr, 33, 0, gere_close, None)

    m.mlx_loop(mlx_ptr)

if __name__ == "__main__":
    main()

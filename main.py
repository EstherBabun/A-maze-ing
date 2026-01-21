#!/usr/bin/env python3
# File: maze.py
# Author: ebabun <ebabun@student.42belgium.be>
# Author: mmeurer <mmeurer@student.42belgium.be>
# Created: 2026/01/15 18:33:22
# Updated: 2026/01/20 18:02:15

"""Docstring to write. Version Morgane"""

import sys
from typing import Dict, Any
from a_maze_ing import MazeGenerator


def load_config(file: str) -> Dict[str, Any]:
    """Parse the config file and return the key,value pairs."""
    dict_config: dict[str, Any] = {}
    if file is None:
        print("Error: Cannot take None as config file")
        return None

    # read from file and create dict of strings:
    try:
        with open(file, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    dict_config[key.strip().upper()] = value.strip()
    except ValueError as e:
        print(f"Error in line {line}: {e}")
        return None
    except (FileNotFoundError, PermissionError) as e:
        print(f"Error: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

    # Convert numeric values, tuples and booleans
    for k, v in dict_config.items():
        try:
            # Numeric values for WIDTH and HEIGHT
            if k == "WIDTH" or k == "HEIGHT":
                dict_config[k] = int(v)
                # Raise error to prevent huge maze:
                # if dict_config[k] > MAX_SIZE(tbd) raise error

            # tuples for ENTRY and EXIT
            elif k == "ENTRY" or k == "EXIT":
                dict_config[k] = tuple(int(i.strip()) for i in v.split(','))
                if len(dict_config[k]) > 2:
                    raise ValueError(f'{k} expects 2 values "x,y"')
            # bool value for PERFECT
            elif k == "PERFECT":
                if v.upper() == "TRUE":
                    dict_config[k] = True
                elif v.upper() == "FALSE":
                    dict_config[k] = False
                else:
                    raise ValueError(f'{k} expects "True" or "False"')
            # path name of the OUTPUT_FILE
            elif k.upper() == "OUTPUT_FILE":
                dict_config[k] = v
            # which algo is choosen
            elif k == "ALGORITHM":
                if v == "Wilson" or v == "DFS":
                    dict_config[k] == v
                else:
                    raise ValueError(f'{k} expects "Wilson" or "DFS"')

            # discard invalid keys
            else:
                raise ValueError(
                        "Expected: WIDTH, HEIGHT, ENTRY, "
                        "EXIT, OUTPUT_FILE, PERFECT", "ALGORITHM"
                        )

        except Exception as e:
            print(f"Error in config file: {k}={v}\n{e}")
            return None

    # Handle invalid entry and exit points
    entry_x, entry_y = dict_config["ENTRY"]
    exit_x, exit_y = dict_config["EXIT"]
    w = dict_config["WIDTH"]
    h = dict_config["HEIGHT"]
    if entry_x < 0 or entry_y < 0 or entry_x > w - 1 or entry_y > h - 1:
        print("Error: Entry point exceeds borders of the maze.")
        return None
    if exit_x < 0 or exit_y < 0 or exit_x > w - 1 or exit_y > h - 1:
        print("Error: Exit point exceeds borders of the maze.")
        return None

    return dict_config


def main() -> None:
    """Docstring to write."""
    # check the arguments
    if len(sys.argv) != 2:
        print("Please pass a config file as argument")
        return

    # take the path to the config file
    config_file: str = sys.argv[1]

    # parse config file into a dict
    config: Dict[str, Any] = load_config(config_file)
    if config is None:
        return

    my_maze: MazeGenerator = MazeGenerator(config)
    my_maze.generate_maze()
    my_maze.print_maze_visual()
    my_maze.export_to_txt()


if __name__ == "__main__":
    main()

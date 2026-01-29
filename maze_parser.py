#!/usr/bin/env python3
# File: maze_parser.py
# Author: ebabun <ebabun@student.42belgium.be>
# Author: mmeurer <mmeurer@student.42belgium.be>
# Created: 2026/01/29 00:00:00
# Updated: 2026/01/29 00:00:00

"""
A module to parse maze configuration files.

This module provides the MazeParser class which handles reading and
validating configuration files for maze generation.
"""

from typing import Dict, List, Tuple, Optional


class MazeParser:
    """
    Parse and validate maze configuration files.

    This class reads configuration files and validates all parameters
    according to the maze requirements.

    Attributes:
        cols (int): Width of the maze (number of cells)
        rows (int): Height of the maze (number of cells)
        seed (int | None): Random seed for reproducibility
        perfect (bool): Whether the maze should be perfect
        entry (tuple): Entry coordinates (x, y)
        exit (tuple): Exit coordinates (x, y)
        output_file (str): Name of the output file
        algorithm (str): Maze generation algorithm (DFS or WILSON)
        display (str): Display mode (ASCII or MLX)
    """

    def __init__(self, config_file: Optional[str] = None) -> None:
        """
        Initialize the parser with default values.

        Args:
            config_file (str | None): Path to configuration file,
                                     or None for defaults
        """
        # Set defaults first (exactly like original MazeGenerator)
        self.cols: int = 20
        self.rows: int = 10
        self.seed: Optional[int] = None
        self.perfect: bool = True
        self.entry: Tuple[int, int] = (0, 0)
        self.exit: Tuple[int, int] = (self.cols - 1, self.rows - 1)
        self.output_file: str = "maze.txt"
        self.algorithm: str = "wilson"
        self.display: str = "mlx"

        # Track which settings came from config file
        self._custom_keys: List[str] = []

        # Load config file if provided
        if config_file is not None:
            self._load_config(config_file)
        # Note: print_config() will be called by MazeGenerator after validation

    def _load_config(self, config_file: str) -> None:
        """
        Load and parse the configuration file.

        Args:
            config_file (str): Path to the configuration file
        """
        raw_config = self._read_config_file(config_file)
        if raw_config is not None:
            self._custom_keys = self._parse_config_values(raw_config)
            
            # Adjust default exit if WIDTH/HEIGHT changed but EXIT wasn't specified
            if ("WIDTH" in self._custom_keys or "HEIGHT" in self._custom_keys) and \
               "EXIT" not in self._custom_keys:
                self.exit = (self.cols - 1, self.rows - 1)

    def _read_config_file(self, file: str) -> Optional[Dict[str, str]]:
        """
        Read config file and return raw dict or None on error.

        Args:
            file (str): Path to the configuration file

        Returns:
            Dict[str, str] | None: Raw configuration dictionary or None on error
        """
        try:
            with open(file, "r") as f:
                content: str = f.read()
                if content == '':
                    print("Config file is empty")
                    return None

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

        Args:
            raw_config (Dict[str, str]): Raw configuration key-value pairs

        Returns:
            List[str]: List of successfully parsed keys
        """
        custom: List[str] = []

        for k, v in raw_config.items():
            try:
                if k == "WIDTH":
                    if int(v) < 2:
                        raise ValueError("width cannot be less than 2")
                    self.cols = int(v)
                    custom.append(k)
                elif k == "HEIGHT":
                    if int(v) < 2:
                        raise ValueError("height cannot be less than 2")
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
                            f'Invalid algorithm "{v}" pick DFS or WILSON'
                        )
                    self.algorithm = v.upper()
                    custom.append(k)
                elif k == "DISPLAY":
                    if v.upper() not in ["ASCII", "MLX"]:
                        raise ValueError(
                            f'Invalid display "{v}" pick ASCII or MLX'
                        )
                    self.display = v.upper()
                    custom.append(k)
                else:
                    print(
                        f"Error: Invalid keyword {k} - "
                        "Allowed: WIDTH, HEIGHT, ENTRY, EXIT, "
                        "OUTPUT_FILE, PERFECT, SEED, ALGORITHM, DISPLAY"
                    )
            except Exception as e:
                print(f'Error in {k}: {e}\nSwitching to default {k.lower()}')

        return custom

    def _parse_coordinate(self, value: str, key: str) -> Tuple[int, int]:
        """
        Parse a coordinate string 'x,y' into a tuple.

        Args:
            value (str): Coordinate string in format "x,y"
            key (str): Configuration key name (for error messages)

        Returns:
            Tuple[int, int]: Parsed coordinates

        Raises:
            ValueError: If coordinate format is invalid
        """
        coord_tuple = tuple(int(i.strip()) for i in value.split(','))
        if len(coord_tuple) != 2:
            raise ValueError('coordinates expect 2 values "x,y"')
        return coord_tuple

    def _parse_boolean(self, value: str, key: str) -> bool:
        """
        Parse a boolean value from string.

        Args:
            value (str): String representation of boolean
            key (str): Configuration key name (for error messages)

        Returns:
            bool: Parsed boolean value

        Raises:
            ValueError: If value is not a valid boolean representation
        """
        value_upper = value.strip().upper()
        if value_upper in ["TRUE", "1", "YES", "Y"]:
            return True
        elif value_upper in ["FALSE", "0", "NO", "N"]:
            return False
        else:
            raise ValueError(
                f'Invalid boolean value "{value}" - '
                'use True/False, 1/0, Yes/No, or Y/N'
            )

    def print_config(self) -> None:
        """Print the final maze configuration."""
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
            if k in self._custom_keys:
                print(f"  {k}: {v}")
            else:
                print(f"  {k}: {v} (default)")
        print()


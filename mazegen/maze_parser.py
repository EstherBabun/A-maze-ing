# File: mazegen/maze_parser.py
# Author: ebabun <ebabun@student.42belgium.be>
# Author: mmeurer <mmeurer@student.42belgium.be>
# Created: 2026/01/29 00:00:00
# Updated: 2026/01/29 00:00:00

"""
A module to parse maze configuration files.

This module provides the MazeParser class which handles reading and
validating configuration files for maze generation.
"""


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
        algorithm (str): Maze generation algorithm (dfs or wilson)
        display (str): Display mode (None, ascii or mlx)
    """

    def __init__(self, config_file: str | None = None) -> None:
        """
        Initialize the parser with default values.

        Args:
            config_file (str | None): Path to configuration file,
                                     or None for defaults
        """
        # Set defaults first (exactly like original MazeGenerator)
        self.config_file = config_file
        self.cols: int = 20
        self.rows: int = 10
        self.seed: int | None = None
        self.perfect: bool = True
        self.entry: tuple[int, int] = (0, 0)
        self.exit: tuple[int, int] = (self.cols - 1, self.rows - 1)
        self.output_file: str = "maze.txt"
        self.algorithm: str = "wilson"
        self.display: str | None = None

        # Track if max width or height have been enforced
        self.max: bool = False
        # Track which settings came from config file
        self._custom_keys: list[str] = []
        # Track if there was a file error
        self._config_loaded = False

        # Load config file if provided
        if config_file is not None:
            self._load_config(config_file)

        # store coordinates of the 42 pattern
        self.ft_walls: list[tuple[int, int]] = self.get_42_cells(
                self.cols,
                self.rows
                )

        # Check that entry/exit points are valid
        self._validate_entry_exit()

        # print the final, validated configuration
        self._print_final_config()

    def _load_config(self, config_file: str) -> None:
        """
        Load and parse the configuration file.

        Args:
            config_file (str): Path to the configuration file
        """
        raw_config = self._read_config_file(config_file)
        if raw_config is not None:
            self._custom_keys = self._parse_config_values(raw_config)
            self._config_loaded = True

    def _read_config_file(self, file: str) -> dict[str, str] | None:
        """
        Read config file and return raw dict or None on error.

        Args:
            file (str): Path to the configuration file

        Returns:
            dict[str, str] | None: Raw configuration dictionary
        """
        try:
            with open(file, "r") as f:
                content: str = f.read()
                if content == '':
                    print("\nError: Config file is empty")
                    return None

                print(f"\nLoading settings from config file {file}...")
                raw_config: dict[str, str] = {}

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

    def _parse_config_values(self, raw_config: dict[str, str]) -> list[str]:
        """
        Parse and validate each config value.

        Args:
            raw_config (dict[str, str]): Raw configuration key-value pairs

        Returns:
            custom (list[str]) List of successfully parsed keys
        """
        custom: list[str] = []

        for k, v in raw_config.items():
            try:
                if k == "WIDTH":
                    if int(v) < 2:
                        raise ValueError("width cannot be less than 2")
                    if int(v) > 350:
                        self.max = True
                        self.cols = 350
                        raise ValueError("width cannot be more than 350")
                    self.cols = int(v)
                    custom.append(k)
                elif k == "HEIGHT":
                    if int(v) < 2:
                        raise ValueError("height cannot be less than 2")
                    if int(v) > 200:
                        self.max = True
                        self.rows = 200
                        raise ValueError("height cannot be more than 200")
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
                    if v.upper() != "NONE":
                        self.seed = int(v)
                    custom.append(k)
                elif k == "OUTPUT_FILE":
                    self.output_file = self._parse_output_file(v, k)
                    custom.append(k)
                elif k == "ALGORITHM":
                    if v.upper() not in ["DFS", "WILSON"]:
                        raise ValueError(
                            f'Invalid algorithm "{v}" pick DFS or WILSON'
                        )
                    self.algorithm = v.lower()
                    custom.append(k)
                elif k == "DISPLAY":
                    import importlib.util
                    if v.upper() in ("ASCII", "MLX"):
                        module = "renderers." + v.lower() + "_renderer"
                        if importlib.util.find_spec(module) is None:
                            raise ImportError(
                                    f"Rendering module '{module}'"
                                    "is not available"
                                    )
                    if v.upper() not in ["NONE", "ASCII", "MLX"]:
                        raise ValueError(
                            f'Invalid display "{v}" pick NONE, ASCII or MLX'
                        )
                    if v.upper() != "NONE":
                        self.display = v.lower()
                    custom.append(k)
                else:
                    print(
                            f"Error: Invalid keyword {k} - "
                            "Allowed: WIDTH, HEIGHT, ENTRY, EXIT, "
                            "OUTPUT_FILE, PERFECT, SEED, "
                            "ALGORITHM, DISPLAY"
                            )
            except Exception as e:
                print(f'Error in {k}: {e}')
                if self.max and (k == "WIDTH" or k == "HEIGHT"):
                    print(f'Enforcing max {k.lower()}')
                elif k == "DISPLAY":
                    print('Aborting rendering')
                else:
                    print(f'Switching to default {k.lower()}')

        if self.display and not self.is_displayable:
            print(f"Error: Size is too big for {self.display} rendering")
            print("Aborting rendering")
            self.display = None
            custom.remove("DISPLAY")

        return custom

    def _parse_coordinate(self, value: str, key: str) -> tuple[int, int]:
        """
        Parse a coordinate string 'x,y' into a tuple.

        Args:
            value (str): Coordinate string in format "x,y"
            key (str): Configuration key name (for error messages)

        Returns:
            coord_tuple (tuple[int, int]): Parsed coordinates

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

    def _parse_output_file(self, value: str, key: str) -> str:
        """
        Parse a output_file name from string.

        Args:
            value (str): String representation of path/to/output_file
            key (str): Configuration key name (for error messages)

        Returns:
            str: Parsed string value

        Raises:
            File related Errors: If value is not a valid file path
        """
        import os
        if not value.endswith('.txt'):
            value = value + '.txt'
            print(f"Info: Added .txt extension to output file: {value}")
        # check the directory of output_file
        directory = os.path.dirname(value) or "."
        if not os.path.isdir(directory):
            raise FileNotFoundError(
                        f'Directory does not exist: "{directory}"'
                        )
        if not os.access(directory, os.W_OK):
            raise PermissionError(
                        f'No write permission in: "{directory}"'
                        )
        # check the basename of output file
        basename = os.path.basename(value)
        if not basename or basename == '.txt':
            raise ValueError(f'Invalid output filename: "{value}"')
        if len(basename) > 255:
            raise ValueError(
                    f'Filename too long: {len(basename)} chars (max 255)'
                    )
        return value

    def get_42_cells(self, w: int, h: int) -> list[tuple[int, int]]:
        """Calculate the coordinates of the 42 cells."""
        if w < 11 or h < 9:
            print("Warning: Maze too small for '42' pattern")
            return []  # No 42_walls, maze too small
        cx: int = (w - 1) // 2 if w % 2 == 0 else w // 2
        cy: int = (h - 1) // 2 if h % 2 == 0 else h // 2

        four_walls: list[tuple[int, int]] = [
                (cx - 1, cy), (cx - 2, cy), (cx - 3, cy),
                (cx - 1, cy + 1), (cx - 1, cy + 2),
                (cx - 3, cy - 1), (cx - 3, cy - 2)
                ]
        two_walls: list[tuple[int, int]] = [
                (cx + 1, cy), (cx + 2, cy), (cx + 3, cy),
                (cx + 1, cy + 1), (cx + 1, cy + 2),
                (cx + 3, cy - 1), (cx + 3, cy - 2),
                (cx + 1, cy - 2), (cx + 2, cy - 2),
                (cx + 2, cy + 2), (cx + 3, cy + 2)
                ]

        return four_walls + two_walls

    def _is_within_bounds(self, coord: tuple[int, int]) -> bool:
        """Check if a coordinate is within maze bounds."""
        x, y = coord
        if 0 <= x < self.cols and 0 <= y < self.rows:
            return True
        return False

    def reset_default_entry_exit(self, point_type: str) -> None:
        """Reset entry or exit to default value and remove from custom keys."""
        if point_type == "ENTRY":
            self.entry = (0, 0)
            # Remove from custom keys since we're resetting to default
            if "ENTRY" in self._custom_keys:
                self._custom_keys.remove("ENTRY")
        elif point_type == "EXIT":
            self.exit = (self.cols - 1, self.rows - 1)
            # Remove from custom keys since we're resetting to default
            if "EXIT" in self._custom_keys:
                self._custom_keys.remove("EXIT")

    def _validate_entry_exit(self) -> None:
        """Validate entry/exit by checking maze bounds and 42 cells."""
        # Adjust default exit if WIDTH/HEIGHT changed
        # but EXIT wasn't specified
        if "EXIT" not in self._custom_keys:
            if ("WIDTH" in self._custom_keys
                    or "HEIGHT" in self._custom_keys
                    or self.max):
                self.exit = (self.cols - 1, self.rows - 1)

        # Check if entry/exit coordinates are within maze bounds
        if not self._is_within_bounds(self.entry):
            print(
                    "Error: Entry point exceeds borders of the maze.\n"
                    'Switching to default entry'
                    )
            self.reset_default_entry_exit("ENTRY")
        if not self._is_within_bounds(self.exit):
            print(
                    "Error: Exit point exceeds borders of the maze.\n"
                    'Switching to default exit'
                    )
            self.reset_default_entry_exit("EXIT")

        # Check if entry/exit coordinates conflict with 42 blocked cells
        if self.entry in self.ft_walls:
            print(
                    "Error: Entry point is stuck in the 42 pattern\n"
                    "Switching to default entry"
                    )
            self.reset_default_entry_exit("ENTRY")
        if self.exit in self.ft_walls:
            print(
                    "Error: Exit point is stuck in the 42 pattern\n"
                    "Switching to default exit"
                    )
            self.reset_default_entry_exit("EXIT")

        if self.entry == self.exit:
            print(
                    "Error: Entry and exit cannot have "
                    "the same coordinates"
                    )
            if self.entry != (0, 0):
                self.reset_default_entry_exit("ENTRY")
                print("Switching to default entry")
            if self.entry == self.exit:
                self.reset_default_entry_exit("EXIT")
                print("Switching to default exit")

    @property
    def is_displayable(self) -> bool:
        """
        Check if maze dimensions are compatible with rendering.

        Returns:
            bool: True if dimensions are safe, False otherwise
        """
        return self.cols <= 320 and self.rows <= 150

    def _print_final_config(self) -> None:
        """
        Print the final validated configuration.

        This is called AFTER entry/exit validation to ensure the printed
        values reflect the actual configuration that will be used.
        """
        if self.config_file is None:
            print("No config file, switching to default settings.")
        elif not self._config_loaded:
            print("Switching to default settings")

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
                if k == "WIDTH" and self.cols == 350:
                    print(f"  {k}: {v} (max)")
                elif k == "HEIGHT" and self.rows == 200:
                    print(f"  {k}: {v} (max)")
                else:
                    print(f"  {k}: {v} (default)")
        print()

        if not self.display:
            if self.cols > 120 and self.rows > 60:
                print("Warning: Maze is quite large (be patient!)")
            print(f"Encoding maze in {self.output_file}...")
        else:
            # print max size warning messages
            if not self.is_displayable:
                print("Warning: Maze is too large for rendering")
                print("Maximum displayable size: 320x150\n")
                print(f"Encoding maze in {self.output_file}... (be patient!)")

            elif self.cols > 120 and self.rows > 60:
                print("Warning: Maze is quite large")
                print("Consider generating a smaller maze")
                print("for faster rendering and better visibility")
                print("Recommended size for big mazes: 120x60\n")
                print("Rendering... (this might take a few minutes)")

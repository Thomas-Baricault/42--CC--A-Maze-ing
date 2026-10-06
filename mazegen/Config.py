from __future__ import annotations
from typing import Any, Callable, Dict, Optional, Tuple
from .Algorithm import Algorithm
from .Position import Position


class Config:
    """Representation of the maze config

    Attributes
    ----------
    width : int
        The width of the maze
    height : int
        The height of the maze
    entry : Position
        The entry position
    exit : Position
        The exit position
    output_file : str
        The file in which the resulting maze will be write
    perfect : bool
        If the maze need to be perfect
    seed : int | None
        The seed of the maze (timestamp by default)
    algorithm : Algorithm
        The algorithm to use (deep-first search by default)

    Static Methods
    --------------
    open(path) -> Config:
        Open an read a configuration file

    Methods
    -------
    save(path) -> None
        Save the config to a file
    """

    class ConfigError(Exception):
        """Base class for config errors"""

        def __init__(self, message: str) -> None:
            """
            Parameters
            ----------
            message : str
                The error message
            """

            super().__init__(f"Config Error: {message}")

    class FileError(ConfigError):
        """Error class for config file errors"""

        def __init__(self, path: str, message: str) -> None:
            """
            Parameters
            ----------
            path : str
                The path of the file
            message : str
                The error message
            """

            super().__init__(f"{message}, with path '{path}'")

    class SyntaxError(ConfigError):
        """Error class for syntax errors in config files"""

        def __init__(self, line: int) -> None:
            """
            Parameters
            ----------
            line : int
                The line of the error
            """

            super().__init__(f"Syntax error at line {line}")

    class MissingKeyError(ConfigError):
        """Error class for missing key error in config file"""

        def __init__(self, key: str) -> None:
            """
            Parameters
            ----------
            key : str
                The missing key
            """

            super().__init__(f"Missing key '{key}'")

    class UnknownKeyError(ConfigError):
        """Error class for unknown keys in config file"""

        def __init__(self, key: str) -> None:
            """
            Parameters
            ----------
            key : str
                The unknown key
            """

            super().__init__(f"Unknown key '{key}'")

    class ValueError(ConfigError):
        """Error class for key value errors in config file"""

        def __init__(self, key: str, given: str, message: str) -> None:
            """
            Parameters
            ----------
            key : str
                The key
            given : str
                The given value
            message : str
                The error message
            """

            super().__init__(f"Invalid value for key '{key}', given '{given}'"
                             + f", {message}")

    class ParameterError(ConfigError):
        """Error class for invalid parameter values"""

        def __init__(self, parameter: str, message: str) -> None:
            """
            Parameters
            ----------
            parameter : str
                The parameter in error
            message : str
                The error message
            """

            super().__init__(f"Parameter {parameter}, {message}")

    @staticmethod
    def _parse_uint(s: str) -> int:
        try:
            n = int(s)
        except ValueError:
            raise ValueError(f"cannot convert '{s}' to number")
        if n < 0:
            raise ValueError("negative numbers are not allowed")
        return n

    @staticmethod
    def _parse_bool(s: str) -> bool:
        if s == "True":
            return True
        if s == "False":
            return False
        raise ValueError(f"cannot convert '{s}' to boolean")

    _KEYS: Dict[str, Tuple[Callable[..., Any], Any]] = {
        "WIDTH": (_parse_uint, None),
        "HEIGHT": (_parse_uint, None),
        "ENTRY": (Position, None),
        "EXIT": (Position, None),
        "OUTPUT_FILE": (str, None),
        "PERFECT": (_parse_bool, None),
        "SEED": (_parse_uint, None),
        "ALGORITHM": (Algorithm, Algorithm.DEFAULT)
    }

    @staticmethod
    def open(path: str) -> Config:
        """Open and read a configuration file

        Parameters
        ----------
        path : str
            The path of the file

        Returns
        -------
        Config
            The config object loaded

        Raises
        ------
        Config.FileError
            If the file cannot be read
        Config.SyntaxError
            If the file syntax is invalid
        Config.MissingKeyError
            If a mandatory key is missing in the file
        Config.UnknownKeyError
            If a given key is unknown
        Config.ValueError
            If the value given for a key is invalid
        """

        found: Dict[str, str] = {}
        try:
            with open(path) as file:
                for index, line in enumerate(file.readlines()):
                    if line.endswith('\n'):
                        line = line[:-1]
                    if line != "" and not line.startswith('#'):
                        parts = line.split('=')
                        if len(parts) != 2:
                            raise Config.SyntaxError(index + 1)
                        key, value = parts
                        found[key] = value
        except FileNotFoundError:
            raise Config.FileError(path, "File not found")
        except PermissionError:
            raise Config.FileError(path, "Unauthorized to read file")
        for key, data in Config._KEYS.items():
            if data[1] is None and key != "SEED" and key not in found:
                raise Config.MissingKeyError(key)
        for key in found:
            if key not in Config._KEYS:
                raise Config.UnknownKeyError(key)
        properties = {}
        for key, value in found.items():
            constructor = Config._KEYS[key][0]
            try:
                value = constructor(value)
            except ValueError as e:
                raise Config.ValueError(key, value, str(e))
            properties[key.lower()] = value
        return Config(**properties)

    def __init__(self, width: int, height: int, entry: Position,
                 exit: Position, output_file: str, perfect: bool,
                 seed: Optional[int] = None,
                 algorithm: Algorithm = Algorithm.DEFAULT) -> None:
        """
        Parameters
        ----------
        width : int
            The width of the maze
        height : int
            The height of the maze
        entry : Position
            The entry position
        exit : Position
            The exit position
        output_file : str
            The file in which the resulting maze will be write
        perfect : bool
            If the maze need to be perfect
        seed : Optional[int]
            The seed of the maze (timestamp by default)
        algorithm : Algorithm
            The algorithm to use (deep-first search by default)

        Raises
        ------
        Config.ParameterError
            If width, height, or seed is negative
        """

        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.output_file = output_file
        self.perfect = perfect
        self.seed = seed
        self.algorithm = algorithm

    def __str__(self) -> str:
        """Returns a readable form of the configuration

        Returns
        -------
        str
            String that represent the configuration
        """

        res = ""
        for key in Config._KEYS:
            value = getattr(self, key.lower())
            if not (key == "SEED" and value is None or
                    key == "ALGORITHM" and value == Algorithm.DEFAULT):
                res += f"{key}={value}\n"
        return res

    @property
    def width(self) -> int:
        """The width of the maze

        Returns
        -------
        int
            The width
        """

        return self._width

    @width.setter
    def width(self, value: int) -> None:
        """Set the width

        Parameters
        ----------
        value : int
            The value

        Raises
        ------
        Config.ParameterError
            If the given value is negative
        """

        if value < 0:
            raise Config.ParameterError("width", "Width cannot be negative")
        self._width = int(value)

    @property
    def height(self) -> int:
        """The height of the maze

        Returns
        -------
        int
            The height
        """

        return self._height

    @height.setter
    def height(self, value: int) -> None:
        """Set the height

        Parameters
        ----------
        value : int
            The value

        Raises
        ------
        Config.ParameterError
            If the given value is negative
        """

        if value < 0:
            raise Config.ParameterError("height", "Height cannot be negative")
        self._height = int(value)

    @property
    def entry(self) -> Position:
        """The entry position

        Returns
        -------
        Position
            The position
        """

        return self._entry

    @entry.setter
    def entry(self, value: Position) -> None:
        """Set the entry

        Parameters
        ----------
        value : Position
            The position
        """

        self._entry = value

    @property
    def exit(self) -> Position:
        """The exit position

        Returns
        -------
        Position
            The position
        """

        return self._exit

    @exit.setter
    def exit(self, value: Position) -> None:
        """Set the exit

        Parameters
        ----------
        value : Position
            The position
        """

        self._exit = value

    @property
    def output_file(self) -> str:
        """The output file path

        Returns
        -------
        str
            The path
        """

        return self._output_file

    @output_file.setter
    def output_file(self, value: str) -> None:
        """Set the output file path

        Parameters
        ----------
        value : str
            The path
        """

        self._output_file = value

    @property
    def perfect(self) -> bool:
        """If the maze is perfect

        Returns
        -------
        bool
            True if is perfect, False otherwise
        """

        return self._perfect

    @perfect.setter
    def perfect(self, value: bool) -> None:
        """Set if the maze is perfect

        Parameters
        ----------
        value : bool
            The value
        """

        self._perfect = value

    @property
    def seed(self) -> int | None:
        """The seed of the maze

        Returns
        -------
        int | None
            The seed, None to use the timestamp
        """

        return self._seed

    @seed.setter
    def seed(self, value: int | None) -> None:
        """Set the seed

        Parameters
        ----------
        value : int
            The value

        Raises
        ------
        Config.ParameterError
            If the given value is negative
        """

        if value is None:
            self._seed = value
        else:
            if value < 0:
                raise Config.ParameterError("seed", "Seed cannot be negative")
            self._seed = int(value)

    @property
    def algorithm(self) -> Algorithm:
        """The algorithm to use

        Returns
        -------
        Algorithm
            The algorithm
        """

        return self._algorithm

    @algorithm.setter
    def algorithm(self, value: Algorithm) -> None:
        """Set the algorithm to use

        Parameters
        ----------
        value : Algorithm
            The algorithm
        """

        self._algorithm = value

    def save(self, path: str) -> None:
        """Save the config to a file

        Parameters
        ----------
        path : str
            The path of the file

        Raises
        ------
        Config.FileError
            If the file cannot be write
        """

        try:
            with open(path, "w") as file:
                file.write(str(self) + '\n')
        except PermissionError:
            raise Config.FileError(path, "Unauthorized to write file")
        except Exception as e:
            raise Config.FileError(path, str(e))

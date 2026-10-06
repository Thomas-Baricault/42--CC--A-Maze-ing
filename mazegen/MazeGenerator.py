from __future__ import annotations
from random import choice, randint, seed as set_seed, shuffle
from time import time
from typing import Callable, List, Optional, Tuple, TypeAlias
from .Algorithm import Algorithm
from .Cell import Cell
from .Direction import Direction
from .Position import Position


class MazeGenerator:
    """A generator for mazes

    Attributes
    ----------
    Callback : TypeAlias
        Function type used for generation callback, equal to
        Callable[[Cell, Direction], None]
    """

    Callback: TypeAlias = Callable[[Cell, Direction], None]

    class MazeError(Exception):
        """Base class for maze errors"""

        def __init__(self, message: str) -> None:
            """
            Parameters
            ----------
            message : str
                The error message
            """

            super().__init__(f"Maze Error: {message}")

    class FileError(MazeError):
        """Error class for maze file errors"""

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

    class SyntaxError(MazeError):
        """Error class for syntax errors in maze files"""

        def __init__(self, line: int, message: str) -> None:
            """
            Parameters
            ----------
            line : int
                The line of the error
            message : str
                The error message
            """

            super().__init__(f"Syntax error at line {line}, {message}")

    class ParameterError(MazeError):
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

    class GridError(MazeError):
        """Error class for grid errors"""

        def __init__(self, message: str) -> None:
            """
            Parameters
            ----------
            message : str
                The error message
            """

            super().__init__(f"Cells grid error, {message}")

    class PathError(MazeError):
        """Error class for path errors"""

        def __init__(self, message: str) -> None:
            """
            Parameters
            ----------
            message : str
                The error message
            """

            super().__init__(f"Path error, {message}")

    @staticmethod
    def open(path: str) -> MazeGenerator:
        """Open and read a maze file

        Parameters
        ----------
        path : str
            The path of the file

        Returns
        -------
        MazeGenerator
            The maze generator object loaded

        Raises
        ------
        MazeGenerator.FileError
            If the file cannot be read
        MazeGenerator.SyntaxError
            If the file syntax is invalid
        """

        try:
            with open(path) as file:
                cells: List[str] = []
                part = 0
                for index, line in enumerate(file.readlines()):
                    if (part == 5 or part == 4 and line != "" or part < 4 and
                            not line.endswith('\n')):
                        raise MazeGenerator.SyntaxError(
                            index + 1,
                            "unexpected informations"
                        )
                    line = line[:-1]
                    if line == "":
                        if part > 0:
                            raise MazeGenerator.SyntaxError(
                                index + 1,
                                "unexpected empty line"
                            )
                        elif len(cells) == 0:
                            raise MazeGenerator.SyntaxError(
                                index + 1,
                                "no maze cells provided"
                            )
                        part += 1
                    elif part == 0:
                        cells.append(line)
                    else:
                        if part == 1:
                            entry = Position(line)
                        elif part == 2:
                            exit = Position(line)
                        elif part == 3:
                            path = line
                        part += 1
                width = len(cells[0])
                generator = MazeGenerator(width, len(cells), entry, exit)
                for index, line in enumerate(cells):
                    if len(line) != width:
                        raise MazeGenerator.SyntaxError(
                            index + 1,
                            "maze have lines of different width"
                        )
                    for x in range(width):
                        generator[Position(x, index)].value = cells[index][x]
                generator._path = [Direction(c) for c in path]
                generator.check_cells()
                generator.check_path()
                return generator
        except FileNotFoundError:
            raise MazeGenerator.FileError(path, "File not found")
        except PermissionError:
            raise MazeGenerator.FileError(path, "Unauthorized to read file")

    def __init__(self, width: int, height: int,
                 entry: Tuple[int, int] | Position,
                 exit: Tuple[int, int] | Position, perfect: bool = True,
                 algorithm: Algorithm = Algorithm.DEFAULT) -> None:
        """
        Parameters
        ----------
        width : int
            The width of the maze
        height : int
            The height of the maze
        entry : Tuple[int, int] | Position
            The entry position
        exit : Tuple[int, int] | Position
            The exit position
        perfect : bool
            If the maze need to be perfect
        algorithm : Algorithm
            The algorithm to use (deep-first search by default)

        Raises
        ------
        MazeGenerator.ParameterError
            If width or height is lower than 2, or if entry or exit isn't in
            maze bounds, or if entry and exit are at the same position
        """

        entry = Position(entry)
        exit = Position(exit)
        if width < 2:
            raise MazeGenerator.ParameterError(
                "width",
                "maze width cannot be less than 2"
            )
        if height < 2:
            raise MazeGenerator.ParameterError(
                "height",
                "maze height cannot be less than 2"
            )
        if not (0 <= entry.x < width and 0 <= entry.y < height):
            raise MazeGenerator.ParameterError(
                "entry",
                "entry have to be in maze bounds"
            )
        if not (0 <= exit.x < width and 0 <= exit.y < height):
            raise MazeGenerator.ParameterError(
                "exit",
                "exit have to be in maze bounds"
            )
        if entry == exit:
            raise MazeGenerator.ParameterError(
                "entry/exit",
                "entry and exit must be distinct"
            )
        self._width = width
        self._height = height
        self._entry = entry
        self._exit = exit
        self._perfect = perfect
        self._algorithm = algorithm
        self._path: List[Direction] = []
        self._seed: int | None = None
        self._generate_cells()

    def __getitem__(self, pos: Tuple[int, int] | Position) -> Cell:
        """Returns the cell at a given position in the maze

        Parameters
        ----------
        pos : Tuple[int, int] | Position
            The cell position

        Returns
        -------
        Cell
            The cell

        Raises
        ------
        MazeGenerator.ParameterError
            If the given position isn't in maze bounds
        """

        pos = Position(pos)
        if not (0 <= pos.x < self.width and 0 <= pos.y < self.height):
            raise MazeGenerator.ParameterError("pos",
                                               f"position {pos} not in grid")
        return self._cells[self.width * pos.y + pos.x]

    @property
    def width(self) -> int:
        """The maze width

        Returns
        -------
        int
            The width
        """

        return self._width

    @property
    def height(self) -> int:
        """The maze height

        Returns
        -------
        int
            The height
        """

        return self._height

    @property
    def entry(self) -> Position:
        """The maze entry position

        Returns
        -------
        Position
            The entry position
        """

        return self._entry

    @property
    def exit(self) -> Position:
        """The maze exit position

        Returns
        -------
        Position
            The exit position
        """

        return self._exit

    @property
    def perfect(self) -> bool:
        """If the maze is perfect

        Returns
        -------
        bool
            True if the maze is perfect, False otherwise
        """

        return self._perfect

    @property
    def seed(self) -> int | None:
        """The maze seed

        Returns
        -------
        int
            The seed
        """

        return self._seed

    @property
    def algorithm(self) -> Algorithm:
        """The algorithm used to generate the maze

        Returns
        -------
        Algorithm
            The algorithm
        """

        return self._algorithm

    @property
    def path(self) -> List[Direction]:
        """The maze path from entry to exit

        Returns
        -------
        List[Direction]
            A list of direction representing the path
        """

        return list(self._path)

    def check_cells(self) -> bool:
        """Check if the maze informations are valids

        Returns
        -------
        bool
            True if the maze is valid

        Raises
        ------
        MazeGenerator.GridError
            If the maze information contains errors
        """

        for cell in self._cells:
            for direction in Direction:
                if cell.has_neighbour(direction):
                    if cell.is_open(direction) != cell.neighbour(
                            direction).is_open(direction.opposite()):
                        raise MazeGenerator.GridError(
                            "the grid contains contradicting walls"
                            + " informations")
                elif cell.is_open(direction):
                    raise MazeGenerator.GridError("the grid isn't closed")
        return True

    def check_path(self) -> bool:
        """Check if the path is valid

        Returns
        -------
        bool
            True if the path is valid

        Raises
        ------
        MazeGenerator.PathError
            If the path is invalid
        """

        cell = self[self.entry]
        for step in self._path:
            print(step)
            if cell.is_closed(step):
                raise MazeGenerator.PathError("walked across a closed wall")
            elif not cell.has_neighbour(step):
                raise MazeGenerator.PathError("walked out of the maze")
            cell = cell.neighbour(step)
        if cell.pos != self.exit:
            raise MazeGenerator.PathError("path doesn't reach the exit")
        return True

    def save(self, path: str) -> None:
        """Save the maze to a file

        Parameters
        ----------
        path : str
            The path of the file

        Raises
        ------
        MazeGenerator.FileError
            If the file cannot be write
        """

        try:
            with open(path, "w") as file:
                for y in range(self.height):
                    for x in range(self.width):
                        file.write(str(self[Position(x, y)]))
                    file.write('\n')
                file.write("\n")
                file.write(f"{self.entry}\n")
                file.write(f"{self.exit}\n")
                file.write(''.join(map(lambda d: str(d), self._path)))
                file.write("\n")
        except PermissionError:
            raise MazeGenerator.FileError(path, "Unauthorized to write file")
        except Exception as e:
            raise MazeGenerator.FileError(path, str(e))

    def generate(self, seed: Optional[int] = None,
                 callback: Optional[Callback] = None) -> None:
        """Generate the maze

        Parameters
        ----------
        seed : Optional[int]
            The seed to use (default is None meaning timestamp)
        callback : Optional[Callback]
            The callback function to call when a wall is open or close
        """

        try:
            if seed is None:
                self._seed = int(time() * 1000)
            else:
                self._seed = seed
            set_seed(self.seed)
            self._generate_cells()
            getattr(self, f"_{self.algorithm.value.lower()}")(callback)
            self._open_random_walls(callback)
            self._find_path()
        except Exception as e:
            self._path = []
            self._seed = None
            raise e

    def _bind_cells(self) -> None:
        for pos in Position.range(self.width, self.height):
            for direction in Direction:
                p = pos.move(direction)
                if 0 <= p.x < self.width and 0 <= p.y < self.height:
                    self[pos].bind_neighbour(direction, self[p])
                    self[p].bind_neighbour(direction.opposite(), self[pos])

    def _generate_cells(self) -> None:
        self._cells = [Cell(pos)
                       for pos in Position.range(self.width, self.height)]
        self._bind_cells()
        ft = ["O...OOO",
              "O.....O",
              "OOO.OOO",
              "..O.O..",
              "..O.OOO"]
        ft_size = Position(len(ft[0]), len(ft))
        if self.width >= ft_size.x + 2 and self.height >= ft_size.y + 2:
            begin = (Position(self.width, self.height) - ft_size) / 2
            for pos in Position.range(ft_size.x, ft_size.y):
                dest = begin + pos
                if dest == self.entry or dest == self.exit:
                    for pos2 in Position.range(ft_size.x, ft_size.y):
                        self[begin + pos2].locked = False
                    return
                if ft[pos.y][pos.x] == 'O':
                    self[dest].locked = True

    def _random_cell(self) -> Cell:
        while True:
            cell = self[Position.random(self.width - 1, self.height - 1)]
            if cell.locked is False:
                return cell

    def _open_random_walls(self, callback: Optional[Callback] = None) -> None:
        def check_square(cell: Cell) -> bool:
            for delta in Position.range(5, 5):
                valid = False
                for it in Position.range(3, 3):
                    pos = cell.pos - Position(3, 3) + delta + it
                    if (not (0 <= pos.x < self.width and
                             0 <= pos.y < self.height) or
                            it.x < 2 and self[pos].is_closed(Direction.EAST) or
                            it.y < 2 and self[pos].is_closed(Direction.SOUTH)):
                        valid = True
                        break
                if valid is False:
                    return True
            return False

        if self.perfect is False:
            for _ in range(self.width * self.height // 4):
                cell = self._random_cell()
                if cell.locked is False:
                    directions = cell.valid_directions(check_data=False)
                    if len(directions) > 0:
                        direction = choice(directions)
                        if cell.is_closed(direction):
                            cell.open(direction)
                            if callback:
                                callback(cell, direction)
                            if check_square(cell):
                                cell.close(direction)
                                if callback:
                                    callback(cell, direction)

    def _find_path(self) -> None:
        for cell in self._cells:
            cell.data = 0
        self[self.exit].data = 1
        self._path = []
        currents: List[Cell] = [self[self.exit]]
        n = 2
        while len(currents) > 0:
            nexts: List[Cell] = []
            for cell in currents:
                for direction in Direction:
                    if cell.is_open(direction):
                        neighbour = cell.neighbour(direction)
                        if neighbour.data == 0:
                            neighbour.data = n
                            nexts.append(neighbour)
                        if neighbour.pos == self.entry:
                            cell = neighbour
                            while cell.pos != self.exit:
                                for direction in Direction:
                                    if cell.is_open(direction):
                                        neighbour = cell.neighbour(direction)
                                        if neighbour.data == cell.data - 1:
                                            self._path.append(direction)
                                            cell = neighbour
                                            break
                            return
            currents = nexts
            n += 1
        raise MazeGenerator.PathError("no valid path found")

    def _aldous_broder(self, callback: Optional[Callback] = None) -> None:
        n = 0
        for cell in self._cells:
            n += cell.locked is False
        cell = self._random_cell()
        while n != 0:
            if cell.data == 0:
                cell.data = 1
                n -= 1
            if n != 0:
                direction = choice(cell.valid_directions(check_data=False))
                other = cell.neighbour(direction)
                if other.data == 0:
                    cell.open(direction)
                    if callback:
                        callback(cell, direction)
                cell = other

    def _deep_first_search(self, callback: Optional[Callback] = None) -> None:
        stack: List[Cell] = [self._random_cell()]
        while len(stack) != 0:
            cell = stack.pop()
            cell.data = 1
            directions = cell.valid_directions()
            if len(directions) > 0:
                stack.append(cell)
                direction = choice(directions)
                stack.append(cell.open(direction))
                if callback:
                    callback(cell, direction)

    def _kruskal(self, callback: Optional[Callback] = None) -> None:
        walls: List[Tuple[Cell, Direction]] = []
        for cell in self._cells:
            cell.data = self.width * cell.pos.y + cell.pos.x
            if cell.locked is False:
                walls += list(map(lambda d: (cell, d), cell.valid_directions(
                    (Direction.WEST, Direction.SOUTH), False)))
        shuffle(walls)
        for wall in walls:
            id = wall[0].neighbour(wall[1]).data
            if wall[0].data != id:
                for cell in self._cells:
                    if cell.data == id:
                        cell.data = wall[0].data
                wall[0].open(wall[1])
                if callback:
                    callback(*wall)

    def _prim(self, callback: Optional[Callback] = None) -> None:
        cell = self._random_cell()
        walls = list(map(lambda d: (cell, d), cell.valid_directions()))
        while len(walls) != 0:
            wall = walls.pop(randint(0, len(walls) - 1))
            cell = wall[0].neighbour(wall[1])
            if cell.data == 0:
                cell.data = 1
                walls += list(map(lambda d: (cell, d),
                                  cell.valid_directions()))
                wall[0].open(wall[1])
                if callback:
                    callback(*wall)

    def _wilson(self, callback: Optional[Callback] = None) -> None:
        n = -1
        for cell in self._cells:
            n += cell.locked is False
        self._random_cell().data = 1
        while n != 0:
            i = randint(1, n)
            for cell in self._cells:
                if cell.locked is False and cell.data == 0:
                    i -= 1
                    if i == 0:
                        break
            path: List[Cell] = []
            while cell.data != 1:
                if cell in path:
                    while path[-1] != cell:
                        other = path.pop()
                        if len(path) > 0:
                            direction = path[-1].pos.diff(other.pos)
                            path[-1].close(direction)
                            if callback:
                                callback(path[-1], direction)
                else:
                    if len(path) > 0:
                        direction = path[-1].pos.diff(cell.pos)
                        path[-1].open(direction)
                        if callback:
                            callback(path[-1], direction)
                    path.append(cell)
                cell = cell.neighbour(choice(cell.valid_directions(
                    check_data=False)))
            direction = path[-1].pos.diff(cell.pos)
            path[-1].open(direction)
            if callback:
                callback(path[-1], direction)
            for cell in path:
                cell.data = 1
            n -= len(path)

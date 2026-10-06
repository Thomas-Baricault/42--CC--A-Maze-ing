from __future__ import annotations
from random import randint
from typing import Generator, Tuple
from .Direction import Direction


class Position:
    """Representation of a 2D position

    Attributes
    ----------
    x : int
        The x coordinate
    y : int
        The y coordinate

    Static Methods
    --------------
    random(xmax, ymax) -> Position
        Returns a random position
    range(xmax, ymax) -> Generator[Position, None, None]
        Generator for a range of positions

    Methods
    -------
    move(direction, n=1) -> Position
        Move the position along a cardinal direction and return the resulting
        position
    diff(other) -> Direction
        Return the cardinal direction differencing two positions
    """

    @staticmethod
    def random(xmax: int, ymax: int) -> Position:
        """Returns a random position

        Parameters
        ----------
        xmax : int
            The maximum value of the x coordinate
        ymax : int
            The maximum value of the y coordinate

        Returns
        -------
        Position
            The generated random position
        """

        return Position(randint(0, xmax),
                        randint(0, ymax))

    @staticmethod
    def range(xmax: int, ymax: int) -> Generator[Position, None, None]:
        """Generator for a range of positions

        Parameters
        ----------
        xmax : int
            The maximum value of the x coordinate
        ymax : int
            The maximum value of the y coordinate

        Yields
        ------
        Position
            A position
        """

        for y in range(ymax):
            for x in range(xmax):
                yield Position(x, y)

    def __init__(self, x: int | str | Tuple[int, int] | Position = 0,
                 y: int = 0) -> None:
        """
        Parameters
        ----------
        x : int | str | Tuple[int, int] | Position
            The x coordinate (0 by default), or the coordinates to parse in
            format 'x,y' if is a str, or a tuple of int representing the
            coordinates, or an another Position to copy
        y : int
            The y coordinate (0 by default), don't used if x is a str

        Raises
        ------
        ValueError
            If x is str and cannot be parsed
        """

        if isinstance(x, str):
            parts = x.split(',')
            if len(parts) != 2:
                raise ValueError(f"invalid position '{x}'")
            x = int(parts[0])
            y = int(parts[1])
        elif isinstance(x, tuple):
            y = x[1]
            x = x[0]
        elif isinstance(x, Position):
            y = x.y
            x = x.x
        self.x = x
        self.y = y

    def __str__(self) -> str:
        """Returns the string representation of the position

        Returns
        -------
        str
            The string in format 'x,y'
        """

        return f"{self.x},{self.y}"

    def __getitem__(self, index: int) -> int:
        """Returns the value of a coordinate associated with an index

        Parameters
        ----------
        index : int
            0 for x coordinate, 1 for y

        Returns
        -------
        int
            The coordinate value

        Raises
        ------
        ValueError
            If index is invalid
        """

        if index == 0:
            return self._x
        if index == 1:
            return self._y
        raise ValueError(f"invalid index '{index}'")

    def __eq__(self, other: object) -> bool:
        """Test if two positions are equal

        Parameters
        ----------
        other : object
            The other position

        Returns
        -------
        bool
            True if the two positions are equal, False otherwise
        """

        if isinstance(other, Position):
            return self.x == other.x and self.y == other.y
        return False

    def __add__(self, other: Position) -> Position:
        """Returns the addition of two positions

        Parameters
        ----------
        other : Position
            The position to add

        Returns
        -------
        Position
            The addition result
        """

        return Position(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Position) -> Position:
        """Returns the subtraction of two positions

        Parameters
        ----------
        other : Position
            The position to subtract

        Returns
        -------
        Position
            The subtraction result
        """

        return Position(self.x - other.x, self.y - other.y)

    def __mul__(self, other: int | float) -> Position:
        """Multiply a position

        Parameters
        ----------
        other : int | float
            The number used to multiply

        Returns
        -------
        Position
            The multiplication result
        """

        return Position(int(self.x * other), int(self.y * other))

    def __truediv__(self, other: int | float) -> Position:
        """Divide a position

        Parameters
        ----------
        other : int | float
            The number used to divide

        Returns
        -------
        Position
            The division result
        """

        return Position(int(self.x / other), int(self.y / other))

    @property
    def x(self) -> int:
        """The x coordinate

        Returns
        -------
        int
            The x coordinate
        """

        return self._x

    @x.setter
    def x(self, value: int) -> None:
        """Set the x coordinate

        Parameters
        ----------
        value : int
            The value
        """

        self._x = int(value)

    @property
    def y(self) -> int:
        """The y coordinate

        Returns
        -------
        int
            The y coordinate
        """

        return self._y

    @y.setter
    def y(self, value: int) -> None:
        """Set the y coordinate

        Parameters
        ----------
        value : int
            The value
        """

        self._y = int(value)

    def move(self, direction: Direction, n: int = 1) -> Position:
        """Move the position along a cardinal direction and return the
        resulting position

        Parameters
        ----------
        direction : Direction
            The direction to follow
        n : int
            The number of steps to do (1 by default)

        Returns
        -------
        Position
            The resulting position
        """

        if direction == Direction.NORTH:
            return Position(self.x, self.y - n)
        if direction == Direction.EAST:
            return Position(self.x + n, self.y)
        if direction == Direction.SOUTH:
            return Position(self.x, self.y + n)
        if direction == Direction.WEST:
            return Position(self.x - n, self.y)

    def diff(self, other: Position) -> Direction:
        """Return the cardinal direction differencing two positions (the two
        positions need to be neighbours)

        Parameters
        ----------
        other : Position
            The other position

        Returns
        -------
        Direction
            The direction differencing the two positions

        Raises
        ------
        ValueError
            If the two positions aren't neighbours
        """

        if self.x == other.x:
            if self.y - 1 == other.y:
                return Direction.NORTH
            if self.y + 1 == other.y:
                return Direction.SOUTH
        if self.y == other.y:
            if self.x - 1 == other.x:
                return Direction.WEST
            if self.x + 1 == other.x:
                return Direction.EAST
        raise ValueError(f"position {self} and position {other} aren't"
                         + " neighbours")

from __future__ import annotations
from typing import Dict, Iterable, List
from .Direction import Direction
from .Position import Position


class Cell:
    """Representation of a maze cell

    Attributes
    ----------
    pos : Position
        The position of the cell
    locked : bool
        If the cell is locked and belongs to a drawing pattern
    value : str
        The cell hexadecimal value
    data : int
        An additional data attribute used by generation algorithms

    Methods
    -------
    is_open(direction) -> bool
        Returns if a wall of the cell is opened
    is_closed(direction) -> bool
        Returns if a wall of the cell is closed
    neighbour(direction) -> Cell
        Returns a neighbour of the cell
    valid_directions(set = Direction, check_data = True) -> List[Direction]
        Returns the cell walls directions that can be opened
    open(direction) -> Cell
        Open the wall in a direction
    close(direction) -> Cell
        Close the wall in a direction
    bind_neighbour(direction, neighbour) -> None
        Bind a neighbouring cell to a direction
    """

    _SET = "0123456789ABCDEF"

    def __init__(self, pos: Position) -> None:
        """
        Parameters
        ----------
        pos : Position
            The cell position
        """

        self._pos = Position(pos)
        self.locked = False
        self.value = 'F'
        self.data = 0
        self._neighbours: Dict[Direction, Cell | None] = {
            Direction.NORTH: None,
            Direction.EAST: None,
            Direction.SOUTH: None,
            Direction.WEST: None
        }

    def __str__(self) -> str:
        return self.value

    @property
    def pos(self) -> Position:
        """The position of the cell

        Returns
        -------
        Position
            The position
        """

        return Position(self._pos)

    @property
    def locked(self) -> bool:
        """If the cell is locked and belongs to a drawing pattern

        Returns
        -------
        bool
            True if locked, False otherwise
        """

        return self._locked

    @locked.setter
    def locked(self, value: bool) -> None:
        """Set if the cell is locked and belongs to a drawing pattern

        Parameters
        ----------
        value : bool
            True if locked, False otherwise
        """

        self._locked = value

    @property
    def value(self) -> str:
        """The cell hexadecimal value

        Returns
        -------
        str
            An hexadecimal character representing the cell value
        """

        return self._SET[self.is_closed(Direction.NORTH) +
                         (self.is_closed(Direction.EAST) << 1) +
                         (self.is_closed(Direction.SOUTH) << 2) +
                         (self.is_closed(Direction.WEST) << 3)]

    @value.setter
    def value(self, value: str) -> None:
        """Set the cell hexadecimal value

        Parameters
        ----------
        value : str
            An hexadecimak character

        Raises
        ------
        ValueError
            If the given character isn't an uppercase hexadecimal character
        """

        if len(value) != 1 and value not in self._SET:
            raise ValueError(f"Invalid value '{value}'")
        index = self._SET.index(value)
        self._walls: Dict[Direction, bool] = {
            Direction.NORTH: (index & 1) > 0,
            Direction.EAST: (index & (1 << 1)) > 0,
            Direction.SOUTH: (index & (1 << 2)) > 0,
            Direction.WEST: (index & (1 << 3)) > 0
        }

    @property
    def data(self) -> int:
        """An additional data attribute used by generation algorithms

        Returns
        -------
        int
            The data
        """

        return self._data

    @data.setter
    def data(self, value: int) -> None:
        """Set the additional data attribute

        Parameters
        ----------
        value : int
            The value
        """

        self._data = value

    def is_open(self, direction: Direction) -> bool:
        """Returns if a wall of the cell is opened

        Parameters
        ----------
        direction : Direction
            The direction of the wall

        Returns
        -------
        bool
            If the wall is opened
        """

        return self._walls[direction] is False

    def is_closed(self, direction: Direction) -> bool:
        """Returns if a wall of the cell is closed

        Parameters
        ----------
        direction : Direction
            The direction of the wall

        Returns
        -------
        bool
            If the wall is closed
        """

        return self._walls[direction]

    def has_neighbour(self, direction: Direction) -> bool:
        """Returns if the cell have a neighbour in a given direction

        Parameters
        ----------
        direction : Direction
            The direction to check

        Returns
        -------
        bool
            True if there is a neighbour, False otherwise
        """

        return self._neighbours[direction] is not None

    def neighbour(self, direction: Direction) -> Cell:
        """Returns a neighbour of the cell

        Parameters
        ----------
        direction : Direction
            The direction of the neighbour

        Returns
        -------
        Cell
            The neighbouring cell

        Raises
        ------
        ValueError
            If the cell has no neighbour in this direction
        """

        neighbour = self._neighbours[direction]
        if neighbour is None:
            raise ValueError(f"Cell at position {self.pos} as no neighbour in"
                             + f" the {direction.name} direction")
        return neighbour

    def valid_directions(self, set: Iterable[Direction] = Direction,
                         check_data: bool = True) -> List[Direction]:
        """Returns the cell walls directions that can be opened

        Parameters
        ----------
        set : Iterable[Direction]
            The directions to check (default is all)
        check_data : bool
            If cells data must be validated (default is True), if this option
            is enable, a cell is only accessible if its data attribute is equal
            to 0

        Returns
        -------
        List[Direction]
            All the valid directions
        """

        valids: List[Direction] = []
        for direction in set:
            neighbour = self._neighbours[direction]
            if neighbour and neighbour.locked is False and (
                    check_data is False or neighbour.data == 0):
                valids.append(direction)
        return valids

    def open(self, direction: Direction) -> Cell:
        """Open the wall in a direction

        Parameters
        ----------
        direction : Direction
            The direction of the wall to open

        Returns
        -------
        Cell
            The neighbouring cell behind the wall

        Raises
        ------
        ValueError
            If the cell has no neighbour in this direction
        """

        neighbour = self._neighbours[direction]
        if neighbour is None:
            raise ValueError(f"Cell at position {self.pos} as no neighbour in"
                             + f" the {direction.name} direction")
        self._walls[direction] = False
        neighbour._walls[direction.opposite()] = False
        return neighbour

    def close(self, direction: Direction) -> Cell:
        """Close the wall in a direction

        Parameters
        ----------
        direction : Direction
            The direction of the wall to close

        Returns
        -------
        Cell
            The neighbouring cell behind the wall

        Raises
        ------
        ValueError
            If the cell has no neighbour in this direction
        """

        neighbour = self._neighbours[direction]
        if neighbour is None:
            raise ValueError(f"Cell at position {self.pos} as no neighbour in"
                             + f" the {direction.name} direction")
        self._walls[direction] = True
        neighbour._walls[direction.opposite()] = True
        return neighbour

    def bind_neighbour(self, direction: Direction, neighbour: Cell) -> None:
        """Bind a neighbouring cell to a direction

        Parameters
        ----------
        direction : Direction
            The direction of the neighbour
        neighbour : Cell
            The neighbouring cell
        """

        self._neighbours[direction] = neighbour

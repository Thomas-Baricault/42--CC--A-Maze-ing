from __future__ import annotations
from enum import Enum


class Direction(Enum):
    """Enum that represent cardinal directions

    Values
    ------
    NORTH : "N"
        North direction
    EAST : "E"
        East direction
    SOUTH : "S"
        South direction
    WEST : "W"
        West direction

    Methods
    -------
    opposite() -> Direction
        Returns the opposite direction
    """

    NORTH = "N"
    EAST = "E"
    SOUTH = "S"
    WEST = "W"

    def __str__(self) -> str:
        """Returns the string representation of the direction

        Returns
        -------
        str
            The string
        """

        return self.value

    def opposite(self) -> Direction:
        """Returns the opposite direction

        Returns
        -------
        Direction
            The opposite direction
        """

        if self == Direction.NORTH:
            return Direction.SOUTH
        if self == Direction.EAST:
            return Direction.WEST
        if self == Direction.SOUTH:
            return Direction.NORTH
        if self == Direction.WEST:
            return Direction.EAST

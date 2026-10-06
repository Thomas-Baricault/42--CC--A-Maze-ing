"""A maze generator module

Examples
--------
>>> from mazegen import MazeGenerator
>>> #
>>> # Create the maze generator
>>> #
>>> generator = MazeGenerator(
        width=10,
        height=10,
        entry=(0, 0),
        exit=(9, 9),
        perfect=True
    )
>>> #
>>> # Generate the maze
>>> #
>>> generator.generate()
>>> #
>>> # Save the maze
>>> #
>>> generator.save("maze.txt")
>>> #
>>> # Accessing maze cell
>>> #
>>> generator[(0, 0)]
<mazegen.Cell.Cell object at 0x00000222c532ac80>
>>> #
>>> # Accessing maze informations
>>> #
>>> generator.seed
1768303330767
>>> generator.path
[<Direction.EAST: 'E'>, <Direction.EAST: 'E'>, <Direction.EAST: 'E'>,
<Direction.EAST: 'E'>, <Direction.SOUTH: 'S'>, <Direction.EAST: 'E'>,
<Direction.NORTH: 'N'>, <Direction.EAST: 'E'>, <Direction.SOUTH: 'S'>,
<Direction.EAST: 'E'>, <Direction.EAST: 'E'>, <Direction.SOUTH: 'S'>,
<Direction.EAST: 'E'>, <Direction.SOUTH: 'S'>, <Direction.SOUTH: 'S'>,
<Direction.WEST: 'W'>, <Direction.SOUTH: 'S'>, <Direction.SOUTH: 'S'>,
<Direction.EAST: 'E'>, <Direction.SOUTH: 'S'>, <Direction.SOUTH: 'S'>,
<Direction.SOUTH: 'S'>]
"""

__version__ = "1.0.0"
__authors__ = ["adfernan", "tbaricau"]
__all__ = [
    "Algorithm",
    "Cell",
    "Config",
    "Direction",
    "MazeGenerator",
    "Position",
    "Renderer",
]

from .Algorithm import Algorithm
from .Cell import Cell
from .Config import Config
from .Direction import Direction
from .MazeGenerator import MazeGenerator
from .Position import Position
from .Renderer import Renderer

from enum import Enum
from random import choice
from sys import stdin, stdout
from .Config import Config
from .Direction import Direction
from .MazeGenerator import MazeGenerator
from .Position import Position


class Renderer:
    """Base class for renderers"""

    class GridElement(Enum):
        """Enum that represent all types of cells that can appear in the render
        grid

        Values
        ------
        NONE : 0
            Not a part of the maze
        CORRIDOR : 1
            Part of a maze corridor
        WALL : 2
            Part of a maze wall
        LOCKED : 3
            Part of a maze locked pattern
        ENTRY : 4
            Part of the maze entry
        EXIT : 5
            Part of the maze exit
        PATH : 6
            Part of the maze path between entry and exit
        """

        NONE = 0
        CORRIDOR = 1
        WALL = 2
        LOCKED = 3
        ENTRY = 4
        EXIT = 5
        PATH = 6

    def __init__(self, config: Config, generator: MazeGenerator) -> None:
        """
        Parameters
        ----------
        config : Config
            The config to use
        generator : MazeGenerator
            The generator
        """

        self._config = config
        self._generator = generator
        self._show_path = True
        self._interrupted = False
        self._colors = {
            Renderer.GridElement.NONE: 0,
            Renderer.GridElement.CORRIDOR: 8,
            Renderer.GridElement.WALL: 15,
            Renderer.GridElement.LOCKED: 2,
            Renderer.GridElement.ENTRY: 13,
            Renderer.GridElement.EXIT: 9,
            Renderer.GridElement.PATH: 4
        }
        self._generate()

    def _generate(self) -> None:
        self._clear()
        try:
            self._generator.generate(
                self._config.seed,
                lambda c, d: self._update_wall(
                    c.pos, d, (Renderer.GridElement.CORRIDOR if c.is_open(d)
                               else Renderer.GridElement.WALL)
                )
            )
            pos = self._generator.entry
            for direction in self._generator.path:
                self._update_wall(pos, direction, Renderer.GridElement.PATH,
                                  self._show_path)
                pos = pos.move(direction)
            self._generator.save(self._config.output_file)
            if self._config.seed:
                self._config.seed = None
            self._show_choice()
        except KeyboardInterrupt as e:
            self._interrupted = True
            raise e

    def _show_hide_path(self) -> None:
        self._show_path = not self._show_path
        self._update()
        self._show_choice()

    def _rotate_maze_colors(self) -> None:
        colors = list(range(0, 16))
        colors.remove(0)
        colors.remove(7)
        for color in self._colors.values():
            if color in colors:
                colors.remove(color)
        self._colors[Renderer.GridElement.WALL] = choice(colors)
        self._update()
        self._show_choice()

    def _clear(self) -> None:
        self._grid = [[Renderer.GridElement.WALL
                       for _ in range(self._generator.width * 3 + 1)]
                      for _ in range(self._generator.height * 3 + 1)]
        if len(self._grid) % 2 == 1:
            self._grid.append([Renderer.GridElement.NONE
                               for _ in range(len(self._grid[0]))])
        for pos in Position.range(self._generator.width,
                                  self._generator.height):
            if self._generator[pos].locked:
                self._update_cell(pos, Renderer.GridElement.LOCKED)
        self._update_cell(self._generator.entry, Renderer.GridElement.ENTRY)
        self._update_cell(self._generator.exit, Renderer.GridElement.EXIT)
        stdout.write("\033[2J")

    def _update(self) -> None:
        def to_ansi(element: Renderer.GridElement, is_bg: bool) -> str:
            if (self._show_path is False and
                    element == Renderer.GridElement.PATH):
                element = Renderer.GridElement.CORRIDOR
            c = self._colors[element]
            return f"\033[{30 + 60 * (c // 8 == 1) + c % 8 + 10 * is_bg}m"

        s = "\033[?25L\033[H"
        for y in range(0, len(self._grid), 2):
            for x in range(len(self._grid[0])):
                fg = to_ansi(self._grid[y][x], False)
                bg = to_ansi(self._grid[y + 1][x], True)
                s += f"{fg}{bg}▀"
            s += "\033[0m\n"
        if self._interrupted is False:
            stdout.write(f"{s}\n\033[?25h")

    def _show_choice(self) -> None:
        if self._interrupted is False:
            stdout.write("=== A-Maze-ing ===\n")
            stdout.write("1. Re-generate a new maze\n")
            stdout.write("2. Show/Hide path from entry to exit\n")
            stdout.write("3. Rotate maze colors\n")
            stdout.write("4. Quit\n")
            choised = False
            while not choised:
                choised = True
                stdout.write("\r\033[KChoice? (1-4): ")
                stdout.flush()
                c = stdin.read(1)
                if c == '1':
                    self._generate()
                elif c == '2':
                    self._show_hide_path()
                elif c == '3':
                    self._rotate_maze_colors()
                elif c == '4':
                    break
                else:
                    choised = False

    def _update_cell(self, pos: Position, type: GridElement) -> None:
        pos = pos * 3 + Position(1, 1)
        if self._grid[pos.y][pos.x] in (Renderer.GridElement.ENTRY,
                                        Renderer.GridElement.EXIT):
            return
        for delta in Position.range(2, 2):
            p = pos + delta
            self._grid[p.y][p.x] = type

    def _update_corner(self, pos: Position) -> None:
        if (pos.x > 0 and
            self._grid[pos.y][pos.x - 1] == Renderer.GridElement.WALL or
            pos.x < len(self._grid[0]) - 1 and
            self._grid[pos.y][pos.x + 1] == Renderer.GridElement.WALL or
            pos.y > 0 and
            self._grid[pos.y - 1][pos.x] == Renderer.GridElement.WALL or
            pos.y < len(self._grid) - 1 and
                self._grid[pos.y + 1][pos.x] == Renderer.GridElement.WALL):
            self._grid[pos.y][pos.x] = Renderer.GridElement.WALL
        else:
            self._grid[pos.y][pos.x] = Renderer.GridElement.CORRIDOR

    def _update_wall(self, pos: Position, direction: Direction,
                     type: GridElement, update: bool = True) -> None:
        p = pos * 3
        vertical = direction in (Direction.NORTH, Direction.SOUTH)
        if vertical:
            p.x += 1
        else:
            p.y += 1
        if direction == Direction.SOUTH:
            p.y += 3
        elif direction == Direction.EAST:
            p.x += 3
        self._grid[p.y][p.x] = type
        self._grid[p.y + (not vertical)][p.x + vertical] = type
        if vertical:
            self._update_corner(p - Position(1, 0))
            self._update_corner(p + Position(2, 0))
        else:
            self._update_corner(p - Position(0, 1))
            self._update_corner(p + Position(0, 2))
        self._update_cell(pos, type)
        self._update_cell(pos.move(direction), type)
        if update:
            self._update()

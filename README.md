*This project has been created as part of the 42 curriculum by adfernan, tbaricau*

# A-Maze-ing

## Description

The goal of this project is to make a Python module to generate random mazes.

It allow to create a variety of mazes using different algorithm and configurations, and render them in the console.
It also compute the shortest path between the entry and exit of the maze.

## Features

- Maze generation
- Configuration file
- Multiple supported algorithms
- Shortest path computation
- ASCII rendering

## Instructions

Install all the dependencies
```Shell
make install
```

Run using the default configuration file
```Shell
make run
```

Run using a custom configuration file
```Shell
python3 a_maze_ing.py <your_config_file>
```

Run in debug mode
```Shell
make debug
```

Clean cached files
```Shell
make clean
```

Check the norm and the typing
```Shell
make lint
make lint-strict
```

Build and install the module
```Shell
make build
make mazegen-install
```

Uninstall the module
```Shell
make mazegen-uninstall
```

## Config file

config.txt
```Env
# The width of the maze
WIDTH=20

# The height of the maze
HEIGHT=15

# The entry position of the maze
ENTRY=0,0

# The exit position of the maze
EXIT=19,14

# The maze output file
OUTPUT_FILE=maze.txt

# If the maze is perfect (means only one path between entry and exit)
PERFECT=True

# (Optional) The seed of the maze
SEED=123456789

# (Optional) The algorithm used
ALGORITHM=DEEP_FIRST_SEARCH
```

## Reusability

If you want to reuse the code to generate mazes in your projects you have to build and install it.
After that, you can import mazegen in your code and do wathever you want, for example:

```Python
from mazegen import MazeGenerator

if __name__ == "__main__":
    # Create the maze generator
    generator = MazeGenerator(
        width=10,
        height=10,
        entry=(0, 0),
        exit=(9, 9),
        perfect=True
    )

    # Generate the maze
    generator.generate()

    # Save the maze
    generator.save("maze.txt")

    # Accessing maze cell
    print(generator[(0, 0)])

    # Accessing maze informations
    print("SEED:", generator.seed)
    print("PATH:", generator.path)

```

## Resources

Maze algorithms and how it works:

<https://en.wikipedia.org/wiki/Maze_generation_algorithm>

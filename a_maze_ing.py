from sys import argv, exit, stderr
from mazegen import Config, MazeGenerator, Renderer

if __name__ == "__main__":
    if len(argv) != 2:
        print("Usage: python a_maze_ing.py <config_file>")
        exit(1)
    try:
        config = Config.open(argv[1])
        generator = MazeGenerator(
            config.width,
            config.height,
            config.entry,
            config.exit,
            config.perfect,
            config.algorithm
        )
        Renderer(config, generator)
    except (Config.ConfigError, MazeGenerator.MazeError) as e:
        stderr.write(f"{e}\n")
        exit(1)
    except KeyboardInterrupt:
        stderr.write("Interrupted\n")
        exit(1)

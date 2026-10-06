from enum import Enum


class Algorithm(Enum):
    """Enum that represent algorithms

    Values
    ------
    ALDOUS_BRODER : "ALDOUS_BRODER"
        - Pick a random cell as the current cell and mark it as visited
        - While there are unvisited cells
            - Pick a random neighbour
            - If the chosen neighbour has not been visited
                - Remove the wall between the current cell and the chosen
                  neighbour
                - Mark the chosen neighbour as visited
            - Make the chosen neighbour the current cell
        (Please note that due to random movements, this could be very slow)
    DEEP_FIRST_SEARCH : "DEEP_FIRST_SEARCH"
        - Choose the initial cell, mark it as visited and push it to the stack
        - While the stack is not empty
            - Pop a cell from the stack and make it a current cell
            - If the current cell has any neighbours which have not been
              visited
                - Push the current cell to the stack
                - Choose one of the unvisited neighbours
                - Remove the wall between the current cell and the chosen cell
                - Mark the chosen cell as visited and push it to the stack
    KRUSKAL : "KRUSKAL"
        - Create a list of all walls, and create a set for each cell, each
          containing just that one cell
        - For each wall, in some random order
            - If the cells divided by this wall belong to distinct sets
                - Remove the current wall
                - Join the sets of the formerly divided cells
    PRIM : "PRIM"
        - Start with a grid full of walls
        - Pick a cell, mark it as part of the maze. Add the walls of the cell
          to the wall list
        - While there are walls in the list
            - Pick a random wall from the list
            - If only one of the cells that the wall divides is visited, then
                - Make the wall a passage and mark the unvisited cell as part
                  of the maze
                - Add the neighboring walls of the cell to the wall list
            - Remove the wall from the list
    WILSON : "WILSON"
        - Make a random cell as visited
        - While there are unvisited cells
            - Choose a random cell and make it the current cell
            - Initialize a path with the actual cell
            - While the current cell isn't visited
                - Choose a random neighbour
                - If the neighbour is already in path
                    - Remove the loop and continue
                - Add the neighbour to the path
            - Remove all walls of the paths and mark the cells as visited
        (Please note that due to random movements, this could be very slow)
    DEFAULT : DEEP_FIRST_SEARCH
        The default algorithm used
    """

    ALDOUS_BRODER = "ALDOUS_BRODER"
    DEEP_FIRST_SEARCH = "DEEP_FIRST_SEARCH"
    KRUSKAL = "KRUSKAL"
    PRIM = "PRIM"
    WILSON = "WILSON"
    DEFAULT = DEEP_FIRST_SEARCH

    def __str__(self) -> str:
        """Returns the string representation of the algorithm

        Returns
        -------
        str
            The string
        """

        return self.value

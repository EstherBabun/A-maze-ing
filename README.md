*This project has been created as part of the 42 curriculum by mmeurer, ebabun*

# Description : A-maze-ing
Create your own maze generator and display its result!

# Instructions

# Technical choices and organisation
We first defined the main classes of the project determined on the subject: **Cell and MazeGenerator**.
We then implemented a parsing system and various algorithms, allowing each of us to work on a separate algorithm and finally a maze-solving process. 
We frequently exchanged ideas about the different parts we were developing and kept each other well-informed about our progress.

## Parsing - Esther


## Algorithms - Both
### DFS Algorithm - Implemented by Esther
### Wilson's Algorithm - Implemented by Morgane
[Wilson’s algorithm](https://medium.com/@batbat.senturk/the-ultimate-unbiased-maze-generation-technique-you-need-to-see-46123d5fec76) was chosen for its elegant approach to maze generation and the quality of the resulting mazes. (The gif of this page got me)
How it works:
1. Select an initial cell and mark it as part of the maze.
2. Choose a random unvisited cell and perform a random walk until it reaches a cell that is already part of the maze, removing any loops formed during the walk.
3. Add the resulting path to the maze.
4. Repeat the process 2 and 3 until all cells are included in the maze.

## Resolution of the maze - Morgane
### Breadth-First Search (BFS) — Maze Solving Algorithm
Breadth-First Search (BFS) was chosen for its simplicity and its ability to guarantee the shortest path in an unweighted maze.
How it works:
- The algorithm starts from the entry cell and add it to a queue. A **deque** is used because it allows efficient removal of the first element.
- All unvisited neighboring cells are explored level by level, using a first-in, first-out (FIFO) queue.
- Each visited cell is stored in a dictionary to keep track of his previous cell (its parent).
- The algorithm stops when the exit cell is reached or when all reachable cells have been explored.
- The shortest path is then reconstructed by backtracking from the target cell to the start cell.

# RESOURCES

Article on Wilson's algo: https://medium.com/@batbat.senturk/the-ultimate-unbiased-maze-generation-technique-you-need-to-see-46123d5fec76
Page on github for maze generating and solving: https://github.com/batuSenturk/Mazes

keyboard key: https://www.cl.cam.ac.uk/~mgk25/ucs/keysymdef.h

Makefile : 
make install      # crée le venv + installe les dépendances
make run          # lance le programme
make debug        # lance avec pdb
make lint         # lint obligatoire
make lint-strict  # lint strict (optionnel)
make clean        # nettoyage
make play		  # test affichage

Braiding algorithm :
- Generate perfect maze
- search dead ends (3 walls)
- Randomly knock down a wall at the back of a percentage of these dead ends
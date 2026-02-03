*This project has been created as part of the 42 curriculum by mmeurer, ebabun.*

# A-maze-ing : Description
**A-maze-ing** is a maze generator and solver project.  
The goal is to generate mazes using different algorithms and display them either in ASCII or using a graphical interface.


# Features
- Automatic fallback to default values for missing or invalid parameters.
- Maze generation using:
  - Depth-First Search (DFS)
  - Wilson’s algorithm
- Maze solving using Breadth-First Search (BFS)
- Two rendering modes:
  - ASCII display
  - MinilibX graphical display


# Instructions
#### 1. Create and activate a virtual environment
```bash
python3.12 -m venv venv
source venv/bin/activate
```
#### 2. Install dependencies
```bash
make install
```
#### 3. Configure the maze
Edit the ```config.txt``` file to define the desired parameters.
If a value is missing or invalid, a default value will be used automatically.

#### 4. Run the program
```bash
make run
```
or 
```bash
./a_maze_ing.py config.txt
```
or 
```bash
python3 a_maze_ing.py config.txt
```


# Technical choices and organization
**A revoir !**
We first defined the main core classes of the project according to the subject: **Cell** and **MazeGenerator**.

We then implemented:
- a parsing system,
- several generation algorithms,
- and a maze solving process.

This organization allowed each team member to work on a separate algorithm while keeping a consistent structure.  
We frequently exchanged ideas and kept each other informed about our progress.


## Parsing — Esther
**- mettre les valeurs par défauts proposées.**


## Algorithms — Both

### DFS Algorithm — Implemented by Esther


### Wilson’s Algorithm — Implemented by Morgane
[Wilson’s algorithm](https://medium.com/@batbat.senturk/the-ultimate-unbiased-maze-generation-technique-you-need-to-see-46123d5fec76) was chosen for its elegant approach and the high quality of the generated mazes (also… the gif convinced us).
![Maze's algo](https://miro.medium.com/v2/resize:fit:640/format:webp/1*Ewed2CKIK6oLAKDfo21DFg.gif)

**How it works:**
1. Select an initial cell and mark it as part of the maze.
2. Choose a random unvisited cell and perform a random walk until it reaches a visited cell, removing loops during the walk.
3. Add the resulting path to the maze.
4. Repeat until all cells are included.

## Maze Resolution — Morgane

### Breadth-First Search (BFS)
BFS was chosen for its simplicity and its ability to guarantee the shortest path in an unweighted maze. Plus, several functions from the algorithms were reused, avoiding redundancy and simplifying the code.

**How it works:**
- Start from the entry cell and add it to a queue (implemented using a **deque** chosen for its efficient removal of the first element).
- Explore all unvisited neighbors level by level (FIFO).
- Store each visited cell’s parent in a dictionary.
- Stop when the exit is reached or when all reachable cells are explored.
- Reconstruct the shortest path by backtracking from the exit to the start.

## Rendering — Both

### ASCII Renderer — Implemented by Morgane
The maze can be rendered directly in the terminal using ASCII characters.

**Features:**
- Display walls, paths, entry (green square), exit (red square), and the solution path (optional) on a fresh screen.
- Supports multiple wall colors with [ANSI codes](https://talyian.github.io/ansicolors/).
- Interactive menu to:
  1. Re-generate a new maze
  2. Show or hide the solution path
  3. Rotate wall colors
  4. Quit the program

**How it works:**
1. The terminal is cleared and the cursor is placed at the top-left corner to give the impression that each new maze is displayed in a fresh window.
2. The maze is printed:
   - On the first iteration, the solution path is hidden and the walls are displayed in white by default.
   - Each cell is rendered according to its content:
     - Entry
     - Exit
     - Solution path (if enabled)
     - 42 block cells (`■`)
     - All other cells are left empty.
   - The maze is drawn line by line using the hexadecimal representation from the `MazeGenerator` class, with each cell’s content centered.
3. The user is prompted for input:
   - If an invalid choice is entered, a message is displayed and the prompt repeats until a valid choice is made.
   - Once a valid choice is entered, step 1 is repeated, updating the display accordingly.

[!NOTE] Each time a new maze is generated, the maze configuration and any error messages are displayed above the renderer. However, to provide a “fresh window” experience more pleasant, these messages are hidden in the main display. To view the configuration or error messages, the user can scroll up in the terminal during the first iteration of the new maze.


### MinilibX Renderer — Implemented by Esther


# Resources
- Wilson’s algorithm article:  
  https://medium.com/@batbat.senturk/the-ultimate-unbiased-maze-generation-technique-you-need-to-see-46123d5fec76

- Maze generation and solving reference:  
  https://github.com/batuSenturk/Mazes

- Keyboard keys reference:  
  https://www.cl.cam.ac.uk/~mgk25/ucs/keysymdef.h

- Terminal visual sequences:  
  https://learn.microsoft.com/fr-fr/windows/console/console-virtual-terminal-sequences

- ANSI color codes:
  https://talyian.github.io/ansicolors/

- Pytest Documentation:
  https://docs.pytest.org/en/stable/getting-started.html

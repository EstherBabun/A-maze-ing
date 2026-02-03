from maze_generator import MazeGenerator

def func(x):
    return x + 1


def test_answer():
    assert func(3) == 4

def test_maze_init_default():
    maze = MazeGenerator()

    assert maze.cols > 0
    assert maze.rows > 0
    assert maze.entry_cell is not None
    assert maze.exit_cell is not None
    assert maze.valid_cells > 0
    assert len(maze.unvisited) == 0
    # self.unvisited = tot
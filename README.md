# A-maze-ing
 Create your own maze generator and display its result!

# Usefull tools

- #### [mypy](#https://mypy.readthedocs.io/en/stable/) for static type checking
    flags to use : 
    - --warn-return-any 
    - --warn-unused-ignores 
    - --ignore-missing-imports
    - --disallow-untyped-defs 
    - --check-untyped-defs

- #### [PEP 257](#https://peps.python.org/pep-0257/) for docstring convention

- #### [flake8](#https://flake8.pycqa.org/en/latest/) for Style Enforcement

- #### [pytest](#https://docs.pytest.org/en/stable/) for unit testing
    Note: pytest is more intuitive than unittest
- #### [venv](#https://docs.python.org/3/library/venv.html) for virtual environments
    ```bash
    # Create venv in the project's root folder
    $ python3 -m venv /path/to/venv
    ```
    ```bash
    # Activate it 
    # under bash/zsh :
    $ source venv/bin/activate
    ```
    ```bash
    # install dependencies and tools
    (venv) $ install <your_py_tool>
    ```
    ```bash
    # When done working, deactivate
    (venv) $ deactivate
    ```

- #### [pdb](#https://docs.python.org/3/library/pdb.html) for python debugging

- #### [MiniLibX](#https://harm-smits.github.io/42docs/libs/minilibx) graphics library for visual rendering



# Theory
- Prim's, Kruskal's and the recursive backtracker algorithms for maze generation.
- Perfect mazes are related to spanning trees in graph theory.


# config.txt
example:
```
"WIDTH=20"
"HEIGHT=15"
"ENTRY=0,0"
"EXIT=19,14"
"OUTPUT_FILE=maze.txt"
"PERFECT=True"

Note: We may add additional keys (e.g., seed, algorithm, display mode) if useful.

# RESSOURCES

article on Wilson's algo : https://medium.com/@batbat.senturk/the-ultimate-unbiased-maze-generation-technique-you-need-to-see-46123d5fec76
github : maze generating and solving https://github.com/batuSenturk/Mazes/?source=post_page-----46123d5fec76---------------------------------------

Pour résoudre le maze : BFS - trouve le chemin le plus court et s'il n'y en a qu'un

keyboard key: https://www.cl.cam.ac.uk/~mgk25/ucs/keysymdef.h
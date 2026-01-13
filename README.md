# A-maze-ing
 Create your own maze generator and display its result!

# Usefull tools

- typing module + `MyPy` (see flags --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs)
- `PEP 257` google style for docstings
- docstring pluggin for `flake8`
- frameworks like `pytest` or `unittest` for unit testing
- virtual environments (e.g., venv or conda) for dependency isolation 
- `pdb` debugger
- `MiniLibX` (MLX) library


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





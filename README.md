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
```
<br/>

# MLX for python3

## Step1: Extract and install

- Download  mlx-2.2-py3-ubuntu-any.whl form the project's page and move it to the project's root.
- Extract and install the MLX wheel manually in the site-packages of our virtual environement (venv)

Install in venv:
```bash
# Make sure you're in your project directory with venv activated
cd ~/Desktop/A-maze-ing

# Extract the wheel
mkdir mlx_temp 
cd mlx_temp
unzip ../mlx-2.2-py3-ubuntu-any.whl

# Copy to site-packages
cp -r mlx ../venv/lib/python3.10/site-packages/
cp -r mlx-2.2.dist-info ../venv/lib/python3.10/site-packages

# Clean up
cd ..
rm -rf mlx_temp

# Test
python3 -c "import mlx; print('✓ MLX installed successfully!')"
```


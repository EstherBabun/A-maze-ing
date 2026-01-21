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

# RESSOURCES

article on Wilson's algo : https://medium.com/@batbat.senturk/the-ultimate-unbiased-maze-generation-technique-you-need-to-see-46123d5fec76
github : maze generating and solving https://github.com/batuSenturk/Mazes/?source=post_page-----46123d5fec76---------------------------------------

Pour résoudre le maze : BFS - trouve le chemin le plus court et s'il n'y en a qu'un

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
# rl_engine/maze.py

class Maze:
    def __init__(self, grid):
        """
        grid : list[list[str]] contenant 'S', '.', '#', 'G'
        """
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if self.rows > 0 else 0

    def is_wall(self, r, c) -> bool:
        """
        Retourne True si (r,c) est hors de la grille OU un mur '#'
        """
        if r < 0 or r >= self.rows or c < 0 or c >= self.cols:
            return True
        return self.grid[r][c] == '#'

    def is_goal(self, r, c) -> bool:
        """
        Retourne True si (r,c) est la case but 'G'
        """
        if 0 <= r < self.rows and 0 <= c < self.cols:
            return self.grid[r][c] == 'G'
        return False

    def is_valid(self, r, c) -> bool:
        """
        True si (r,c) est dans la grille ET n'est pas un mur
        """
        if 0 <= r < self.rows and 0 <= c < self.cols:
            return self.grid[r][c] != '#'
        return False

    def get_reward(self, r, c) -> int:
        """
        +100 : goal
        -10  : mur ou tentative d'entrer dans un mur
        -1   : case normale
        """
        if self.is_goal(r, c):
            return 100
        if self.is_wall(r, c):
            return -10
        return -1


# Labyrinthes prédéfinis (liste de grilles). Chaque grille est une liste de lignes
# où chaque ligne est une liste de caractères 'S', '.', '#', 'G'.
# Utiliser MAZES[0] dans la vue pour la démo.
MAZES = [
    [
        list("S...#"),
        list(".#..#"),
        list(".##.."),
        list("...#."),
        list("..G.."),
    ],
    [
        list("S.#.."),
        list("..#.."),
        list(".##.#"),
        list("...#G"),
        list("....."),
    ],
]

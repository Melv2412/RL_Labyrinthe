"""
Module maze.py
Contient les labyrinthes prédéfinis pour le projet
"""

# Liste des labyrinthes prédéfinis
# S = Start (Départ)
# G = Goal (Arrivée)
# # = Wall (Mur)
# . = Empty (Case vide)

MAZES = [
    # Labyrinthe 1 - FACILE (5x5)
    [
        ['S', '.', '#', '.', 'G'],
        ['.', '#', '#', '.', '#'],
        ['.', '.', '.', '.', '.'],
        ['#', '#', '.', '#', '.'],
        ['.', '.', '.', '.', '.'],
    ],
    
    # Labyrinthe 2 - MOYEN (7x7)
    [
        ['S', '.', '.', '#', '.', '.', '.'],
        ['#', '#', '.', '#', '.', '#', '.'],
        ['.', '.', '.', '.', '.', '#', '.'],
        ['.', '#', '#', '#', '.', '#', '.'],
        ['.', '.', '.', '.', '.', '.', '.'],
        ['.', '#', '#', '#', '#', '#', '.'],
        ['.', '.', '.', '.', '.', '.', 'G'],
    ],
    
    # Labyrinthe 3 - DIFFICILE (8x8)
    [
        ['S', '.', '#', '.', '.', '.', '#', '.'],
        ['.', '.', '#', '.', '#', '.', '#', '.'],
        ['.', '#', '#', '.', '#', '.', '.', '.'],
        ['.', '.', '.', '.', '#', '#', '#', '.'],
        ['#', '#', '.', '.', '.', '.', '#', '.'],
        ['.', '.', '.', '#', '#', '.', '#', '.'],
        ['.', '#', '.', '.', '.', '.', '.', '.'],
        ['.', '#', '#', '#', '.', '#', '#', 'G'],
    ],
    
    # Labyrinthe 4 - EXPERT (10x10)
    [
        ['S', '.', '.', '#', '.', '.', '.', '#', '.', '.'],
        ['.', '#', '.', '#', '.', '#', '.', '#', '.', '.'],
        ['.', '#', '.', '.', '.', '#', '.', '.', '.', '#'],
        ['.', '.', '#', '#', '.', '#', '#', '#', '.', '#'],
        ['#', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '#', '#', '#', '#', '.', '#', '#', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.', '#', '.'],
        ['.', '#', '#', '#', '.', '#', '#', '.', '#', '.'],
        ['.', '.', '.', '#', '.', '.', '.', '.', '.', '.'],
        ['#', '#', '.', '#', '#', '#', '.', '#', '#', 'G'],
    ],
    
    # Labyrinthe 5 - SIMPLE (3x3)
    [
        ['S', '.', 'G'],
        ['.', '#', '.'],
        ['.', '.', '.'],
    ],
    
    # Labyrinthe 6 - COMPLEXE (6x9)
    [
        ['S', '.', '.', '#', '.', '.', '.', '.', '.'],
        ['.', '#', '.', '#', '.', '#', '#', '#', '.'],
        ['.', '#', '.', '.', '.', '.', '.', '#', '.'],
        ['.', '.', '#', '#', '#', '.', '.', '#', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
        ['#', '#', '#', '.', '#', '#', '#', '.', 'G'],
    ],
]


# Classe Maze (optionnelle, pour des fonctionnalités supplémentaires)
class Maze:
    """
    Classe représentant un labyrinthe
    Fournit des méthodes utilitaires pour vérifier les propriétés du labyrinthe
    """
    
    def __init__(self, grid):
        """
        Initialise un labyrinthe à partir d'une grille
        
        Args:
            grid: Liste 2D de caractères (S, G, #, .)
        """
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if self.rows > 0 else 0
        self.start = self._find_position('S')
        self.goal = self._find_position('G')
    
    def _find_position(self, target):
        """
        Trouve la position d'un caractère dans la grille
        
        Args:
            target: Caractère à rechercher ('S' ou 'G')
            
        Returns:
            Tuple (r, c) ou None si non trouvé
        """
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == target:
                    return (r, c)
        return None
    
    def is_valid_position(self, r, c):
        """
        Vérifie si une position est valide (dans les limites et pas un mur)
        
        Args:
            r: Ligne
            c: Colonne
            
        Returns:
            bool: True si valide, False sinon
        """
        if not (0 <= r < self.rows and 0 <= c < self.cols):
            return False
        return self.grid[r][c] != '#'
    
    def is_wall(self, r, c):
        """
        Vérifie si une position est un mur
        
        Args:
            r: Ligne
            c: Colonne
            
        Returns:
            bool: True si mur, False sinon
        """
        if not (0 <= r < self.rows and 0 <= c < self.cols):
            return True  # Hors limites = mur
        return self.grid[r][c] == '#'
    
    def is_goal(self, r, c):
        """
        Vérifie si une position est l'arrivée
        
        Args:
            r: Ligne
            c: Colonne
            
        Returns:
            bool: True si arrivée, False sinon
        """
        if not (0 <= r < self.rows and 0 <= c < self.cols):
            return False
        return self.grid[r][c] == 'G'
    
    def get_reward(self, r, c):
        """
        Calcule la récompense pour une position donnée
        
        Args:
            r: Ligne
            c: Colonne
            
        Returns:
            int: Récompense (+100 pour G, -10 pour mur, -1 sinon)
        """
        if self.is_goal(r, c):
            return 100
        if self.is_wall(r, c):
            return -10
        return -1
    
    def get_neighbors(self, r, c):
        """
        Retourne les positions voisines valides
        
        Args:
            r: Ligne
            c: Colonne
            
        Returns:
            Liste de tuples (r, c) des voisins valides
        """
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # haut, bas, gauche, droite
        
        for dr, dc in directions:
            new_r, new_c = r + dr, c + dc
            if self.is_valid_position(new_r, new_c):
                neighbors.append((new_r, new_c))
        
        return neighbors
    
    def validate(self):
        """
        Valide le labyrinthe (1 S, 1 G, au moins un chemin possible)
        
        Returns:
            Tuple (bool, str): (est_valide, message_erreur)
        """
        if not self.start:
            return (False, "Pas de point de départ (S)")
        
        if not self.goal:
            return (False, "Pas de point d'arrivée (G)")
        
        # Vérifier qu'il n'y a qu'un seul S et un seul G
        s_count = sum(row.count('S') for row in self.grid)
        g_count = sum(row.count('G') for row in self.grid)
        
        if s_count != 1:
            return (False, f"Il doit y avoir exactement 1 départ (S), trouvé: {s_count}")
        
        if g_count != 1:
            return (False, f"Il doit y avoir exactement 1 arrivée (G), trouvé: {g_count}")
        
        return (True, "Labyrinthe valide")
    
    def __str__(self):
        """
        Représentation textuelle du labyrinthe
        """
        result = []
        for row in self.grid:
            result.append(' '.join(row))
        return '\n'.join(result)


# Fonction utilitaire pour créer un labyrinthe vide
def create_empty_maze(rows, cols):
    """
    Crée un labyrinthe vide de taille rows x cols
    
    Args:
        rows: Nombre de lignes
        cols: Nombre de colonnes
        
    Returns:
        Liste 2D de '.'
    """
    return [['.' for _ in range(cols)] for _ in range(rows)]
import random
import numpy as np
from typing import List, Tuple

class QLearner:

    
    DIRECTIONS = {
        0: (-1, 0), 
        1: (1, 0),   
        2: (0, -1),  
        3: (0, 1)    
    }
    
    def __init__(self, alpha: float = 0.1, gamma: float = 0.9, epsilon: float = 0.1):

        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = {}  
    
    def init_q_table(self, grid: List[List[str]]):

        self.q_table = {}
        rows = len(grid)
        cols = len(grid[0])
        
        for r in range(rows):
            for c in range(cols):
                # Si ce n'est pas un mur (#), on crée une entrée dans la Q-table
                if grid[r][c] != '#':
                    # 4 actions possibles : haut, bas, gauche, droite
                    self.q_table[(r, c)] = [0.0, 0.0, 0.0, 0.0]
    
    def get_valid_actions(self, state: Tuple[int, int], grid: List[List[str]]) -> List[int]:

        r, c = state
        rows = len(grid)
        cols = len(grid[0])
        valid_actions = []
        
        # Vérifier chaque direction
        for action in range(4):
            dr, dc = self.DIRECTIONS[action]
            new_r, new_c = r + dr, c + dc
            
            # Vérifier si dans les limites
            if 0 <= new_r < rows and 0 <= new_c < cols:
                # Vérifier si pas un mur
                if grid[new_r][new_c] != '#':
                    valid_actions.append(action)
        
        return valid_actions
    
    def choose_action(self, state: Tuple[int, int], grid: List[List[str]]) -> int:

        valid_actions = self.get_valid_actions(state, grid)
        
        if not valid_actions:
            return None
        
        # EXPLORATION : action aléatoire
        if random.random() < self.epsilon:
            return random.choice(valid_actions)
        
        # EXPLOITATION : meilleure action selon Q-table
        # Récupérer les valeurs Q pour cet état
        q_values = self.q_table[state]
        
        # Parmi les actions valides, prendre celle avec la plus grande valeur Q
        best_action = valid_actions[0]
        best_value = q_values[best_action]
        
        for action in valid_actions[1:]:
            if q_values[action] > best_value:
                best_value = q_values[action]
                best_action = action
        
        return best_action
    
    def update_q_value(self, state: Tuple[int, int], action: int, 
                      reward: float, next_state: Tuple[int, int], grid: List[List[str]]):

        # Valeur Q actuelle
        current_q = self.q_table[state][action]
        
        # Meilleure valeur Q pour le prochain état
        if next_state in self.q_table:
            valid_next_actions = self.get_valid_actions(next_state, grid)
            if valid_next_actions:
                next_q_values = [self.q_table[next_state][a] for a in valid_next_actions]
                max_next_q = max(next_q_values)
            else:
                max_next_q = 0
        else:
            max_next_q = 0
        
        # Appliquer la formule Q-learning
        new_q = current_q + self.alpha * (reward + self.gamma * max_next_q - current_q)
        
        # Mettre à jour la Q-table
        self.q_table[state][action] = new_q
    
    def get_best_action(self, state: Tuple[int, int], grid: List[List[str]]) -> int:

        valid_actions = self.get_valid_actions(state, grid)
        
        if not valid_actions:
            return None
        
        # Récupérer les valeurs Q pour cet état
        q_values = self.q_table[state]
        
        # Prendre l'action avec la plus grande valeur Q
        best_action = valid_actions[0]
        best_value = q_values[best_action]
        
        for action in valid_actions[1:]:
            if q_values[action] > best_value:
                best_value = q_values[action]
                best_action = action
        
        return best_action
    
    def train(self, grid: List[List[str]], start_pos: Tuple[int, int], 
              episodes: int = 1000) -> List[float]:

        # Initialiser la Q-table
        self.init_q_table(grid)
        
        rewards_history = []
        rows = len(grid)
        cols = len(grid[0])
        
        for episode in range(episodes):
            state = start_pos
            total_reward = 0
            steps = 0
            max_steps = 100  # Éviter les boucles infinies
            
            while steps < max_steps:
                # Choisir une action
                action = self.choose_action(state, grid)
                if action is None:
                    break
                
                # Calculer la nouvelle position
                dr, dc = self.DIRECTIONS[action]
                new_r, new_c = state[0] + dr, state[1] + dc
                
                # Vérifier si valide (normalement oui, car choose_action vérifie)
                if not (0 <= new_r < rows and 0 <= new_c < cols):
                    break
                
                # Calculer la récompense
                cell = grid[new_r][new_c]
                if cell == 'G':  # Sortie
                    reward = 100
                elif cell == '#':  # Mur (ne devrait pas arriver)
                    reward = -10
                else:  # Case normale
                    reward = -1
                
                # Mettre à jour la Q-table
                self.update_q_value(state, action, reward, (new_r, new_c), grid)
                
                # Mettre à jour l'état
                state = (new_r, new_c)
                total_reward += reward
                steps += 1
                
                # Si sortie trouvée, terminer l'épisode
                if cell == 'G':
                    break
            
            rewards_history.append(total_reward)
        
        return rewards_history


# Fonction pour obtenir le chemin optimal 
def get_optimal_path(grid: List[List[str]], alpha: float = 0.1, 
                    gamma: float = 0.9, epsilon: float = 0.1, 
                    episodes: int = 1000) -> List[Tuple[int, int]]:

    # Trouver la position de départ 'S'
    start_pos = None
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == 'S':
                start_pos = (r, c)
                break
        if start_pos:
            break
    
    if not start_pos:
        raise ValueError("Pas de position de départ 'S' dans le labyrinthe")
    
    # Créer et entraîner l'agent
    agent = QLearner(alpha=alpha, gamma=gamma, epsilon=epsilon)
    agent.train(grid, start_pos, episodes)
    
    # Reconstruire le chemin optimal
    path = [start_pos]
    state = start_pos
    visited = set([state])
    max_steps = 50  # Éviter les boucles
    
    for _ in range(max_steps):
        action = agent.get_best_action(state, grid)
        if action is None:
            break
        
        dr, dc = agent.DIRECTIONS[action]
        new_state = (state[0] + dr, state[1] + dc)
        
        # Éviter les boucles
        if new_state in visited:
            break
        
        path.append(new_state)
        visited.add(new_state)
        state = new_state
        
        # Vérifier si sortie atteinte
        if grid[new_state[0]][new_state[1]] == 'G':
            break
    
    return path
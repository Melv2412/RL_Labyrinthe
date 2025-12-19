import random
import numpy as np
from typing import List, Tuple, Dict, Callable

class QLearnerWithVisualization:
    """Version améliorée avec visualisation complète de l'entraînement"""
    
    DIRECTIONS = {
        0: (-1, 0),  # Haut
        1: (1, 0),   # Bas
        2: (0, -1),  # Gauche
        3: (0, 1)    # Droite
    }
    
    def __init__(self, alpha: float = 0.1, gamma: float = 0.9, epsilon: float = 0.1):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = {}
        self.training_stats = {
            'errors': [],
            'explorations': [],
            'rewards_per_episode': [],
            'best_path_per_episode': []
        }
    
    def init_q_table(self, grid: List[List[str]]):
        """Initialise la Q-table"""
        self.q_table = {}
        rows = len(grid)
        cols = len(grid[0])
        
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] != '#':
                    self.q_table[(r, c)] = [0.0, 0.0, 0.0, 0.0]
    
    def get_valid_actions(self, state: Tuple[int, int], grid: List[List[str]]) -> List[int]:
        """Retourne les actions valides depuis un état"""
        r, c = state
        rows = len(grid)
        cols = len(grid[0])
        valid_actions = []
        
        for action in range(4):
            dr, dc = self.DIRECTIONS[action]
            new_r, new_c = r + dr, c + dc
            
            if 0 <= new_r < rows and 0 <= new_c < cols:
                if grid[new_r][new_c] != '#':
                    valid_actions.append(action)
        
        return valid_actions
    
    def choose_action(self, state: Tuple[int, int], grid: List[List[str]]) -> Tuple[int, str]:
        """Choisit une action (retourne aussi le type: 'explore' ou 'exploit')"""
        valid_actions = self.get_valid_actions(state, grid)
        
        if not valid_actions:
            return None, 'blocked'
        
        # EXPLORATION
        if random.random() < self.epsilon:
            return random.choice(valid_actions), 'explore'
        
        # EXPLOITATION
        q_values = self.q_table[state]
        best_action = valid_actions[0]
        best_value = q_values[best_action]
        
        for action in valid_actions[1:]:
            if q_values[action] > best_value:
                best_value = q_values[action]
                best_action = action
        
        return best_action, 'exploit'
    
    def update_q_value(self, state: Tuple[int, int], action: int, 
                      reward: float, next_state: Tuple[int, int], grid: List[List[str]]):
        """Met à jour la Q-table"""
        current_q = self.q_table[state][action]
        
        if next_state in self.q_table:
            valid_next_actions = self.get_valid_actions(next_state, grid)
            if valid_next_actions:
                next_q_values = [self.q_table[next_state][a] for a in valid_next_actions]
                max_next_q = max(next_q_values)
            else:
                max_next_q = 0
        else:
            max_next_q = 0
        
        new_q = current_q + self.alpha * (reward + self.gamma * max_next_q - current_q)
        self.q_table[state][action] = new_q
    
    def get_current_best_path(self, grid: List[List[str]], start_pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Extrait le meilleur chemin actuel selon la Q-table"""
        path = [start_pos]
        state = start_pos
        visited = set([state])
        max_steps = 100
        
        for _ in range(max_steps):
            valid_actions = self.get_valid_actions(state, grid)
            if not valid_actions:
                break
            
            q_values = self.q_table[state]
            best_action = valid_actions[0]
            best_value = q_values[best_action]
            
            for action in valid_actions[1:]:
                if q_values[action] > best_value:
                    best_value = q_values[action]
                    best_action = action
            
            dr, dc = self.DIRECTIONS[best_action]
            new_state = (state[0] + dr, state[1] + dc)
            
            if new_state in visited:
                break
            
            path.append(new_state)
            visited.add(new_state)
            state = new_state
            
            if grid[new_state[0]][new_state[1]] == 'G':
                break
        
        return path
    
    def train_with_callback(self, grid: List[List[str]], start_pos: Tuple[int, int], 
                           episodes: int = 1000) -> List[Dict]:
        """Entraîne avec callback pour visualisation"""
        self.init_q_table(grid)
        history = []
        rows = len(grid)
        cols = len(grid[0])
        
        for episode in range(episodes):
            state = start_pos
            total_reward = 0
            steps = 0
            max_steps = 100
            episode_path = [state]
            episode_errors = []
            episode_explorations = 0
            
            while steps < max_steps:
                action, action_type = self.choose_action(state, grid)
                
                if action is None:
                    episode_errors.append({
                        'step': steps,
                        'state': state,
                        'error': 'blocked',
                        'message': 'Aucune action valide disponible'
                    })
                    break
                
                if action_type == 'explore':
                    episode_explorations += 1
                
                dr, dc = self.DIRECTIONS[action]
                new_r, new_c = state[0] + dr, state[1] + dc
                
                if not (0 <= new_r < rows and 0 <= new_c < cols):
                    episode_errors.append({
                        'step': steps,
                        'state': state,
                        'action': action,
                        'error': 'out_of_bounds',
                        'message': f'Action mène hors limites: ({new_r}, {new_c})'
                    })
                    break
                
                cell = grid[new_r][new_c]
                
                if cell == 'G':
                    reward = 100
                elif cell == '#':
                    reward = -10
                    episode_errors.append({
                        'step': steps,
                        'state': state,
                        'action': action,
                        'error': 'hit_wall',
                        'message': f'Collision avec un mur à ({new_r}, {new_c})'
                    })
                else:
                    reward = -1
                
                self.update_q_value(state, action, reward, (new_r, new_c), grid)
                
                state = (new_r, new_c)
                episode_path.append(state)
                total_reward += reward
                steps += 1
                
                if cell == 'G':
                    break
            
            # Obtenir le meilleur chemin actuel
            best_path = self.get_current_best_path(grid, start_pos)
            
            # Sauvegarder l'historique
            history.append({
                'episode': episode,
                'reward': total_reward,
                'steps': steps,
                'path': episode_path,
                'best_path': best_path,
                'errors': episode_errors,
                'explorations': episode_explorations,
                'reached_goal': grid[state[0]][state[1]] == 'G'
            })
        
        return history


def get_optimal_path(grid: List[List[str]], alpha: float = 0.1, 
                    gamma: float = 0.9, epsilon: float = 0.1, 
                    episodes: int = 1000) -> List[Tuple[int, int]]:
    """Fonction principale pour obtenir le chemin optimal"""
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
    
    agent = QLearnerWithVisualization(alpha=alpha, gamma=gamma, epsilon=epsilon)
    agent.train_with_callback(grid, start_pos, episodes)
    
    path = agent.get_current_best_path(grid, start_pos)
    return path


def train_with_live_updates(grid: List[List[str]], alpha: float = 0.1, 
                            gamma: float = 0.9, epsilon: float = 0.1, 
                            episodes: int = 1000):
    """Entraîne et retourne l'historique complet pour la visualisation"""
    start_pos = None
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == 'S':
                start_pos = (r, c)
                break
        if start_pos:
            break
    
    if not start_pos:
        raise ValueError("Pas de position de départ 'S'")
    
    agent = QLearnerWithVisualization(alpha=alpha, gamma=gamma, epsilon=epsilon)
    history = agent.train_with_callback(grid, start_pos, episodes)
    final_path = agent.get_current_best_path(grid, start_pos)
    
    return {
        'history': history,
        'final_path': final_path,
        'q_table': agent.q_table,
        'stats': agent.training_stats
    }
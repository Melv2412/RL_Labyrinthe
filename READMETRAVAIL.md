# READMETRAVAIL

Ce fichier décrit précisément ce qui reste à faire dans le projet, pourquoi c'est nécessaire,
et comment l'implémenter étape par étape. Destiné aux membres : Steven, Blé, Yann, Toka, Deric.

## Vue d'ensemble

Le serveur Django (`appgamme/views.py`) appelle `get_optimal_path(maze_grid)` et attend :
- `maze` : la grille (list[list[str]]) contenant `S`, `.`, `#`, `G`.
- `path_str` : liste de chaînes "r,c" représentant le chemin optimal.

Actuellement la vue demo est en place ; il manque l'IA et l'affichage final.

## Tâches restantes (ordre recommandé)

1) Implémenter `Maze` — fichier `rl_engine/maze.py`
   - But : représenter la grille et fournir les règles/ récompenses.
   - Méthodes requises :
     - `is_wall(r, c) -> bool` : True si `grid[r][c] == '#'`.
     - `is_goal(r, c) -> bool` : True si `grid[r][c] == 'G'`.
     - `is_valid(r, c) -> bool` : True si (r,c) à l'intérieur de la grille et pas un mur.
     - `get_reward(r, c) -> int` : +100 si goal, -10 si mur (ou tentative d'entrer dans mur), -1 sinon.
   - Autres : définir `MAZES` (liste d'exemples). Format :
     ```py
     MAZES = [
         [list("S..#G"), list(".##.."), ...],
         ...
     ]
     ```
   - Tests rapides : unit tests pour chaque méthode (bordures, mur, but).

2) Implémenter `QLearner` — fichier `rl_engine/q_learner.py`
   - But : entraîner un agent Q-learning qui, donné un `maze_grid`, apprend une Q-table
     et renvoie le chemin optimal entre `S` et `G`.
   - Classe minimale `QLearner` :
     - Attributs : `q_table` (dict ou numpy array), `alpha`, `gamma`, `epsilon`.
     - Méthodes :
       - `choose_action(r, c, valid_actions) -> int` : ε-greedy sur Q.
       - `update_q(r, c, action, reward, nr, nc, valid_next_actions)` : règle Q-learning :
         Q(s,a) += alpha * (reward + gamma * max_a' Q(s',a') - Q(s,a))
   - Fonction publique `get_optimal_path(maze_grid) -> list[tuple]` :
     - Instancier `Maze(maze_grid)`.
     - Localiser `S` et `G`.
     - Boucler `N` épisodes (ex : 1000) : pour chaque épisode, part de `S` et simule
       jusqu'à terme (atteint `G` ou step limit), appliquant `update_q` à chaque pas.
     - Après entraînement, extraire chemin : partir de `S`, suivre argmax Q tant que
       pas `G` ou boucle détectée, retourner liste de positions.
   - Hyperparamètres conseillés : `alpha=0.1`, `gamma=0.9`, `epsilon=0.1`, `episodes=1000`, `max_steps=500`.
   - Recommandations :
     - Représentation Q-table : dictionnaire keyed by ((r,c),action) si grille petite.
     - Actions : 0=up,1=down,2=left,3=right (ou autre, mais documenter).

3) Template d'affichage — fichier `appgamme/templates/demo.html` (Toka)
   - But : afficher la grille et colorier le chemin selon `path_str`.
   - Pour chaque case, construire la clé `"{r},{c}"` et faire `{% if key in path_str %}`
     pour appliquer la classe `.path`.
   - Classes CSS recommandées : `.start`, `.goal`, `.wall`, `.path`, `.empty`.
   - Démo minimale : un bouton `Recharger` renvoyant la même vue (rafraîchit l'entraînement).

4) Route Django — fichier `appgamme/urls.py` et inclusion dans le routeur principal
   - Ajouter `path('demo/', views.demo_view, name='demo')` puis inclure `appgamme.urls` dans
     le `urls.py` du projet.

5) Dépendances & environnement
   - Ajouter `requirements.txt` (ex : `Django>=3.2`, `numpy` si utilisé).
   - Instructions d'exécution (voir README principal) : créer venv, installer, `runserver`.



## Détails d'implémentation (extraits utiles)

Exemple minimal de `Maze` :
```py
class Maze:
    def __init__(self, grid):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if self.rows else 0

    def is_wall(self, r, c):
        return not (0 <= r < self.rows and 0 <= c < self.cols) or self.grid[r][c] == '#'

    def is_goal(self, r, c):
        return 0 <= r < self.rows and 0 <= c < self.cols and self.grid[r][c] == 'G'

    def is_valid(self, r, c):
        return 0 <= r < self.rows and 0 <= c < self.cols and self.grid[r][c] != '#'

    def get_reward(self, r, c):
        if self.is_goal(r, c):
            return 100
        if self.is_wall(r, c):
            return -10
        return -1
```

Extrait de la boucle d'entraînement (pseudocode) :
```py
for ep in range(episodes):
    r,c = start
    for step in range(max_steps):
        valid_actions = get_valid_actions(r,c)
        a = qlearner.choose_action(r,c,valid_actions)
        nr,nc = step_from_action(r,c,a)
        reward = maze.get_reward(nr,nc)
        next_valid = get_valid_actions(nr,nc)
        qlearner.update_q(r,c,a,reward,nr,nc,next_valid)
        r,c = nr,nc
        if maze.is_goal(r,c): break
```

## Comment valider une implémentation (checklist)
- Lancer `python manage.py runserver` et aller sur `/demo/`.
- Le template affiche correctement la grille (S, G, murs).
- Le chemin affiché colore les cases correspondantes (vérifier `path_str`).
- Ajouter print/logging dans `get_optimal_path` pour confirmer que l'entraînement s'exécute et termine.

## Conseils pratiques / pièges
- Commencer avec labyrinthes petits (5x5) pour déboguer l'agent.
- Utiliser une représentation Q simple (dict) avant d'optimiser en numpy.
- Pour extraire le chemin apprise, suivre argmax Q; défendre contre boucles en limitant la longueur.


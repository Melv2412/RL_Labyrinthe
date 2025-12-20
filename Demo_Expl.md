# Démonstration — boutons de l'interface et commandes d'exécution

Ce fichier décrit l'interface de démonstration (boutons et comportements attendus) ainsi que les commandes pour lancer le projet et exécuter l'entraînement et la démo.

## 1. Boutons/contrôles suggérés pour la démo

- **Start Training** : lance l'entraînement du agent en arrière‑plan. Affiche un indicateur de progression (épisodes, récompense moyenne). Permet paramètres (alpha, gamma, epsilon, épisodes).
- **Stop Training** : arrête proprement l'entraînement (sauvegarde automatique de la Q‑table si demandé).
- **Pause / Resume** : met en pause la boucle d'entraînement et peut reprendre sans réinitialiser l'épisode en cours.
- **Step Training** : effectue un seul pas d'entraînement (utile pour débogage pas à pas).
- **Reset Agent** : réinitialise la Q‑table (ou la remet à une Q‑table chargée par défaut).
- **Randomize Maze** : génère un nouveau labyrinthe aléatoire.
- **Reset Maze** : charge le labyrinthe initial.
- **Play (Greedy)** : exécute un épisode en mode exploitation (\varepsilon=0) pour montrer la politique apprise.
- **Show Q‑values** : active l'affichage des valeurs Q dans chaque case (sous forme de flèches / valeurs numériques).
- **Speed Slider** : contrôle la vitesse d'animation de la démonstration.

## 2. Comportements attendus

- `Start Training` démarre une coroutine / thread qui exécute la boucle d'entraînement et met à jour l'UI régulièrement.
- `Show Q‑values` lit la Q‑table en mémoire et affiche, pour chaque case, l'action avec la plus haute valeur et/ou les valeurs normalisées.
- `Play (Greedy)` exécute la politique courante et affiche la trajectoire; mesurer le nombre d'étapes et si l'agent atteint l'objectif.

## 3. Endpoints API (exemples)

- `POST /api/train/start` — body: `{ "episodes":1000, "alpha":0.1, "gamma":0.95, "epsilon":1.0 }`
- `POST /api/train/stop`
- `POST /api/agent/reset`
- `GET /api/agent/q_values` — renvoie la Q‑table (format JSON ou base64 pickled)

## 4. Commandes pour exécuter le projet (PowerShell)

Depuis la racine du projet (où se trouve `venv`), exemples de commandes PowerShell :

```powershell
& .\venv\Scripts\Activate.ps1
cd RL_Labyrinthe\Labyrinthegame
python manage.py runserver
```

Pour lancer un script d'entraînement (si `q_learner.py` est exécutable en tant que module) :

```powershell
& .\venv\Scripts\Activate.ps1
cd RL_Labyrinthe
python -m rl_engine.q_learner
# ou
python rl_engine\q_learner.py
```

Pour lancer les tests :

```powershell
& .\venv\Scripts\Activate.ps1
cd RL_Labyrinthe
pytest -q
```

Remarques:
- Adaptez les chemins selon votre emplacement courant. Sur Windows PowerShell, utiliser la commande `& .\venv\Scripts\Activate.ps1` pour activer l'environnement virtuel.
- Si les scripts d'entraînement attendent des arguments, fournir `--episodes` etc. selon l'implémentation.

## 5. Flux utilisateur recommandé pour la démo

1. Lancer le serveur web: `python manage.py runserver`.
2. Ouvrir la page de démonstration dans le navigateur.
3. (Optionnel) Charger une Q‑table pré‑entraînée.
4. Cliquer sur `Play (Greedy)` pour voir la politique actuelle.
5. Lancer `Start Training`, observer la progression et afficher `Show Q‑values` pour visualiser l'apprentissage.

---

Si vous voulez, j'ajoute les endpoints Django et un fichier JavaScript minimal pour contrôler ces boutons depuis l'UI.

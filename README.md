# RL_Labyrinthe

Projet de classe : démonstration d'un agent par renforcement (Q-learning)

Objectif : implémenter un agent Q-learning qui apprend à traverser un labyrinthe et afficher
le chemin optimal via une interface Django.

Membres et rôles
- Melvin : intégration Django, vues, déploiement de la démo (controller & template)
- Yann : implémentation de l'algorithme Q-learning (`rl_engine/q_learner.py`)
- Steven & Blé : logique du labyrinthe (`rl_engine/maze.py`)
- Toka : template HTML/CSS pour l'affichage du labyrinthe (`appgamme/templates/demo.html`)
- Deric : mazes prédéfinis, README, captures et documentation

Stack technique
- Python 3.8+
- Django
- Q-learning (algorithme d'apprentissage par renforcement)

Lancement (3 lignes)
1. Créer un environnement virtuel et installer les dépendances :

		python -m venv venv
		venv\Scripts\activate
		pip install -r requirements.txt

2. Lancer le serveur Django :

		python manage.py runserver

3. Ouvrir la page de la démo : `http://127.0.0.1:8000/demo/`

Capture
Voir démo en direct ou capture d'écran dans le dossier `docs/` (placeholder).

Repo
Lien : (ajouter le lien GitHub du projet ici)

Notes
- La vue principale `demo_view` se trouve dans `appgamme/views.py` et appelle
	`get_optimal_path()` pour récupérer le chemin appris puis le transmet au template
	sous forme de `path_str` (liste de chaînes "r,c") pour faciliter le rendu côté template.

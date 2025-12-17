from django.shortcuts import render


try:
	from rl_engine.q_learner import get_optimal_path
	from rl_engine.maze import MAZES
except Exception:
	try:
		from Labyrinthegame.rl_engine.q_learner import get_optimal_path
		from Labyrinthegame.rl_engine.maze import MAZES
	except Exception:
		get_optimal_path = None
		MAZES = []


def demo_view(request):
	"""Vue de démonstration : appelle l'agent RL pour récupérer le chemin optimal.

	Renvoie au template `demo.html` le labyrinthe (`maze`) et `path_str`
	(liste de "r,c") pour faciliter le templating Django.
	"""
	maze = MAZES[0] if MAZES else []
	path = []
	if get_optimal_path and maze:
		try:
			path = get_optimal_path(maze)
		except Exception:
			path = []

	path_str = [f"{r},{c}" for (r, c) in path]
	context = {"maze": maze, "path_str": path_str}
	return render(request, "demo.html", context)

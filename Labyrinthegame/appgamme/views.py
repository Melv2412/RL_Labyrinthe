from django.shortcuts import render, redirect


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
    # Prioritise un labyrinthe personnalisé stocké en session (depuis create/choose),
    # sinon utilise le premier labyrinthe prédéfini.
    maze = request.session.get('last_maze') if request.session.get('last_maze') else (MAZES[0] if MAZES else [])
    path = []
    if get_optimal_path and maze:
        try:
            path = get_optimal_path(maze)
        except Exception:
            path = []

    path_str = [f"{r},{c}" for (r, c) in path]
    context = {"maze": maze, "path_str": path_str}
    return render(request, "demo.html", context)

def home_view(request):
    return render(request, "home.html")

def choose_maze_view(request):
    try:
        from rl_engine.maze import MAZES as _MAZES
    except Exception:
        try:
            from Labyrinthegame.rl_engine.maze import MAZES as _MAZES
        except Exception:
            _MAZES = []
    mazes = [{"grid": g, "rows": len(g), "cols": len(g[0])} for g in _MAZES]
    return render(request, "choose_maze.html", {"mazes": mazes})

def create_maze_view(request):
    rows = range(5); cols = range(5); show = False
    if request.method == "POST" and request.POST.get("action") == "generate":
        try:
            r = int(request.POST.get("rows",5)); c = int(request.POST.get("cols",5))
            rows = range(r); cols = range(c); show = True
        except Exception:
            pass
    return render(request, "create_maze.html", {"show_grid": show, "rows_range": rows, "cols_range": cols})

def about_view(request):
    return render(request, "about.html")

def solve_maze(request):
    if request.method == "POST":
        idx = int(request.POST.get("maze_index",0))
        try:
            from rl_engine.maze import MAZES
        except Exception:
            from Labyrinthegame.rl_engine.maze import MAZES
        request.session['last_maze'] = MAZES[idx] if 0 <= idx < len(MAZES) else []
    return redirect('demo')

def solve_custom_maze(request):
    if request.method == "POST":
        keys = [k for k in request.POST.keys() if k.startswith("cell_")]
        if not keys:
            return redirect('create_maze')
        rows = sorted({int(k.split("_")[1]) for k in keys}); cols = sorted({int(k.split("_")[2]) for k in keys})
        grid = [[request.POST.get(f"cell_{r}_{c}", ".") for c in range(max(cols)+1)] for r in range(max(rows)+1)]
        request.session['last_maze'] = grid
    return redirect('demo')

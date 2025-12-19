from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rl_engine.q_learner import get_optimal_path, train_with_live_updates
from rl_engine.maze import MAZES
import json


def home_view(request):
    """Page d'accueil du projet"""
    return render(request, 'home.html')


def demo_view(request):
    """
    Démonstration avec animation progressive (Option 1)
    """
    maze_grid = [
        ['S', '.', '#', '.', '.'],
        ['.', '#', '#', '.', '#'],
        ['.', '.', '.', '.', '.'],
        ['#', '#', '.', '#', '.'],
        ['.', '.', '.', '.', 'G']
    ]
    
    try:
        path = get_optimal_path(
            grid=maze_grid,
            alpha=0.1,
            gamma=0.9,
            epsilon=0.1,
            episodes=1000
        )
        
        if not path or len(path) <= 1:
            context = {
                'maze': maze_grid,
                'path_str': [],
                'error': 'Aucun chemin trouvé',
                'success': False
            }
        else:
            # Convertir en format JSON pour JavaScript
            path_str = [f"{r},{c}" for r, c in path]
            context = {
                'maze': maze_grid,
                'path_str': json.dumps(path_str),  # JSON pour JavaScript
                'error': None,
                'success': True
            }
    except Exception as e:
        context = {
            'maze': maze_grid,
            'path_str': json.dumps([]),
            'error': str(e),
            'success': False
        }
    
    return render(request, 'demo.html', context)


def training_view(request):
    """
    Visualisation de l'entraînement en direct (Option 2)
    """
    maze_grid = [
        ['S', '.', '#', '.', '.'],
        ['.', '#', '#', '.', '#'],
        ['.', '.', '.', '.', '.'],
        ['#', '#', '.', '#', '.'],
        ['.', '.', '.', '.', 'G']
    ]
    
    try:
        # Entraîner et récupérer l'historique
        training_result = train_with_live_updates(
            grid=maze_grid,
            alpha=0.1,
            gamma=0.9,
            epsilon=0.1,
            episodes=1000
        )
        
        # Préparer les données pour le template
        history_simplified = []
        for episode_data in training_result['history']:
            history_simplified.append({
                'episode': episode_data['episode'],
                'reward': episode_data['reward'],
                'steps': episode_data['steps'],
                'path': [f"{r},{c}" for r, c in episode_data['path']]
            })
        
        final_path = [f"{r},{c}" for r, c in training_result['final_path']]
        
        context = {
            'maze': maze_grid,
            'training_data': json.dumps({
                'history': history_simplified,
                'final_path': final_path
            })
        }
        
    except Exception as e:
        context = {
            'maze': maze_grid,
            'training_data': json.dumps({
                'history': [],
                'final_path': []
            }),
            'error': str(e)
        }
    
    return render(request, 'training.html', context)


def choose_maze_view(request):
    """Affiche la liste des labyrinthes prédéfinis"""
    mazes_data = []
    
    for idx, maze in enumerate(MAZES):
        mazes_data.append({
            'grid': maze,
            'rows': len(maze),
            'cols': len(maze[0]) if maze else 0,
            'index': idx
        })
    
    context = {'mazes': mazes_data}
    return render(request, 'choose_maze.html', context)


def create_maze_view(request):
    """Interface pour créer un labyrinthe personnalisé"""
    context = {'show_grid': False}
    
    if request.method == 'POST':
        try:
            rows = int(request.POST.get('rows', 5))
            cols = int(request.POST.get('cols', 5))
            
            rows = max(3, min(20, rows))
            cols = max(3, min(20, cols))
            
            context['show_grid'] = True
            context['rows_range'] = range(rows)
            context['cols_range'] = range(cols)
            context['rows'] = rows
            context['cols'] = cols
        except ValueError:
            context['error'] = "Valeurs invalides pour les dimensions"
    
    return render(request, 'create_maze.html', context)


def about_view(request):
    """Page d'information sur le projet"""
    return render(request, 'about.html')


def solve_maze_view(request):
    """Résout un labyrinthe prédéfini sélectionné"""
    if request.method != 'POST':
        return redirect('choose_maze')
    
    try:
        maze_index = int(request.POST.get('maze_index', 0))
        
        if maze_index < 0 or maze_index >= len(MAZES):
            context = {
                'error': 'Index de labyrinthe invalide',
                'maze': [],
                'path_str': json.dumps([]),
                'success': False
            }
            return render(request, 'solved_maze.html', context)
        
        maze_grid = MAZES[maze_index]
        
        context = {
            'maze': maze_grid,
            'maze_json': json.dumps(maze_grid),
            'path_str': json.dumps([]),
            'error': None,
            'success': True
        }
        
    except ValueError as e:
        context = {
            'error': f'Erreur de validation: {str(e)}',
            'maze': [],
            'maze_json': json.dumps([]),
            'path_str': json.dumps([]),
            'success': False
        }
    except Exception as e:
        context = {
            'error': f'Erreur lors de la résolution: {str(e)}',
            'maze': [],
            'maze_json': json.dumps([]),
            'path_str': json.dumps([]),
            'success': False
        }
    
    return render(request, 'solved_maze.html', context)


def solve_custom_maze_view(request):
    """Résout un labyrinthe personnalisé créé par l'utilisateur"""
    if request.method != 'POST':
        return redirect('create_maze')
    
    try:
        rows = 0
        cols = 0
        
        for key in request.POST.keys():
            if key.startswith('cell_'):
                parts = key.split('_')
                if len(parts) == 3:
                    r = int(parts[1])
                    c = int(parts[2])
                    rows = max(rows, r + 1)
                    cols = max(cols, c + 1)
        
        if rows == 0 or cols == 0:
            context = {
                'error': 'Aucune grille détectée',
                'maze': [],
                'maze_json': json.dumps([]),
                'path_str': json.dumps([]),
                'success': False
            }
            return render(request, 'solved_maze.html', context)
        
        maze_grid = []
        for r in range(rows):
            row = []
            for c in range(cols):
                cell_value = request.POST.get(f'cell_{r}_{c}', '.')
                if cell_value not in ['S', 'G', '#', '.']:
                    cell_value = '.'
                row.append(cell_value)
            maze_grid.append(row)
        
        # Validation
        s_count = sum(row.count('S') for row in maze_grid)
        g_count = sum(row.count('G') for row in maze_grid)
        
        if s_count == 0:
            context = {
                'error': 'Le labyrinthe doit contenir un point de départ (S)',
                'maze': maze_grid,
                'maze_json': json.dumps(maze_grid),
                'path_str': json.dumps([]),
                'success': False
            }
            return render(request, 'solved_maze.html', context)
        
        if s_count > 1:
            context = {
                'error': 'Un seul point de départ (S) autorisé',
                'maze': maze_grid,
                'maze_json': json.dumps(maze_grid),
                'path_str': json.dumps([]),
                'success': False
            }
            return render(request, 'solved_maze.html', context)
        
        if g_count == 0:
            context = {
                'error': 'Le labyrinthe doit contenir un point d\'arrivée (G)',
                'maze': maze_grid,
                'maze_json': json.dumps(maze_grid),
                'path_str': json.dumps([]),
                'success': False
            }
            return render(request, 'solved_maze.html', context)
        
        if g_count > 1:
            context = {
                'error': 'Un seul point d\'arrivée (G) autorisé',
                'maze': maze_grid,
                'maze_json': json.dumps(maze_grid),
                'path_str': json.dumps([]),
                'success': False
            }
            return render(request, 'solved_maze.html', context)
        
        context = {
            'maze': maze_grid,
            'maze_json': json.dumps(maze_grid),
            'path_str': json.dumps([]),
            'error': None,
            'success': True
        }
        
    except ValueError as e:
        context = {
            'error': f'Erreur de validation: {str(e)}',
            'maze': maze_grid if 'maze_grid' in locals() else [],
            'maze_json': json.dumps(maze_grid if 'maze_grid' in locals() else []),
            'path_str': json.dumps([]),
            'success': False
        }
    except Exception as e:
        context = {
            'error': f'Erreur lors de la résolution: {str(e)}',
            'maze': maze_grid if 'maze_grid' in locals() else [],
            'maze_json': json.dumps(maze_grid if 'maze_grid' in locals() else []),
            'path_str': json.dumps([]),
            'success': False
        }
    
    return render(request, 'solved_maze.html', context)


def train_api(request):
    """API pour l'entraînement en temps réel"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)
    
    try:
        data = json.loads(request.body)
        maze_grid = data.get('maze', [])
        episodes = data.get('episodes', 1000)
        
        # Validation
        if not maze_grid:
            return JsonResponse({'error': 'Grille invalide'}, status=400)
        
        # Validation du labyrinthe
        s_count = sum(row.count('S') for row in maze_grid)
        g_count = sum(row.count('G') for row in maze_grid)
        
        if s_count != 1:
            return JsonResponse({
                'error': f'Le labyrinthe doit contenir exactement un point de départ (S). Trouvé: {s_count}',
                'success': False
            }, status=400)
        
        if g_count != 1:
            return JsonResponse({
                'error': f'Le labyrinthe doit contenir exactement un point d\'arrivée (G). Trouvé: {g_count}',
                'success': False
            }, status=400)
        
        # Entraîner l'agent
        result = train_with_live_updates(
            grid=maze_grid,
            alpha=0.1,
            gamma=0.9,
            epsilon=0.1,
            episodes=episodes
        )
        
        # Simplifier l'historique pour le JSON
        history_simplified = []
        for episode_data in result['history']:
            history_simplified.append({
                'episode': episode_data['episode'],
                'reward': episode_data['reward'],
                'steps': episode_data['steps'],
                'path': episode_data['path'],
                'best_path': episode_data.get('best_path', []),
                'errors': episode_data.get('errors', []),
                'explorations': episode_data.get('explorations', 0),
                'reached_goal': episode_data.get('reached_goal', False)
            })
        
        return JsonResponse({
            'success': True,
            'history': history_simplified,
            'final_path': result['final_path'],
            'total_episodes': len(history_simplified)
        })
        
    except ValueError as e:
        return JsonResponse({
            'error': f'Erreur de validation: {str(e)}',
            'success': False
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'error': f'Erreur lors de l\'entraînement: {str(e)}',
            'success': False
        }, status=500)
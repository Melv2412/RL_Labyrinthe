from django.urls import path
from . import views

urlpatterns = [
    # Page d'accueil
    path('', views.home_view, name='home'),
    
    # Page de démonstration avec un labyrinthe exemple
    path('demo/', views.demo_view, name='demo'),
    
    # Page pour choisir parmi les labyrinthes prédéfinis
    path('choose/', views.choose_maze_view, name='choose_maze'),
    
    # Page pour créer un labyrinthe personnalisé
    path('create/', views.create_maze_view, name='create_maze'),
    
    # Page d'information sur le projet
    path('about/', views.about_view, name='about'),
    
    # Route POST pour résoudre un labyrinthe prédéfini
    path('solve/', views.solve_maze_view, name='solve_maze'),
    
    # Route POST pour résoudre un labyrinthe personnalisé
    path('solve-custom/', views.solve_custom_maze_view, name='solve_custom_maze'),
    
    # Page de visualisation d'entraînement
    path('training/', views.training_view, name='training'),
    
    # API pour l'entraînement en temps réel (NOUVELLE ROUTE)
    path('api/train/', views.train_api, name='train_api'),
]
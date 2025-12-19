from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('demo/', views.demo_view, name='demo'),
    path('choose/', views.choose_maze_view, name='choose_maze'),
    path('create/', views.create_maze_view, name='create_maze'),
    path('about/', views.about_view, name='about'),
    path('solve_maze/', views.solve_maze, name='solve_maze'),
    path('solve_custom_maze/', views.solve_custom_maze, name='solve_custom_maze'),
]
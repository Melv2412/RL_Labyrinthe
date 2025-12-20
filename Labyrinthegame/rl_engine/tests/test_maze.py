import pytest

from rl_engine.maze import Maze, MAZES


def test_maze_basics():
    grid = [list("S.#"), list("..G")]
    m = Maze(grid)
    assert m.rows == 2
    assert m.cols == 3
    assert m.is_wall(0, 2) is True
    assert m.is_valid(0, 1) is True
    assert m.is_goal(1, 2) is True
    assert m.get_reward(1, 2) == 100
    # out of bounds -> wall
    assert m.is_wall(-1, 0) is True


def test_mazes_defined():
    assert isinstance(MAZES, list)
    assert len(MAZES) >= 1

import pytest

from rl_engine.maze import MAZES

try:
    from rl_engine.q_learner import get_optimal_path
except Exception:
    get_optimal_path = None


def test_get_optimal_path_runs_and_contains_goal():
    if get_optimal_path is None:
        pytest.skip("get_optimal_path not implemented")
    grid = MAZES[0]
    path = get_optimal_path(grid, episodes=200)
    assert isinstance(path, list)
    # Check if any position in path corresponds to 'G'
    found_goal = any(grid[r][c] == 'G' for (r, c) in path)
    assert found_goal, "The returned path does not contain the goal position"

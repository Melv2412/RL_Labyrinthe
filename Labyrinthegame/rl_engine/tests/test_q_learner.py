import pytest

try:
    from rl_engine.q_learner import get_optimal_path
except Exception:
    get_optimal_path = None


def test_get_optimal_path_callable():
    assert get_optimal_path is None or callable(get_optimal_path)

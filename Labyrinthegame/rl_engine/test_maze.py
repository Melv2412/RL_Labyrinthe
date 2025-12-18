from maze import Maze
def test_maze():
    grid = [
        list("S.#G"),
        list("...."),
    ]
    maze = Maze(grid)

    # murs
    assert maze.is_wall(0, 2) is True
    assert maze.is_wall(-1, 0) is True
    assert maze.is_wall(0, 0) is False

    # goal
    assert maze.is_goal(0, 3) is True
    assert maze.is_goal(0, 0) is False

    # validité
    assert maze.is_valid(1, 1) is True
    assert maze.is_valid(0, 2) is False
    assert maze.is_valid(5, 5) is False

    # récompenses
    assert maze.get_reward(0, 3) == 100   # goal
    assert maze.get_reward(0, 2) == -10   # mur
    assert maze.get_reward(1, 1) == -1    # normal

    print("✅ Tous les tests Maze sont OK")


if __name__ == "__main__":
    test_maze()

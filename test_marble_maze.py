#!/usr/bin/python3

import unittest
from collections import deque
from unittest.mock import Mock, MagicMock
import sys

# Mock the sense_hat module before importing marble_maze
sys.modules["sense_hat"] = MagicMock()

from marble_maze import MarbleMaze, r, g  # noqa: E402


maze_count = 10


class TestMarbleMaze(unittest.TestCase):
    def setUp(self):
        """Create a new MarbleMaze instance for each test"""
        # Create a mock SenseHat that tracks pixel operations
        mock_sense = Mock()
        mock_sense.clear = Mock()
        mock_sense.set_pixels = Mock()
        mock_sense.set_rotation = Mock()

        self.mm = MarbleMaze(sense=mock_sense)

    def test_maze_is_solvable(self):
        """Test that the maze is always solvable from (0,0) using BFS"""
        for _ in range(maze_count):  # Test multiple generated mazes
            self.mm.reset()
            maze = self.mm.maze

            # Find goal position
            goal_pos = None
            for y in range(8):
                for x in range(8):
                    if maze[y][x] == g:
                        goal_pos = (x, y)
                        break
                if goal_pos:
                    break

            self.assertIsNotNone(goal_pos, "Goal should exist in the maze")

            # BFS to find path from (0,0) to goal
            queue = deque([(0, 0)])
            visited = {(0, 0)}
            found = False

            while queue:
                x, y = queue.popleft()

                if (x, y) == goal_pos:
                    found = True
                    break

                # Check all 4 directions
                for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
                    nx, ny = x + dx, y + dy
                    if (
                        0 <= nx < 8
                        and 0 <= ny < 8
                        and (nx, ny) not in visited
                        and maze[ny][nx] != r
                    ):
                        visited.add((nx, ny))
                        queue.append((nx, ny))

            self.assertTrue(found, "Maze should be solvable")

    def test_at_least_one_fork(self):
        """Test that there is at least one fork (junction) in the path"""
        for _ in range(maze_count):  # Test multiple generated mazes
            self.mm.reset()
            maze = self.mm.maze

            fork_found = False

            # A fork exists when a passage has 3 or 4 neighboring passages
            for y in range(8):
                for x in range(8):
                    if maze[y][x] != r:  # If it's a passage or goal
                        neighbors = 0
                        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < 8 and 0 <= ny < 8 and maze[ny][nx] != r:
                                neighbors += 1

                        if neighbors >= 3:
                            fork_found = True
                            break
                if fork_found:
                    break

            self.assertTrue(fork_found, "Maze should have at least one fork/junction")

    def test_goal_distance_from_start(self):
        """Test that the goal is at least two corners away from start (0,0)"""
        for _ in range(maze_count):  # Test multiple generated mazes
            self.mm.reset()
            maze = self.mm.maze

            # Find goal position
            goal_pos = None
            for y in range(8):
                for x in range(8):
                    if maze[y][x] == g:
                        goal_pos = (x, y)
                        break
                if goal_pos:
                    break

            self.assertIsNotNone(goal_pos, "Goal should exist in the maze")

            # BFS to count corners (direction changes) from start to goal
            queue: deque[tuple[int, int, int | None, int]] = deque(
                [(0, 0, None, 0)]
            )  # (x, y, prev_direction, corners)
            visited: dict[tuple[int, int, int | None], int] = {(0, 0, None): 0}
            min_corners = float("inf")

            while queue:
                x, y, prev_dir, corners = queue.popleft()

                if (x, y) == goal_pos:
                    min_corners = min(min_corners, corners)
                    continue

                # Check all 4 directions
                for i, (dx, dy) in enumerate([(0, -1), (1, 0), (0, 1), (-1, 0)]):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < 8 and 0 <= ny < 8 and maze[ny][nx] != r:
                        new_corners = corners
                        if prev_dir is not None and prev_dir != i:
                            new_corners += 1

                        state = (nx, ny, i)
                        if state not in visited or visited[state] > new_corners:
                            visited[state] = new_corners
                            queue.append((nx, ny, i, new_corners))

            self.assertGreaterEqual(
                min_corners,
                2,
                "Goal should be at least 2 corners from start, found %s" % min_corners,
            )

    def test_no_double_thick_walls(self):
        """Test that there are no walls that are two thick (2x2 blocks of walls)"""
        for _ in range(maze_count):  # Test multiple generated mazes
            self.mm.reset()
            maze = self.mm.maze

            # Check for 2x2 blocks of walls
            for y in range(7):
                for x in range(7):
                    block = [
                        maze[y][x],
                        maze[y][x + 1],
                        maze[y + 1][x],
                        maze[y + 1][x + 1],
                    ]

                    # All four cells should not all be walls
                    all_walls = all(cell == r for cell in block)
                    self.assertFalse(
                        all_walls, f"Found 2x2 block of walls at position ({x},{y})"
                    )

    def test_goal_exists(self):
        """Test that exactly one goal exists in each maze"""
        for _ in range(10):
            self.mm.reset()
            maze = self.mm.maze

            goal_count = 0
            for y in range(8):
                for x in range(8):
                    if maze[y][x] == g:
                        goal_count += 1

            self.assertEqual(
                goal_count, 1, "There should be exactly one goal in the maze"
            )


if __name__ == "__main__":
    unittest.main()

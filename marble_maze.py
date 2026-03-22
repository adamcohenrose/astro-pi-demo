#!/usr/bin/python3

from sense_hat import SenseHat
from time import sleep
import random

r = (255, 0, 0)
o = (0, 0, 0)
w = (255, 255, 255)
g = (0, 200, 0)


class MarbleMaze:
    def __init__(self, sense=None):
        if sense is None:
            self.sense = SenseHat()
            self.sense.clear()
        else:
            self.sense = sense

        self.maze: list[list[tuple[int, int, int]]] = []
        self.reset()

    def generate_maze(self, width=8, height=8):
        # Initialize grid with walls
        maze: list[list[tuple[int, int, int]]] = [
            [r for _ in range(width)] for _ in range(height)
        ]

        # Track visited nodes to ensure connectivity and find a far exit
        visited = []

        def walk(x, y):
            maze[y][x] = o
            visited.append((x, y))

            # Directions: move 2 units to maintain 1px wall thickness
            dirs = [(0, 2), (0, -2), (2, 0), (-2, 0)]
            random.shuffle(dirs)

            for dx, dy in dirs:
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height:
                    if maze[ny][nx] == r:
                        # Carve the path and the wall between
                        maze[y + dy // 2][x + dx // 2] = o
                        walk(nx, ny)
                    elif random.random() < 0.2:
                        # Create a loop/braid by knocking down a wall to an existing path
                        maze[y + dy // 2][x + dx // 2] = o

        # 1. Start at top-left
        walk(0, 0)

        # 2. BREAK THE BOTTOM AND RIGHT WALLS
        # This logic looks at the edges and "leaks" the path into the 8th pixel
        for i in range(0, 8, 2):
            # Randomly open the right-most wall (column 7)
            if random.random() < 0.5:
                maze[i][7] = o
                # Ensure it's connected to the cell to its left
                maze[i][6] = o

            # Randomly open the bottom-most wall (row 7)
            if random.random() < 0.5:
                maze[7][i] = o
                # Ensure it's connected to the cell above it
                maze[6][i] = o

        # 3. Find all current passageways to pick an End point
        all_passages = [(x, y) for y in range(8) for x in range(8) if maze[y][x] == o]

        # Filter for "End" (g) points at least two corners away from (0,0)
        # We define "far" as bottom-right quadrant or far edges
        potential_ends = [(x, y) for (x, y) in all_passages if (x + y) >= 9]

        if not potential_ends:
            # Fallback to absolute bottom corner if the randomizer was stingy
            maze[7][7] = o
            potential_ends = [(7, 7)]

        end_x, end_y = random.choice(potential_ends)

        # 4. Place End
        maze[end_y][end_x] = g

        return maze

    def reset(self):
        self.maze = self.generate_maze()
        self.x, self.y = 0, 0

    def check_wall(self, x, y, new_x, new_y):
        if new_x < 0 or new_x > 7 or new_y < 0 or new_y > 7:
            return x, y
        if self.maze[new_y][new_x] != r:
            return new_x, new_y
        elif self.maze[new_y][x] != r:
            return x, new_y
        elif self.maze[y][new_x] != r:
            return new_x, y
        else:
            return x, y

    def move_marble(self, pitch, roll, x, y):
        new_x = x
        new_y = y
        if 1 < pitch < 179 and x > 0:
            new_x -= 1
        elif 181 < pitch < 359 and x < 7:
            new_x += 1
        if 1 < roll < 179 and y < 7:
            new_y += 1
        elif 181 < roll < 359 and y > 0:
            new_y -= 1
        new_x, new_y = self.check_wall(x, y, new_x, new_y)
        return new_x, new_y

    def win_animation(self, x, y):
        for frame in range(1, 8):
            min_x = max(x - frame, 0)
            max_x = min(x + frame, 8)
            min_y = max(y - frame, 0)
            max_y = min(y + frame, 8)
            for fill_x in range(min_x, max_x):
                for fill_y in range(min_y, max_y):
                    self.maze[fill_y][fill_x] = (240, 240, 0)
            self.sense.set_pixels(sum(self.maze, []))
            sleep(0.1)
        sleep(0.3)
        self.sense.clear()
        sleep(0.3)

    def main_loop(self):
        orientation = self.sense.get_orientation()
        pitch = orientation["pitch"]
        roll = orientation["roll"]
        self.x, self.y = self.move_marble(pitch, roll, self.x, self.y)
        if self.maze[self.y][self.x] == g:
            self.win_animation(self.x, self.y)
            self.reset()
        self.maze[self.y][self.x] = w
        self.sense.set_pixels(sum(self.maze, []))
        self.maze[self.y][self.x] = o
        sleep(0.05)

    def finish(self):
        self.sense.clear()


if __name__ == "__main__":
    mm = MarbleMaze()
    try:
        while True:
            mm.main_loop()
    # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        pass
    finally:
        mm.finish()

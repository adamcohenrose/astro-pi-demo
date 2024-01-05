#!/usr/bin/python3

# Based on the Marble Maze tutorial from Raspberry Pi
# https://github.com/raspberrypilearning/sense-hat-marble-maze
# Licenced under a Creative Commons Attribution 4.0 International License
# http://creativecommons.org/licenses/by-sa/4.0/

from sense_hat import SenseHat
from time import sleep

r = (255,0,0)
o = (0,0,0)
w = (255,255,255)
g = (0,200,0)

class MarbleMaze:

    def __init__(self, sense=None):
        if sense is None:
            self.sense = SenseHat()
            self.sense.clear()
        else:
            self.sense = sense

        self.x, self.y = 1, 1
        self.maze = []
        self.reset()

    def reset(self):
        self.maze.clear()
        self.maze.extend([[r,r,r,r,r,r,r,r],
                          [r,o,o,o,o,o,o,r],
                          [r,r,r,o,r,o,o,r],
                          [r,o,r,o,r,r,r,r],
                          [r,o,o,o,o,o,o,r],
                          [r,o,r,r,r,r,o,r],
                          [r,o,o,r,g,o,o,r],
                          [r,r,r,r,r,r,r,r]])

    def check_wall(self, x, y, new_x, new_y):
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
                    self.maze[fill_y][fill_x] = (240,240,0)
            self.sense.set_pixels(sum(self.maze,[]))
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
            self.x, self.y = 1, 1
        self.maze[self.y][self.x] = w
        self.sense.set_pixels(sum(self.maze,[]))
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

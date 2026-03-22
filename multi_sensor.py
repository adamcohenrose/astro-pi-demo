#!/usr/bin/python3

import evdev
import marble_maze
import humidity_temp_sensor
from sense_hat import SenseHat
import os

print("starting in {}".format(os.getcwd()))

buttonA = evdev.ecodes.KEY_A
buttonB = evdev.ecodes.KEY_B

sense = SenseHat()
sense.clear()

maze = marble_maze.MarbleMaze(sense)
gauge = humidity_temp_sensor.HumidTempGauge(sense)

current_sensor = maze

# event0 is the gpio buttons (event1 is the joystick)
device = evdev.InputDevice('/dev/input/event0')

if __name__ == "__main__":
    try:
        while True:
            current_sensor.main_loop()

            event = device.read_one()
            if event is not None and event.type == evdev.ecodes.EV_KEY:
                if event.code == buttonA and event.value == 1:
                    current_sensor = maze
                elif event.code == buttonB and event.value == 1:
                    current_sensor = gauge

    # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        pass
    finally:
        sense.clear()

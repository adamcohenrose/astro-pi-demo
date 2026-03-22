#!/usr/bin/python3

import time

from base_runner import BaseRunner
import evdev
from marble_maze import MarbleMaze
from humidity_temp_sensor import HumidTempGauge
from camera_colour_scanner import CameraColourScanner
from cohort_runner import CohortRunner
from sense_hat import SenseHat
import os

print("starting in {}".format(os.getcwd()))

#####################
# button layout:
#
#   A        L
#         []   D
#   B        R
#
#####################


buttonA = evdev.ecodes.KEY_A
buttonB = evdev.ecodes.KEY_B
buttonL = evdev.ecodes.KEY_L
buttonR = evdev.ecodes.KEY_R
buttonD = evdev.ecodes.KEY_D

sense = SenseHat()
sense.clear()

maze = MarbleMaze(sense)
gauge = HumidTempGauge(sense)
camera_sensor = CameraColourScanner()

# Create cohort runners
script_dir = os.path.dirname(os.path.abspath(__file__))
cohort_dir = os.path.join(script_dir, "2026_cohort")
agheart_runner = CohortRunner(camera_sensor, cohort_dir, "agheart.py")
spacefam_runner = CohortRunner(camera_sensor, cohort_dir, "spacefam.py")
thundery_runner = CohortRunner(camera_sensor, cohort_dir, "thundery.py")


current_display: BaseRunner = maze

# event0 is the gpio buttons (event1 is the joystick)
device = evdev.InputDevice("/dev/input/event0")

if __name__ == "__main__":
    try:
        while True:
            current_display.main_loop()

            event = device.read_one()
            if (
                event is not None
                and event.type == evdev.ecodes.EV_KEY
                and event.value == 1
            ):
                current_display.stop()

                if event.code == buttonA:
                    camera_sensor.stop()
                    maze.reset()
                    current_display = maze
                elif event.code == buttonB:
                    camera_sensor.stop()
                    current_display = gauge
                elif event.code == buttonL:
                    camera_sensor.start()
                    current_display = agheart_runner
                elif event.code == buttonR:
                    camera_sensor.start()
                    current_display = spacefam_runner
                elif event.code == buttonD:
                    camera_sensor.start()
                    current_display = thundery_runner

    # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        pass
    finally:
        sense.clear()

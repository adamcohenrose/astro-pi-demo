#!/usr/bin/python3

import time

from base_runner import BaseRunner
from camera_colour_scanner import CameraColourScanner
import evdev
from marble_maze import MarbleMaze
from humidity_temp_sensor import HumidTempGauge
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
buttonU = evdev.ecodes.KEY_U
buttonD = evdev.ecodes.KEY_D

sense = SenseHat()
sense.clear()

maze = MarbleMaze(sense)
gauge = HumidTempGauge(sense)


# Create cohort runners
script_dir = os.path.dirname(os.path.abspath(__file__))
cohort_dir = os.path.join(script_dir, "2026_cohort")
camera_colour_scanner = CameraColourScanner()
agheart_runner = CohortRunner(camera_colour_scanner, cohort_dir, "agheart.py")
spacefam_runner = CohortRunner(camera_colour_scanner, cohort_dir, "spacefam.py")
thundery_runner = CohortRunner(camera_colour_scanner, cohort_dir, "thundery.py")


current_display: BaseRunner = maze

# event0 is the gpio buttons (event1 is the joystick)
device = evdev.InputDevice("/dev/input/event0")

if __name__ == "__main__":
    try:
        current_display.main_loop()

        while True:
            event = device.read_one()
            if (
                event is not None
                and event.type == evdev.ecodes.EV_KEY
                and event.value == 1
            ):
                if current_display:
                    current_display.stop()

                if event.code == buttonA:
                    print("button A")
                    maze.reset()
                    current_display = maze
                elif event.code == buttonB:
                    print("button B")
                    current_display = gauge
                elif event.code == buttonL:
                    print("button L")
                    current_display = agheart_runner
                elif event.code == buttonD:
                    print("button D")
                    current_display = thundery_runner
                elif event.code == buttonU:
                    print("button U")
                    current_display = spacefam_runner

            current_display.main_loop()
            time.sleep(0.01)  # give the CPU a rest

    # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        pass
    finally:
        current_display.stop()
        camera_colour_scanner.stop()
        device.close()  # Explicitly close the input device
        sense.clear()

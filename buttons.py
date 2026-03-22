import evdev

buttonA = evdev.ecodes.KEY_A
buttonB = evdev.ecodes.KEY_B
buttonL = evdev.ecodes.KEY_L
buttonR = evdev.ecodes.KEY_R
buttonD = evdev.ecodes.KEY_D
buttonU = evdev.ecodes.KEY_U

button_map = {
    buttonA: "A",
    buttonB: "B",
    buttonL: "L",
    buttonR: "R",
    buttonD: "D",
    buttonU: "U",
}

# event0 is the gpio buttons (event1 is the joystick)
device = evdev.InputDevice("/dev/input/event0")
for event in device.read_loop():
    if event.type == evdev.ecodes.EV_KEY and event.value == 1:
        if event.code in button_map:
            print(f"Button {button_map[event.code]} pressed")
        else:
            print(event.code)

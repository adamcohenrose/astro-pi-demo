import evdev

buttonA = evdev.ecodes.KEY_A
buttonB = evdev.ecodes.KEY_B

# event0 is the gpio buttons (event1 is the joystick)
device = evdev.InputDevice('/dev/input/event0')
for event in device.read_loop():
    if event.type == evdev.ecodes.EV_KEY:
        if event.code == buttonA and event.value == 1:
            print("A")
        elif event.code == buttonB and event.value == 1:
            print("B")

''' 
To run use python3
There are three different events for each PS4 controller, event0, event1, and event2
    event0 = touchpad buttons only
    event1 = motion sensors
    event2 = all other buttons
Apart from events there are two other folders "by-id" and "by-path" that has some other functionality
    usb-Sony_Interactive_Entertainment_Wireless_Controller-
        if03-event-mouse = touchpad touch position and buttons
        if03-event-joystick = event2
    # the related paths in by-path are the same
All other folders and files do not work with evdev
        

Each interrupt has its own code, type, and value
Buttons have type 01, val 01 (up) or 00 (down)
    X = code 304
    circle = code 305
    triangle = code 307
    square = code 308
    L1 = code 310
    R1 = code 311
    L2 = code 312
    R2 = code 313
    share = code 314
    options = code 315
    PS_symbol = code 316
    L3 = code 317
    R3 = code 318

    touchpad_press = code 272
    touchpad_touch = code 325 and 330 (both are activated simultaneously)

    the extra back button extension does not register

Analog inputs have six important axis types with a range from 0-255
    right joystick = ABS_RX and ABS_RY 
    left joystick = ABS_X and ABS_Y 
    R2 = ABS_RZ 
    L2 = ABS_Z 
The joysticks are at center at 128 and triggers rest at 0

'''

import evdev
from evdev import list_devices, InputDevice, categorize, ecodes

# creates object 'gamepad' to store the data
# you can call it whatever you like
gamepad = InputDevice('/dev/input/event2')

# prints out device info at start
print(gamepad)

# evdev takes care of polling the controller in a loop
for event in gamepad.read_loop():
    # Buttons
    if event.type == ecodes.EV_KEY:
        print(event)
    # Analog gamepad
    elif event.type == ecodes.EV_ABS:
        absevent = categorize(event)
        print(ecodes.bytype[absevent.event.type]
              [absevent.event.code], absevent.event.value)

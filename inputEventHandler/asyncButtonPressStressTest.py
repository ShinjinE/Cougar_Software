'''
Having both controllers connected over bluetooth first then USB second
rapidly press L1 and R1 10 times each one after the other for controller1 then controller2
rapidly press xbutton 10 times at the same time for both controller1 and controller2
Compare how many were missed
For Bluetooth non were missed (repeat x3)
For USB non were missed (repeat x3)
'''

import asyncio
import evdev
import time
from evdev import list_devices, InputDevice, categorize, ecodes

xButton = 304
L1 = 310
R1 = 311
circle = 305
triangle = 307
square = 308
share = 314
options = 315
PS_symbol = 316
L3 = 317
R3 = 318


async def print_events(device):
    '''Async helper function. Print the events from either device in an asyncronous fashion'''
    async for event in device.async_read_loop():
        if event.type == ecodes.EV_KEY:
            if device.path == "/dev/input/event2":
                print("from controller 1")
                if event.code == xButton:
                    print("xbutton")
                elif event.code == R1:
                    print("R1")
                elif event.code == L1:
                    print("L1")
                elif event.code == circle:
                    print("circle")
                elif event.code == triangle:
                    print("triangle")
                elif event.code == square:
                    print("square")
                elif event.code == share:
                    print("share")
                elif event.code == options:
                    print("options")
                elif event.code == PS_symbol:
                    print("ps_symbol")
                elif event.code == L3:
                    print("L3")
                elif event.code == R3:
                    print("R3")
            elif device.path == "/dev/input/event5":
                print("from controller 2")
                if event.code == xButton:
                    print("xbutton")
                elif event.code == R1:
                    print("R1")
                elif event.code == L1:
                    print("L1")
                elif event.code == circle:
                    print("circle")
                elif event.code == triangle:
                    print("triangle")
                elif event.code == square:
                    print("square")
                elif event.code == share:
                    print("share")
                elif event.code == options:
                    print("options")
                elif event.code == PS_symbol:
                    print("ps_symbol")
                elif event.code == L3:
                    print("L3")
                elif event.code == R3:
                    print("R3")


# create gamecontroller objects. Wait until both controllers are plugged in
while True:
    try:
        gamepad1 = InputDevice('/dev/input/event2')
        gamepad2 = InputDevice('/dev/input/event5')
    except:
        continue
    break

# prints out device info at start
print(gamepad1)
print(gamepad2)

for device in gamepad1, gamepad2:
    asyncio.ensure_future(print_events(device))

loop = asyncio.get_event_loop()
loop.run_forever()

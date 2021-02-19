'''
Results when both controllers are pressed at the same time in a rolling fashion L1 -> R1 -> xbutton
from controller 2
4933.738650609
L1
from controller 2
4933.842613742
R1
from controller 2
4933.902622481
L1
from controller 1
4933.945630283
L1
from controller 2
4933.974632127
xbutton
from controller 1
4933.985792588
R1
from controller 2
4934.042633871
R1
from controller 1
4934.089640075
xbutton
from controller 2
4934.138671719
xbutton
from controller 1
4934.169688596
L1
from controller 1
4934.237681952
R1
from controller 1
4934.329672122
xbutton

When only pressed once the time between a down press and a register release:
from controller 2
5114.707034893
xbutton
from controller 2
5114.767064448
xbutton
A ~0.06sec difference
'''

import asyncio
import evdev
import time
from evdev import list_devices, InputDevice, categorize, ecodes

xButton = 304
L1 = 310
R1 = 311

async def print_events(device):
    '''Async helper function. Print the events from either device in an asyncronous fashion'''
    async for event in device.async_read_loop():
        if event.type == ecodes.EV_KEY:
            if device.path == "/dev/input/event2":
                print("from controller 1")
                if event.code == xButton:
                    print(time.perf_counter())
                    print("xbutton")
                elif event.code == R1:
                    print(time.perf_counter())
                    print("R1")
                elif event.code == L1:
                    print(time.perf_counter())
                    print("L1")
            elif device.path == "/dev/input/event5":
                print("from controller 2")
                if event.code == xButton:
                    print(time.perf_counter())
                    print("xbutton")
                elif event.code == R1:
                    print(time.perf_counter())
                    print("R1")
                elif event.code == L1:
                    print(time.perf_counter())
                    print("L1")

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

'''
In terminal:
sudo bluetoothctl
power on
agent on
default-agent
(if not paired already use specific MAC address: 
    scan on 
    pair 4C:B9:9B:68:F1:EA
    trust 4C:B9:9B:68:F1:EA
    pair A4:AE:12:C4:C3:5D
    trust A4:AE:12:C4:C3:5D)
hold PS button and share button down to turn controller to pair mode
connect 4C:B9:9B:68:F1:EA //blue
connect A4:AE:12:C4:C3:5D //black
agent off
power off
exit
'''

import asyncio
import evdev
import time
from evdev import list_devices, InputDevice, categorize, ecodes


async def print_events(device):
    '''Async helper function. Print the events from either device in an asyncronous fashion'''
    async for event in device.async_read_loop():
        if event.type == ecodes.EV_KEY:
            if device.path == "/dev/input/event2":
                print("from controller 1")
            elif device.path == "/dev/input/event5":
                print("from controller 2")

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

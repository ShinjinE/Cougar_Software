import asyncio
import evdev
import time
from evdev import list_devices, InputDevice, categorize, ecodes


async def print_events(device):
    '''Async helper function. Print the events from either device in an asyncronous fashion'''
    async for event in device.async_read_loop():
        print(device.path, evdev.categorize(event), sep=': ')


# main function

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

# test code for reconnecting a disconnected device

# for device in gamepad1, gamepad2:
#     asyncio.ensure_future(print_events(device))

# while True:
#     try:
#         loop = asyncio.get_event_loop()
#         loop.run_forever()
#     except KeyboardInterrupt:
#         break
#     except:
#         gamepad1 = InputDevice('/dev/input/event2')
#         gamepad2 = InputDevice('/dev/input/event5')
#         for device in gamepad1, gamepad2:
#             asyncio.ensure_future(print_events(device))

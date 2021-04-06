import asyncio
import evdev
import time
from evdev import list_devices, InputDevice, categorize, ecodes

MAX_VARIANCE = 5


async def print_events(device):
    '''Async helper function. Print the events from either device in an asyncronous fashion'''
    last = {
        "ABS_RZ": 128,
        "ABS_Z": 128,
        "ABS_RX": 128,
        "ABS_X": 128,
        "ABS_RY": 128,
        "ABS_Y": 128
    }
    async for event in device.async_read_loop():
        if event.type == ecodes.EV_KEY:
            if device.path == "/dev/input/event2":
                print("from controller 1")
            elif device.path == "/dev/input/event5":
                print("from controller 2")
        if event.type == ecodes.EV_ABS:
            absevent = categorize(event)
            currentEvent = absevent.event.value
            if ecodes.bytype[absevent.event.type][absevent.event.code] == 'ABS_RZ':
                if last["ABS_RZ"] != currentEvent:
                    print(currentEvent)
                    last["ABS_RZ"] = currentEvent

            if ecodes.bytype[absevent.event.type][absevent.event.code] == 'ABS_Z':
                if last["ABS_Z"] != currentEvent:
                    print(currentEvent)
                    last["ABS_Z"] = currentEvent

            if ecodes.bytype[absevent.event.type][absevent.event.code] == 'ABS_RX':
                if abs(last["ABS_RX"] - currentEvent) >= MAX_VARIANCE:
                    print(currentEvent)
                    last["ABS_RX"] = currentEvent

            if ecodes.bytype[absevent.event.type][absevent.event.code] == 'ABS_X':
                if abs(last["ABS_X"] - currentEvent) >= MAX_VARIANCE:
                    print(currentEvent)
                    last["ABS_X"] = currentEvent

            if ecodes.bytype[absevent.event.type][absevent.event.code] == 'ABS_RY':
                if abs(last["ABS_RY"] - currentEvent) >= MAX_VARIANCE:
                    print(currentEvent)
                    last["ABS_RY"] = currentEvent

            if ecodes.bytype[absevent.event.type][absevent.event.code] == 'ABS_Y':
                if abs(last["ABS_Y"] - currentEvent) >= MAX_VARIANCE:
                    print(currentEvent)
                    last["ABS_Y"] = currentEvent


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

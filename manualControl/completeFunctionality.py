import asyncio
import evdev
import time
from evdev import list_devices, InputDevice, categorize, ecodes

MAX_VARIANCE = 5
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
lastInput = {
    "ABS_RZ": 128,
    "ABS_Z": 128,
    "ABS_RX": 128,
    "ABS_X": 128,
    "ABS_RY": 128,
    "ABS_Y": 128
}


def printGamepad(gamePad1, gamePad2):
    if gamepad1:
        print("from first controller")
    elif gamePad2:
        print("from second controller")


async def print_events(device):
    '''Async helper function. Print the events from either device in an asyncronous fashion'''
    fromGamepad1 = False
    fromGamepad2 = False
    async for event in device.async_read_loop():
        if device.path == "/dev/input/event2":
            fromGamepad1 = True
        elif device.path == "/dev/input/event5":
            fromGamepad2 = True
        if event.type == ecodes.EV_KEY:
            printGamepad(fromGamepad1, fromGamepad2)
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
        if event.type == ecodes.EV_ABS:
            absevent = categorize(event)
            currentEvent = absevent.event.value
            if ecodes.bytype[absevent.event.type][absevent.event.code] == 'ABS_RZ':
                if lastInput["ABS_RZ"] != currentEvent:
                    printGamepad(fromGamepad1, fromGamepad2)
                    print("R2: ", currentEvent)
                    lastInput["ABS_RZ"] = currentEvent

            if ecodes.bytype[absevent.event.type][absevent.event.code] == 'ABS_Z':
                if lastInput["ABS_Z"] != currentEvent:
                    printGamepad(fromGamepad1, fromGamepad2)
                    print("L2: ", currentEvent)
                    lastInput["ABS_Z"] = currentEvent

            if ecodes.bytype[absevent.event.type][absevent.event.code] == 'ABS_RX':
                if abs(lastInput["ABS_RX"] - currentEvent) >= MAX_VARIANCE:
                    printGamepad(fromGamepad1, fromGamepad2)
                    print("Right Joystick X: ", currentEvent)
                    lastInput["ABS_RX"] = currentEvent

            if ecodes.bytype[absevent.event.type][absevent.event.code] == 'ABS_X':
                if abs(lastInput["ABS_X"] - currentEvent) >= MAX_VARIANCE:
                    printGamepad(fromGamepad1, fromGamepad2)
                    print("Left Joystick X: ", currentEvent)
                    lastInput["ABS_X"] = currentEvent

            if ecodes.bytype[absevent.event.type][absevent.event.code] == 'ABS_RY':
                if abs(lastInput["ABS_RY"] - currentEvent) >= MAX_VARIANCE:
                    printGamepad(fromGamepad1, fromGamepad2)
                    print("Right Joystick Y: ", currentEvent)
                    lastInput["ABS_RY"] = currentEvent

            if ecodes.bytype[absevent.event.type][absevent.event.code] == 'ABS_Y':
                if abs(lastInput["ABS_Y"] - currentEvent) >= MAX_VARIANCE:
                    printGamepad(fromGamepad1, fromGamepad2)
                    print("Left Joystick X: ", currentEvent)
                    lastInput["ABS_Y"] = currentEvent
        fromGamepad1 = False
        fromGamepad2 = False


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

import asyncio
import evdev
import time
from evdev import list_devices, InputDevice, categorize, ecodes
from ButtonTest_ServoHandler_2 import ServoHandler

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
    "ABS_Y": 128,
    "ABS_HAT0X": 0,
    "ABS_HAT0Y": 0
}

servoHandler = ServoHandler()

class ControllerEvent:
    def __init__(self, name, value):
        self.name = name
        self.value = value


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
            if event.code == xButton:
                xButtonInput = ControllerEvent("x_button_1" if fromGamepad1 else "x_button_2", event.value)
                servoHandler.process_input(xButtonInput)
            elif event.code == R1:
                r1ButtonInput = ControllerEvent("r1_button_1" if fromGamepad1 else "r1_button_2", event.value)
                servoHandler.process_input(r1ButtonInput)
            elif event.code == L1:
                l1ButtonInput = ControllerEvent("l1_button_1" if fromGamepad1 else "l1_button_2", event.value)
                servoHandler.process_input(l1ButtonInput)
            elif event.code == circle:
                circleButtonInput = ControllerEvent("circle_button_1" if fromGamepad1 else "circle_button_2", event.value)
                servoHandler.process_input(circleButtonInput)
            elif event.code == triangle:
                triangleButtonInput = ControllerEvent("triangle_button_1" if fromGamepad1 else "triangle_button_2", event.value)
                servoHandler.process_input(triangleButtonInput)
            elif event.code == square:
                squareButtonInput = ControllerEvent("square_button_1" if fromGamepad1 else "square_button_2", event.value)
                servoHandler.process_input(squareButtonInput)
            elif event.code == share:
                shareButtonInput = ControllerEvent("share_button_1" if fromGamepad1 else "share_button_2", event.value)
                servoHandler.process_input(shareButtonInput)
            elif event.code == options:
                optionsButtonInput = ControllerEvent("options_button_1" if fromGamepad1 else "options_button_2", event.value)
                servoHandler.process_input(optionsButtonInput)
            elif event.code == PS_symbol:
                PS_symbolButtonInput = ControllerEvent("ps_symbol_button_1" if fromGamepad1 else "ps_symbol_button_2", event.value)
                servoHandler.process_input(PS_symbolButtonInput)
            elif event.code == L3:
                l3ButtonInput = ControllerEvent("l3_button_1" if fromGamepad1 else "l3_button_2", event.value)
                servoHandler.process_input(l3ButtonInput)
            elif event.code == R3:
                r3ButtonInput = ControllerEvent("r3_button_1" if fromGamepad1 else "r3_button_2", event.value)
                servoHandler.process_input(r3ButtonInput)

        if event.type == ecodes.EV_ABS:
            absevent = categorize(event)
            currentEvent = absevent.event.value

            if ecodes.bytype[absevent.event.type][absevent.event.code] == 'ABS_RZ':
                if lastInput["ABS_RZ"] != currentEvent:
                    r2AnalogInput = ControllerEvent("r2_analog_1" if fromGamepad1 else "r2_analog_2", currentEvent)
                    servoHandler.process_input(r2AnalogInput)
                    lastInput["ABS_RZ"] = currentEvent

            elif ecodes.bytype[absevent.event.type][absevent.event.code] == 'ABS_Z':
                if lastInput["ABS_Z"] != currentEvent:
                    l2AnalogInput = ControllerEvent("l2_analog_1" if fromGamepad1 else "l2_analog_2", currentEvent)
                    servoHandler.process_input(l2AnalogInput)
                    lastInput["ABS_Z"] = currentEvent

            elif ecodes.bytype[absevent.event.type][absevent.event.code] == 'ABS_RX':
                if abs(lastInput["ABS_RX"] - currentEvent) >= MAX_VARIANCE:
                    rJoystickXAnalogInput = ControllerEvent("r_joystick_x_analog_1" if fromGamepad1 else "r_joystick_x_analog_2", currentEvent)
                    servoHandler.process_input(rJoystickXAnalogInput)
                    lastInput["ABS_RX"] = currentEvent

            elif ecodes.bytype[absevent.event.type][absevent.event.code] == 'ABS_X':
                if abs(lastInput["ABS_X"] - currentEvent) >= MAX_VARIANCE:
                    lJoystickXAnalogInput = ControllerEvent("l_joystick_x_analog_1" if fromGamepad1 else "l_joystick_x_analog_2", currentEvent)
                    servoHandler.process_input(lJoystickXAnalogInput)
                    lastInput["ABS_X"] = currentEvent

            elif ecodes.bytype[absevent.event.type][absevent.event.code] == 'ABS_RY':
                if abs(lastInput["ABS_RY"] - currentEvent) >= MAX_VARIANCE:
                    rJoystickYAnalogInput = ControllerEvent("r_joystick_y_analog_1" if fromGamepad1 else "r_joystick_y_analog_2", currentEvent)
                    servoHandler.process_input(rJoystickYAnalogInput)
                    lastInput["ABS_RY"] = currentEvent

            elif ecodes.bytype[absevent.event.type][absevent.event.code] == 'ABS_Y':
                if abs(lastInput["ABS_Y"] - currentEvent) >= MAX_VARIANCE:
                    lJoystickYAnalogInput = ControllerEvent("l_joystick_y_analog_1" if fromGamepad1 else "l_joystick_y_analog_2", currentEvent)
                    servoHandler.process_input(lJoystickYAnalogInput)
                    lastInput["ABS_Y"] = currentEvent

            else:
                print(ecodes.bytype[absevent.event.type][absevent.event.code])

            if ecodes.bytype[absevent.event.type][absevent.event.code] == 'ABS_HAT0Y':
                if lastInput["ABS_HAT0Y"] != currentEvent:
                    if currentEvent == 1:
                        dDownInput = ControllerEvent("down_button_1" if fromGamepad1 else "down_button_2", True)
                        servoHandler.process_input(dDownInput)
                    elif currentEvent == -1:
                        dUpInput = ControllerEvent("up_button_1" if fromGamepad1 else "up_button_2", True)
                        servoHandler.process_input(dUpInput)
                    else:
                        dUpInput = ControllerEvent("up_button_1" if fromGamepad1 else "up_button_2", currentEvent)
                        servoHandler.process_input(dUpInput)
                        dDownInput = ControllerEvent("down_button_1" if fromGamepad1 else "down_button_2", currentEvent)
                        servoHandler.process_input(dDownInput)
                    lastInput["ABS_HAT0Y"] = currentEvent

            if ecodes.bytype[absevent.event.type][absevent.event.code] == 'ABS_HAT0X':
                if lastInput["ABS_HAT0X"] != currentEvent:
                    if currentEvent == 1:
                        dRightInput = ControllerEvent("right_button_1" if fromGamepad1 else "right_button_2", True)
                        servoHandler.process_input(dRightInput)
                    elif currentEvent == -1:
                        dLeftInput = ControllerEvent("left_button_1" if fromGamepad1 else "left_button_2", True)
                        servoHandler.process_input(dLeftInput)
                    else:
                        dRightInput = ControllerEvent("right_button_1" if fromGamepad1 else "right_button_2", currentEvent)
                        servoHandler.process_input(dRightInput)
                        dLeftInput = ControllerEvent("left_button_1" if fromGamepad1 else "left_button_2", currentEvent)
                        servoHandler.process_input(dLeftInput)
                    lastInput["ABS_HAT0X"] = currentEvent

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

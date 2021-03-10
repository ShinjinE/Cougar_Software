"""
This module will handle all input from the Bluetooth connected PS4 controllers in an asynchronous manner. It expects two controllers to be connected 
and will not run until then. If either controller is disconnected the program will need to be restarted in order to reconnect.
Sends modified controller input to the ServoHandler.
"""
import asyncio
import evdev
from evdev import list_devices, InputDevice, categorize, ecodes
from ServoHandler import ServoHandler

# absolute paths to input files interpreted by the evdev kernel driver for PS4 events
PS4_INPUT_PATH_1 = "/dev/input/event2"  # first controller connected
PS4_INPUT_PATH_2 = "/dev/input/event5"  # second controller connected
# difference from last analog input to current analog input that will register a new servo input
MAX_VARIANCE = 5
# d-pad input values from PS4 controller
D_UP = -1
D_DOWN = 1
D_RIGHT = 1
D_LEFT = -1
# PS4 button input values
X_BUTTON = 304
L1 = 310
R1 = 311
CIRCLE = 305
TRIANGLE = 307
SQUARE = 308
SHARE = 314
OPTIONS = 315
PS_SYMBOL = 316
L3 = 317
R3 = 318
# event codes for analog inputs set to a nuetral position
LAST_INPUT = {
    "ABS_RZ": 128,
    "ABS_Z": 128,
    "ABS_RX": 128,
    "ABS_X": 128,
    "ABS_RY": 128,
    "ABS_Y": 128,
    "ABS_HAT0X": 0,
    "ABS_HAT0Y": 0
}
# custom servo handler class object
servoHandler = ServoHandler()


class ControllerEvent:
    """Controller event object. To be sent to the servo handler to convert a button press to movement, for example. 
    Contains a predetermined name and the current event's value. 
    For buttons the value is 1 or 0. For analog axes it is 0-255. For d-pad hat axes it is -1,0,1."""

    def __init__(self, name, value):
        self.name = name
        self.value = value


async def process_events(device):
    """Async helper function. Process PS4 events and create ControllerEvent objects to be passed to the servoHandler"""
    fromGamepad1 = False
    # fromGamepad2 = False
    async for event in device.async_read_loop():
        if device.path == PS4_INPUT_PATH_1:
            fromGamepad1 = True
        # elif device.path == PS4_INPUT_PATH_2:
        #     fromGamepad2 = True

        if event.type == ecodes.EV_KEY:  # button events
            if event.code == X_BUTTON:
                xButtonInput = ControllerEvent(
                    "x_button_1" if fromGamepad1 else "x_button_2", event.value)
                servoHandler.process_input(xButtonInput)
            elif event.code == R1:
                r1ButtonInput = ControllerEvent(
                    "r1_button_1" if fromGamepad1 else "r1_button_2", event.value)
                servoHandler.process_input(r1ButtonInput)
            elif event.code == L1:
                l1ButtonInput = ControllerEvent(
                    "l1_button_1" if fromGamepad1 else "l1_button_2", event.value)
                servoHandler.process_input(l1ButtonInput)
            elif event.code == CIRCLE:
                circleButtonInput = ControllerEvent(
                    "circle_button_1" if fromGamepad1 else "circle_button_2", event.value)
                servoHandler.process_input(circleButtonInput)
            elif event.code == TRIANGLE:
                triangleButtonInput = ControllerEvent(
                    "triangle_button_1" if fromGamepad1 else "triangle_button_2", event.value)
                servoHandler.process_input(triangleButtonInput)
            elif event.code == SQUARE:
                squareButtonInput = ControllerEvent(
                    "square_button_1" if fromGamepad1 else "square_button_2", event.value)
                servoHandler.process_input(squareButtonInput)
            elif event.code == SHARE:
                shareButtonInput = ControllerEvent(
                    "share_button_1" if fromGamepad1 else "share_button_2", event.value)
                servoHandler.process_input(shareButtonInput)
            elif event.code == OPTIONS:
                optionsButtonInput = ControllerEvent(
                    "options_button_1" if fromGamepad1 else "options_button_2", event.value)
                servoHandler.process_input(optionsButtonInput)
            elif event.code == PS_SYMBOL:
                PS_symbolButtonInput = ControllerEvent(
                    "ps_symbol_button_1" if fromGamepad1 else "ps_symbol_button_2", event.value)
                servoHandler.process_input(PS_symbolButtonInput)
            elif event.code == L3:
                l3ButtonInput = ControllerEvent(
                    "l3_button_1" if fromGamepad1 else "l3_button_2", event.value)
                servoHandler.process_input(l3ButtonInput)
            elif event.code == R3:
                r3ButtonInput = ControllerEvent(
                    "r3_button_1" if fromGamepad1 else "r3_button_2", event.value)
                servoHandler.process_input(r3ButtonInput)

        elif event.type == ecodes.EV_ABS:  # analog and d-pad events
            absevent = categorize(event)
            currentEvent = absevent.event.value
            # right trigger
            if ecodes.bytype[absevent.event.type][absevent.event.code] == 'ABS_RZ':
                if LAST_INPUT["ABS_RZ"] != currentEvent:
                    r2AnalogInput = ControllerEvent(
                        "r2_analog_1" if fromGamepad1 else "r2_analog_2", currentEvent)
                    servoHandler.process_input(r2AnalogInput)
                    LAST_INPUT["ABS_RZ"] = currentEvent
            # left trigger
            elif ecodes.bytype[absevent.event.type][absevent.event.code] == 'ABS_Z':
                if LAST_INPUT["ABS_Z"] != currentEvent:
                    l2AnalogInput = ControllerEvent(
                        "l2_analog_1" if fromGamepad1 else "l2_analog_2", currentEvent)
                    servoHandler.process_input(l2AnalogInput)
                    LAST_INPUT["ABS_Z"] = currentEvent
            # right joystick x-axis
            elif ecodes.bytype[absevent.event.type][absevent.event.code] == 'ABS_RX':
                if abs(LAST_INPUT["ABS_RX"] - currentEvent) >= MAX_VARIANCE:
                    rJoystickXAnalogInput = ControllerEvent(
                        "r_joystick_x_analog_1" if fromGamepad1 else "r_joystick_x_analog_2", currentEvent)
                    servoHandler.process_input(rJoystickXAnalogInput)
                    LAST_INPUT["ABS_RX"] = currentEvent
            # left joystick x-axis
            elif ecodes.bytype[absevent.event.type][absevent.event.code] == 'ABS_X':
                if abs(LAST_INPUT["ABS_X"] - currentEvent) >= MAX_VARIANCE:
                    lJoystickXAnalogInput = ControllerEvent(
                        "l_joystick_x_analog_1" if fromGamepad1 else "l_joystick_x_analog_2", currentEvent)
                    servoHandler.process_input(lJoystickXAnalogInput)
                    LAST_INPUT["ABS_X"] = currentEvent
            # right joystick y-axis
            elif ecodes.bytype[absevent.event.type][absevent.event.code] == 'ABS_RY':
                if abs(LAST_INPUT["ABS_RY"] - currentEvent) >= MAX_VARIANCE:
                    rJoystickYAnalogInput = ControllerEvent(
                        "r_joystick_y_analog_1" if fromGamepad1 else "r_joystick_y_analog_2", currentEvent)
                    servoHandler.process_input(rJoystickYAnalogInput)
                    LAST_INPUT["ABS_RY"] = currentEvent
            # left joystick y-axis
            elif ecodes.bytype[absevent.event.type][absevent.event.code] == 'ABS_Y':
                if abs(LAST_INPUT["ABS_Y"] - currentEvent) >= MAX_VARIANCE:
                    lJoystickYAnalogInput = ControllerEvent(
                        "l_joystick_y_analog_1" if fromGamepad1 else "l_joystick_y_analog_2", currentEvent)
                    servoHandler.process_input(lJoystickYAnalogInput)
                    LAST_INPUT["ABS_Y"] = currentEvent
            # up and down d-pad
            elif ecodes.bytype[absevent.event.type][absevent.event.code] == 'ABS_HAT0Y':
                if LAST_INPUT["ABS_HAT0Y"] != currentEvent:
                    if currentEvent == D_DOWN:
                        dDownInput = ControllerEvent(
                            "down_button_1" if fromGamepad1 else "down_button_2", True)
                        servoHandler.process_input(dDownInput)
                    elif currentEvent == D_UP:
                        dUpInput = ControllerEvent(
                            "up_button_1" if fromGamepad1 else "up_button_2", True)
                        servoHandler.process_input(dUpInput)
                    else:  # because the last input could've been from either up or down, reset both on zero
                        dUpInput = ControllerEvent(
                            "up_button_1" if fromGamepad1 else "up_button_2", currentEvent)
                        servoHandler.process_input(dUpInput)
                        dDownInput = ControllerEvent(
                            "down_button_1" if fromGamepad1 else "down_button_2", currentEvent)
                        servoHandler.process_input(dDownInput)
                    LAST_INPUT["ABS_HAT0Y"] = currentEvent
            # right and left d-pad
            elif ecodes.bytype[absevent.event.type][absevent.event.code] == 'ABS_HAT0X':
                if LAST_INPUT["ABS_HAT0X"] != currentEvent:
                    if currentEvent == D_RIGHT:
                        dRightInput = ControllerEvent(
                            "right_button_1" if fromGamepad1 else "right_button_2", True)
                        servoHandler.process_input(dRightInput)
                    elif currentEvent == D_LEFT:
                        dLeftInput = ControllerEvent(
                            "left_button_1" if fromGamepad1 else "left_button_2", True)
                        servoHandler.process_input(dLeftInput)
                    else:  # because the last input could've been from either right or left, reset both on zero
                        dRightInput = ControllerEvent(
                            "right_button_1" if fromGamepad1 else "right_button_2", currentEvent)
                        servoHandler.process_input(dRightInput)
                        dLeftInput = ControllerEvent(
                            "left_button_1" if fromGamepad1 else "left_button_2", currentEvent)
                        servoHandler.process_input(dLeftInput)
                    LAST_INPUT["ABS_HAT0X"] = currentEvent
        # reset boolean for next PS4 event
        fromGamepad1 = False
        # fromGamepad2 = False


# Create gamecontroller objects. Wait until both controllers are plugged in or connected via bluetooth
while True:
    try:
        gamepad1 = InputDevice(PS4_INPUT_PATH_1)
        gamepad2 = InputDevice(PS4_INPUT_PATH_2)
    except:
        continue
    break

# prints out device info at start
print(gamepad1)
print(gamepad2)
# ensuer the processing of all events from both controllers
for device in gamepad1, gamepad2:
    asyncio.ensure_future(process_events(device))

loop = asyncio.get_event_loop()
loop.run_forever()

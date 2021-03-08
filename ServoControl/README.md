# Servo Control Code
The servo control code consists of the following files
1. ServoHandler.py
2. OutputObject.py
3. AnalogOutputObject.py
4. DigitalOutputObject.py
5. maestro.py
6. maestro-linux/
7. manualControl.py

All the above files are required to properly map inputs and communicate with the maestro board. Only a ServoHandler object needs to be created to control the maestro board with inputs.

## ServoHandler.py
This code recieves the input objects from manual control code. It holds all the objects that map inputs to outputs.

## OutputObject.py
Base object class for mapping inputs.

## AnalogOutputObject.py
Class for mapping analog inputs into outputs to be sent to the maestro board

## DigitalOutputObject.py
Class for mapping digital inputs into outputs to be sent to the maestro board

## maestro.py
Open source code for communicating with the maestro board

## masetro-linux/
Contains drivers for using the maestro board. Also contains the control center program which is useful for creating and changing settings for the board. See readme in this folder for how to properly set up drivers on a new system. 

## manualControl.py
Code to that manages the inputs from the PS4 gamepads. Requires connecting 2 gamepads and the evdev library to be installed on the system to work properly. This is the code that is run in order to control the servos with the gamepads.

The names for each button and analog input are described below for quick reference.
    "x_button_1"
    "x_button_2"
    "r1_button_1"
    "r1_button_2"
    "l1_button_1"
    "l1_button_2"
    "circle_button_1"
    "circle_button_2"
    "triangle_button_1"
    "triangle_button_2"
    "square_button_1"
    "square_button_2"
    "share_button_1"
    "share_button_2"
    "options_button_1"
    "options_button_2"
    "ps_symbol_button_1"
    "ps_symbol_button_2"
    "l3_button_1"
    "l3_button_2"
    "r3_button_1"
    "r3_button_2"
    "r2_analog_1"
    "r2_analog_2"
    "l2_analog_1"
    "l2_analog_2"
    "r_joystick_x_analog_1"
    "r_joystick_x_analog_2"
    "l_joystick_x_analog_1"
    "l_joystick_x_analog_2"
    "r_joystick_y_analog_1"
    "r_joystick_y_analog_2"
    "l_joystick_y_analog_1"
    "l_joystick_y_analog_2"
    "down_button_1"
    "down_button_2"
    "up_button_1"
    "up_button_2"
    "right_button_1"
    "right_button_2"
    "left_button_1"
    "left_button_2"
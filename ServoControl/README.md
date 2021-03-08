# Servo Control Code
The servo control code consists of the following files
1. ServoHandler.py
2. OutputObject.py
3. AnalogOutputObject.py
4. DigitalOutputObject.py
5. maestro.py
6. maestro-linux/

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
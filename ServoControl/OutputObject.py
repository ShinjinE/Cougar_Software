from enum import Enum, auto
import numpy

class OutputObject:
    """
    A class to represent a an output object for a controller input.

    ...

    Attributes
    ----------
    name : str
        name of the servo group for the output
    num_outputs : int
        total number of outputs from the given input
    channels_output : int list
        channels corresponding to the servos controlled by the outputs
    maximums_output : int list
        maximum pulse width values for the corresponding servo channel
    minimums_output : int list
        minimum pulse width values for the corresponding servo channel
    current_output : int list
        current output position of the servos to be used for increment mode
    maximum_input : int
        maximum input value used for mapping inputs to outputs
    minimum_input : int
        minimum input value used for mapping inputs to outputs
    is_inverted : Boolean list
        whether to invert the output mapping
    control_type : Enum ControlType
        mode on how to determine the output

    Methods
    -------
    __init_(name, num_outputs):
        Class constructor.
    set_outputs(channels_output, maximums_output, minimums_output):
        Sets which channels to output to and the maximum and minimun pulse width for each of
        those channels.
    set_inversion(is_inverted):
        Sets whether to invert the output signal or not.
    set_control_direct():
        Sets control mode to direct.
    set_control_toggle():
        Sets control mode to toggle.
    set_control_increment():
        Sets control mode to increment.
    map_input(input_value):
        Maps the input value to outputs for the servos.
    """

    def __init__(self, name, num_outputs):
        self.name = name
        self.num_outputs = num_outputs

        self.channels_output = range(num_outputs)
        self.maximums_output = [8000 for i in range(num_outputs)] 
        self.minimums_output = [4000 for i in range(num_outputs)]
        # self.neutral_output = self.minimums_output
        self.current_output = self.minimums_output

        self.maximum_input = 1
        self.mininum_input = -1
        self.is_inverted = [False for i in range(num_outputs)]

        self.control_type = ControlType.DIRECT

        self.toggle_state = ToggleState.OFF

    def set_outputs(self, channels_output, maximums_output, minimums_output):
        self.channels_output = channels_output
        self.maximums_output = maximums_output
        self.minimums_output = minimums_output
        self.current_output = minimums_output

    def set_inversion(self, is_inverted):
        self.is_inverted = is_inverted

    def set_control_direct(self):
        self.control_type = ControlType.DIRECT

    def set_control_toggle(self):
        self.control_type = ControlType.TOGGLE

    def set_control_increment(self):
        self.control_type = ControlType.INCREMENT

    def get_output(self, input_value):
        return [0]

    def map_values(self, value, input_min, input_max, out_max, out_min):
        return (value - input_min) * (out_max - out_min) / (input_max - input_min) + out_min

class ControlType(Enum):
    DIRECT = auto()
    TOGGLE = auto()
    INCREMENT = auto()

class ToggleState(Enum):
    ON = auto()
    OFF = auto()
from MultiInputOutputObject import MultiInputOutputObject, ControlType

class AnalogMixerOutput(MultiInputOutputObject):
    """
    A class to represent an output object that mixes two analog inputs.
    It inherits attributes and methods from MultiInputOutputObject.

    ...

    Attributes
    ----------
    name : str
        name of the servo group for the output
    num_outputs : int
        total number of outputs calculated from the given input
    channels_output : [int]
        channels corresponding to the servos controlled by the outputs
    maximums_output : [int]
        maximum pulse width values for the corresponding servo channel
    minimums_output : [int]
        minimum pulse width values for the corresponding servo channel
    default_output : [int]
        default output position of the servos for start up position
    current_output : [int]
        current output position of the servos to be used for increment mode
    maximum_input : int
        maximum input value used for mapping inputs to outputs
    minimum_input : int
        minimum input value used for mapping inputs to outputs
    is_inverted : Boolean list
        whether to invert the output mapping
    control_type : Enum ControlType
        mode on how to determine the output
    toggle_state : Enum ToggleState
        used when control mode is set to TOGGLE to determine the current output state
    names_input : [str]
        list of the input names used by the object, this allows the object to know which input value to update
    num_inputs : int
        number of inputs the object uses
    current_input : [int]
        since input is given one at a time, this list keeps track of previous inputs
    out_raw_min : int
        minimum value of an intermediate value used to calculate output
    out_raw_max : int
        maximum value of an intermediate value used to calculate output
    raw_output : [int]
        list to store the calculated intermediate values that will be mapped to final output values

    Methods
    -------
    __init_(name, num_outputs, channels_output, names_input):
        Class constructor. Assigns the values passed in and initalizes remaining members to default values.
    set_outputs(channels_output, maximums_output, minimums_output):
        Sets which channels to output to and the minimun, default, and maximum pulse width for each of those channels.
        Also sets current outputs to the same values as the default.
    set_inversion(is_inverted):
        Sets whether to invert the output signal or not.
    set_control_direct():
        Sets control mode to direct.
    set_control_toggle():
        Sets control mode to toggle.
    set_control_increment():
        Sets control mode to increment.
    get_num_channels():
        Returns the number of output channels for the object.
    get_default_outputs():
        Returns the default output values for the object.
    get_output(input_name, input_value):
        Calculate and returns the output based on the given input value and current control mode.
    map_values(value, input_min, input_max, out_min, out_max):
        Maps an input value to its output.
    """

    def __init__(self, name, num_outputs, channels_output, names_input):
        """
        Class constructor. Assigns the values passed in and initalizes remaining members to default values.

        Parameters
        ----------
        name : string
            name of the output group represented by output object
        num_outputs : int
            number of output channels controlled by the output object
        channels_output : [int]
            list of the output channels used by the object, the order is potentially very specific
        names_input : [str]
            the names of the associated controller inputs with the object
        """
        super().__init__(name, num_outputs, channels_output, names_input)
        # TODO: Check if changing inhertance to MultiInputOutputObject works
        # self.names_input = names_input
        # self.num_inputs = len(self.names_input)
        # self.current_input = [int((self.maximum_input + self.minimum_input)/2) for i in range(self.num_inputs)]
        # self.out_raw_max = self.maximum_input + (self.maximum_input - self.minimum_input)
        # self.out_raw_min = self.minimum_input

    def get_output(self, input_name, input_value):
        """
        Calculate and returns the output based on the given input value and current control mode.

        Parameters
        ----------
        input_name : str
            name associated with the input
        input_value : int
            the input value from the PS4 controller

        Returns
        -------
        [channels_output, current_output] : [[int], [int]]
            current_output is the pulse widths in quarter microseconds to output, and channels_output
            is which channels those outputs will be sent over. How the ouptut is calculated is based
            off of which control type the output object is set to. Direct will map the output directly
            based on the input and the set input and output ranges. Toggle will set the output between
            the max and the min output values and switch between these values whenever the input is
            released. Increment will increment the output value whenever input is given.
        """
        # TODO Write functions for each if statement
        if self.control_type is ControlType.DIRECT:
            # Update corresponding input value
            for i in range(self.num_inputs):
                if self.names_input[i] == input_name:
                    self.current_input[i] = input_value

            # The first input is assumed to be for tilting head left and right
            # The second input is assumed to be for tilting head up and down
            raw_output = self.current_input[0] - self.current_input[1] + self.maximum_input

            # Mapping to the outputs to send to the Maestro board
            for i in range(self.num_outputs):
                self.current_output[i] = self.map_values(raw_output, self.out_raw_min, self.out_raw_max,
                    self.minimums_output[i], self.maximums_output[i])
            return [self.channels_output, self.current_output]

        elif self.control_type is ControlType.INCREMENT:
            # TODO Finish output
            return [self.channels_output, self.current_output]

        else:
            return [self.channels_output, self.current_output]
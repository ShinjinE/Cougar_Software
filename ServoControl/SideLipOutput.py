from MultiInputOutputObject import MultiInputOutputObject, ControlType

class SideLipOutput(MultiInputOutputObject):
    """
    A class to represent a an output object for a digital controller input.

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
    get_output(input_value):
        Returns servo outputs based off of the mapped inputs.
    map_input(input_value, input_min, input_max, out_max, out_min):
        Maps an input value to its output.
    """

    def __init__(self, name, num_outputs, channels_output, names_input):
        """
        Class constructor.

        Parameters
        ----------
        name : string
            name of the output group represented by output object
        num_outputs : int
            number of output channels controlled by the output object, must be 2 for this object
        channels_output : int list
            the two channels to output to, order matters
        names_input : string list
            the two associated controller inputs with the object, first horizontal twist, second is vertical twist
        current_input : int list
            since input is given one at a time, this list keeps track of both inputs
        """
        super().__init__(name, num_outputs, channels_output, names_input)
        self.maximum_input = 1
        self.minimum_input = 0
        self.current_input = [0, 0]
        self.out_raw_max = 1
        self.out_raw_min = -1

    def get_output(self, input_name, input_value):
        """
        Returns servo outputs based off of the mapped inputs.

        Parameters
        ----------
        input_name : string
            name of the associated controller input
        input_value : int
            the analog input from the PS4 controller

        Returns
        -------
        [channels_output, current_output] : [int list, int list]
            current_output is the pulse widths in quarter microseconds to output, and channels_output
            is which channels those outputs will be sent over. How the ouptut is calculated is based
            off of which control type the output object is set to. Direct will map the output directly
            based on the input and the set input and output ranges. Toggle will set the output between
            the max and the min output values and switch between these values whenever the input is
            released. Increment will increment the output value whenever input is given.
        """
        # TODO Write functions for each if statement
        if self.control_type is ControlType.DIRECT:
            for i in range(self.num_inputs):
                if self.names_input[i] == input_name:
                    self.current_input[i] = input_value

            # First input is assumed to be the one that moves the lip up
            # Second input is assumed to be the one that moves the lip down
            raw_output = self.current_input[0] - self.current_input[1]
            for i in range(self.num_outputs):
                self.current_output[i] = self.map_values(raw_output, self.out_raw_min,
                    self.out_raw_max, self.minimums_output[i], self.maximums_output[i])
            return [self.channels_output, self.current_output]

        elif self.control_type is ControlType.INCREMENT:
            # TODO Finish output
            return [self.channels_output, self.current_output]

        else:
            return [self.channels_output, self.current_output]
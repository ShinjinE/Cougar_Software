from OutputObject import OutputObject, ControlType

class MultiInputOutputObject(OutputObject):
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
        super().__init__(name, num_outputs, channels_output)
        self.names_input = names_input
        self.num_inputs = len(self.names_input)
        self.current_input = [int((self.maximum_input + self.minimum_input)/2) for i in range(self.num_inputs)]
        self.out_raw_max = self.maximum_input + (self.maximum_input - self.minimum_input)
        self.out_raw_min = self.minimum_input
        self.raw_output = [0 for i in range(self.num_outputs)]
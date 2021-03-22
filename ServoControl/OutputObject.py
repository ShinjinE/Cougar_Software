from enum import Enum, auto

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
    get_output(input_value):
        Returns servo outputs based off of the mapped inputs.
    map_input(input_value, input_min, input_max, out_max, out_min):
        Maps an input value to its output.
    """

    def __init__(self, name, num_outputs, channels_output):
        """
        Class constructor.

        Parameters
        ----------
        name : string
            name of the output group represented by output object
        num_outputs : int
            number of output channels controlled by the output object
        """
        self.name = name
        self.num_outputs = num_outputs

        self.channels_output = channels_output# range(num_outputs)
        self.maximums_output = [8000 for i in range(num_outputs)] 
        self.minimums_output = [4000 for i in range(num_outputs)]
        self.default_output = [6000 for i in range(num_outputs)]
        self.current_output = [6000 for i in range(num_outputs)]

        self.maximum_input = 255
        self.minimum_input = 0
        self.is_inverted = [False for i in range(num_outputs)]

        self.control_type = ControlType.DIRECT

        self.toggle_state = ToggleState.OFF

    def set_outputs(self, minimums_output, default_output, maximums_output):
        """
        Sets which channels to output to and the maximum and minimun pulse width for each of
        those channels.

        Parameters
        ----------
        channels_output : int list
            channels corresponding to the servos controlled by the outputs
        minimums_output : int list
            minimum pulse width values for the corresponding servo channel
        default_output : int list
            neutral pulse width values for the corresponding servo channel, also determines starting position
        maximums_output : int list
            maximum pulse width values for the corresponding servo channel

        Returns
        -------
        None
        """
        
        self.minimums_output = minimums_output
        self.default_output = default_output
        self.current_output = default_output
        self.maximums_output = maximums_output

    def set_inversion(self, is_inverted):
        """
        Sets whether to invert the output signal or not.

        Parameters
        ----------
        is_inverted : boolean
            the state to set the attribute is_inverted to

        Returns
        -------
        None
        """
        self.is_inverted = is_inverted

    def set_control_direct(self):
        """
        Sets control mode to direct.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.control_type = ControlType.DIRECT

    def set_control_toggle(self):
        """
        Sets control mode to toggle.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.control_type = ControlType.TOGGLE

    def set_control_increment(self):
        """
        Sets control mode to increment.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.control_type = ControlType.INCREMENT

    # TODO Write documentation
    def get_num_channels(self):
        return self.num_outputs

    # def get_output(self, input_value):
    #     """
    #     Use summary from methods section of the class docstring

    #     Parameters
    #     ----------
    #     inputVar : type
    #         Definition

    #     Returns
    #     -------
    #     outputVar : type
    #         Definition
    #     """
    #     return [0]

    def get_default_outputs(self):
        return [self.channels_output, self.default_output]

    def map_values(self, value, input_min, input_max, out_min, out_max):
        """
        Maps an input value to its output.

        Parameters
        ----------
        value : float
            value of the input to map to an output value
        input_min : float
            minimun input value in input range
        input_max : float
            maximun input value in input range
        out_min : int
            minimun output value in output range
        out_max : int
            maximun output value in output range

        Returns
        -------
        mapped_output : int
            pulse width to output for the given input value
        """
        return (value - input_min) * (out_max - out_min) / (input_max - input_min) + out_min

class ControlType(Enum):
    """
    The output mode of the input. This determines how output is calculated from the inputs.

    Attributes
    ----------
    DIRECT : auto
        output is mapped directly to the input value
    TOGGLE : auto
        output is switched between states and is triggered by a false value
    INCREMENT : auto
        output is incremented by the input
    """
    DIRECT = auto()
    TOGGLE = auto()
    INCREMENT = auto()

class ToggleState(Enum):
    """
    Used to determine output behavior when the control type is set to toggle mode.

    Attributes
    ----------
    ON : auto
        the output is toggled "on"
    OFF : auto
        the output is toggled "off"
    """
    ON = auto()
    OFF = auto()
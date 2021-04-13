from enum import Enum

class OutputObject:
    """
    A base class to represent a an output object for a controller input.

    ...

    :Attributes:

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
        default output position of the servos for start up position and used for some multi input objects
    current_output : [int]
        current output position of the servos to be used for increment mode or multi input objects
    maximum_input : int
        maximum input value used for mapping inputs to outputs, 255 for analog and 1 for digital
    minimum_input : int
        minimum input value used for mapping inputs to outputs, 0 for both analog and digital
    is_inverted : [Boolean]
        whether to invert the output mapping
    control_type : Enum ControlType
        mode on how to determine the output
    toggle_state : Enum ToggleState
        used when control mode is set to TOGGLE to determine the current output state
    
    ...

    :Methods:

    """

    def __init__(self, name, num_outputs, channels_output):
        """
        Class constructor. Assigns the values passed in and initalizes remaining members to default values.

        :Parameters:

        name : string
            name of the output group represented by output object
        num_outputs : int
            number of output channels controlled by the output object
        channels_output : [int]
            list of the output channels used by the object
        """
        # Set parameters from values passed into constructor
        self.name = name
        self.num_outputs = num_outputs
        self.channels_output = channels_output

        # Set default values for output members
        self.maximums_output = [8000 for i in range(num_outputs)] 
        self.minimums_output = [4000 for i in range(num_outputs)]
        self.default_output = [6000 for i in range(num_outputs)]
        self.current_output = [6000 for i in range(num_outputs)]

        # Set default values for input members
        self.maximum_input = 255
        self.minimum_input = 0
        self.is_inverted = [False for i in range(num_outputs)]

        # Set default values for object states
        self.control_type = ControlType.DIRECT
        self.toggle_state = ToggleState.OFF

    def set_outputs(self, minimums_output, default_output, maximums_output):
        """
        Sets which channels to output to and the minimun, default, and maximum pulse width for each of those channels.
        Also sets current outputs to the same values as the default.

        :Parameters:

        minimums_output : [int]
            minimum pulse width values for the corresponding servo channel
        default_output : [int]
            neutral pulse width values for the corresponding servo channel, also determines starting position
        maximums_output : [int]
            maximum pulse width values for the corresponding servo channel

        :Returns:

        None
        """
        
        self.minimums_output = minimums_output
        self.default_output = default_output
        self.current_output = default_output
        self.maximums_output = maximums_output

    def set_inversion(self, is_inverted):
        """
        Sets whether to invert the output signal or not.

        :Parameters:

        is_inverted : boolean
            the state to set the attribute is_inverted to

        :Returns:

        None
        """
        self.is_inverted = is_inverted

    def set_control_direct(self):
        """
        Sets control mode to direct.

        :Parameters:

        None

        :Returns:

        None
        """
        self.control_type = ControlType.DIRECT

    def set_control_toggle(self):
        """
        Sets control mode to toggle.

        :Parameters:

        None

        :Returns:

        None
        """
        self.control_type = ControlType.TOGGLE

    def set_control_increment(self):
        """
        Sets control mode to increment.

        :Parameters:

        None

        :Returns:

        None
        """
        self.control_type = ControlType.INCREMENT

    def get_num_channels(self):
        """
        Returns the number of output channels for the object.

        :Parameters:

        None

        :Returns:

        num_outputs : int
            number of output channels the object sends output to
        """
        return self.num_outputs

    def get_default_outputs(self):
        """
         Returns the default output values for the object.

        :Parameters:

        None

        :Returns:

        [channels_output, default_output] : [[int], [int]]
            corresponding channels to the default output values for the object
        """
        return [self.channels_output, self.default_output]

    def map_values(self, value, input_min, input_max, out_min, out_max):
        """
        Maps an input value to its output.

        :Parameters:

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

        :Returns:

        mapped_output : int
            pulse width to output for the given input value
        """
        return (value - input_min) * (out_max - out_min) / (input_max - input_min) + out_min

class ControlType(Enum):
    """
    The output mode of the input. This determines how output is calculated from the inputs.

    :Attributes:

    DIRECT : auto
        output is mapped directly to the input value
    TOGGLE : auto
        output is switched between states and is triggered by a false value
    INCREMENT : auto
        output is incremented by the input
    """
    DIRECT = 0
    TOGGLE = 1
    INCREMENT = 2

class ToggleState(Enum):
    """
    Used to determine output behavior when the control type is set to toggle mode.

    :Attributes:

    ON : auto
        the output is toggled "on"
    OFF : auto
        the output is toggled "off"
    """
    ON = 1
    OFF = 0
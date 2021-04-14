from enum import Enum

class OutputObject:
    """
    A base class to represent a an output object for a controller input.

    ...

    :Attributes:
        * **name**\ (\ *str*\ ) -- name of the servo group for the output
        * **num_outputs**\ (\ *int*\ ) -- total number of outputs 
          calculated from the given input
        * **channels_output**\ (\ *[int]*\ ) -- channels corresponding to 
          the servos controlled by the outputs
        * **maximums_output**\ (\ *[int]*\ ) -- maximum pulse width values 
          for the corresponding servo channel
        * **minimums_output**\ (\ *[int]*\ ) -- minimum pulse width values 
          for the corresponding servo channel
        * **default_output**\ (\ *[int]*\ ) -- default output position of 
          the servos for start up position and used for some multi input 
          objects
        * **current_output**\ (\ *[int]*\ ) -- current output position of the 
          servos to be used for increment mode or multi input objects
        * **maximum_input**\ (\ *int*\ ) -- maximum input value used for mapping 
          inputs to outputs, 255 for analog and 1 for digital
        * **minimum_input**\ (\ *int*\ ) -- minimum input value used for mapping 
          inputs to outputs, 0 for both analog and digital
        * **is_inverted**\ (\ *[Boolean]*\ ) -- whether to invert the output 
          mapping
        * **control_type**\ (\ *Enum ControlType*\ ) -- mode on how to determine 
          the output
        * **toggle_state**\ (\ *Enum ToggleState*\ ) -- used when control mode 
          is set to TOGGLE to determine the current output state
    
    ...

    **Methods**

    """

    def __init__(self, name, num_outputs, channels_output):
        """
        Class constructor. Assigns the values passed in and initalizes remaining 
        members to default values.

        :param name: name of the output group represented by output object
        :type name: string
        :param num_outputs: number of output channels controlled by the output 
            object
        :type num_outputs: int
        :param channels_output: list of the output channels used by the object
        :type channels_output: [int]

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
        Sets which channels to output to and the minimun, default, and maximum 
        pulse width for each of those channels.
       
        Also sets current outputs to the same values as the default.

        :param minimums_output: minimum pulse width values for the corresponding 
            servo channel
        :type minimums_output: [int]
        :param default_output: neutral pulse width values for the corresponding 
            servo channel, also determines starting position
        :type default_output: [int]
        :param maximums_output: maximum pulse width values for the corresponding 
            servo channel
        :type maximums_output: [int]

        """
        
        self.minimums_output = minimums_output
        self.default_output = default_output
        self.current_output = default_output
        self.maximums_output = maximums_output

    def set_inversion(self, is_inverted):
        """
        Sets whether to invert the output signal or not.

        :param is_inverted: the state to set the attribute is_inverted to
        :type is_inverted: boolean

        """
        self.is_inverted = is_inverted

    def set_control_direct(self):
        """
        Sets control mode to direct.
        """
        self.control_type = ControlType.DIRECT

    def set_control_toggle(self):
        """
        Sets control mode to toggle.
        """
        self.control_type = ControlType.TOGGLE

    def set_control_increment(self):
        """
        Sets control mode to increment.
        """
        self.control_type = ControlType.INCREMENT

    def get_num_channels(self):
        """
        Returns the number of output channels for the object.

        :return: number of output channels the object sends output to
        :rtype: int
        
        """
        return self.num_outputs

    def get_default_outputs(self):
        """
        Returns the default output values for the object.

        :return: Two lists. The first list is the output channels and the second 
            is the default output for those channels.
        :rtype: [[int], [int]]

        """
        return [self.channels_output, self.default_output]

    def map_values(self, value, input_min, input_max, out_min, out_max):
        """
        Maps an input value to its output.

        :param value: value of the input to map to an output value
        :type value: float
        :param input_min: minimun input value in input range
        :type input_min: float
        :param input_max: maximun input value in input range
        :type input_max: float
        :param out_min: minimun output value in output range
        :type out_min: int
        :param out_max: maximun output value in output range
        :type out_max: int

        :return: pulse width to output for the given input value
        :rtype: int
        """
        return (value - input_min) * (out_max - out_min) / (input_max - input_min) + out_min

class ControlType(Enum):
    """
    The output mode of the input. This determines how output is calculated 
    from the inputs.

    :States:
        * **DIRECT** : output is mapped directly to the input value
        * **TOGGLE** : output is switched between states and is triggered by a 
            zero input value
        * **INCREMENT** : output is incremented when input is received
    """
    DIRECT = 0
    TOGGLE = 1
    INCREMENT = 2

class ToggleState(Enum):
    """
    Used to determine output behavior when the control type is set to toggle mode.

    :States:
        * **ON** : the output is toggled "on"
        * **OFF** : the output is toggled "off"
    """
    ON = 1
    OFF = 0
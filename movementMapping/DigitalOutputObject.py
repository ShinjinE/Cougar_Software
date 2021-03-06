from OutputObject import OutputObject, ControlType, ToggleState

class DigitalOutputObject(OutputObject):
    """
    A class to represent a an output object for a digital controller input.

    It inherits attributes and methods from OutputObject.

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
        super().__init__(name, num_outputs, channels_output)
        self.maximum_input = 1
        self.minimum_input = 0

    def get_output(self, input_name, input_value):
        """
        Calculate and returns the output based on the given input value and 
        current control mode.

        :param input_name: name associated with the input, this object does not 
            use this value
        :type input_name: str
        :param input_value: the input value from the PS4 controller
        :type input_value: int

        :return: Two lists. The first list is the output channels and the second 
            is output values for those channels (in units of quarter of milliseconds).

            How the ouptut is calculated is based off of which control type the output 
            object is set to. Direct will map the output directly based on the input 
            and the set input and output ranges. Toggle will set the output between the 
            max and the min output values and switch between these values whenever the 
            input is released. Increment will increment the output value whenever input 
            is given.
        :rtype: [[int], [int]]
        """
        # TODO Make ugly nested ifs pretty using functions
        if self.control_type is ControlType.DIRECT:
            # TODO Finish output
            for i in range(self.num_outputs):
                self.current_output[i] = self.map_values(input_value, self.minimum_input, self.maximum_input,
                    self.minimums_output[i], self.maximums_output[i])
            return [self.channels_output, self.current_output]

        elif self.control_type is ControlType.TOGGLE:
            if input_value is False:
                if self.toggle_state is ToggleState.ON:
                    self.toggle_state = ToggleState.OFF
                    self.current_output = self.minimums_output
                    return [self.channels_output, self.current_output]
                else:
                    self.toggle_state = ToggleState.ON
                    self.current_output = self.maximums_output
                return [self.channels_output, self.current_output]

        elif self.control_type is ControlType.INCREMENT:
            # TODO Finish output
            return [self.channels_output, self.current_output]
        else:
            return [self.channels_output, self.current_output]
from OutputObject import *

class DigitalOutputObject(OutputObject):
    def __init__(self, name, num_outputs):
        super().__init__(name, num_outputs)
        self.maximum_input = 1
        self.minimum_input = 0

    def get_output(self, input_value):
        # TODO Make ugly nested ifs pretty using functions
        if self.control_type is ControlType.DIRECT:
            # TODO Finish output
            return [self.channels_output, self.current_output]
        elif self.control_type is ControlType.TOGGLE:
            if input_value is False:
                if self.toggle_state is ToggleState.ON:
                    self.toggle_state = ToggleState.OFF
                    return [self.channels_output, self.minimums_output]
                else:
                    # Same but opposite
                    # TODO Finish output
                    return [self.channels_output, self.current_output]
        elif self.control_type is ControlType.INCREMENT:
            # TODO Finish output
            return [self.channels_output, self.current_output]
        else:
            return [self.channels_output, self.current_output]
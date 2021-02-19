from OutputObject import *

class AnalogOutputObject(OutputObject):
    def __init__(self, name, num_outputs):
        super().__init__(name, num_outputs)

    def get_output(self, input_value):
        # TODO Write functions for each if statement
        if self.control_type is ControlType.DIRECT:
            # TODO Finish output
            return [self.channels_output, self.current_output]
        elif self.control_type is ControlType.INCREMENT:
            # TODO Finish output
            return [self.channels_output, self.current_output]
        else:
            return [self.channels_output, self.current_output]
from DigitalOutputObject import DigitalOutputObject
from AnalogOutputObject import AnalogOutputObject
import maestro

class ServoHandler:
    def __init__(self):
        self.servoBoard = maestro.Controller()

        self.l1_digital = DigitalOutputObject("l1", 1, [0])
        self.l2_analog = AnalogOutputObject("l2", 1, [1])
        self.r1_digital = DigitalOutputObject("r1", 1, [2])
        self.r2_analog = AnalogOutputObject("r2", 1, [3])
        self.x_button = DigitalOutputObject("x", 1, [4])
        self.circle_button = DigitalOutputObject("circle", 1, [5])
        self.triangle_button = DigitalOutputObject("triangle", 1, [6])
        self.square_button = DigitalOutputObject("square", 1, [7])
        self.down_button = DigitalOutputObject("down", 1, [8])
        self.right_button = DigitalOutputObject("right", 1, [9])
        self.up_button = DigitalOutputObject("up", 1, [10])
        self.left_button = DigitalOutputObject("left", 1, [11])
        self.r_stick_x = AnalogOutputObject("r2", 1, [12])
        self.r_stick_y = AnalogOutputObject("r2", 1, [13])
        self.l_stick_x = AnalogOutputObject("r2", 1, [14])
        self.l_stick_y = AnalogOutputObject("r2", 1, [15])
        self.r3_button = DigitalOutputObject("r3", 1, [16])
        self.l3_button = DigitalOutputObject("l3", 1, [17])
        self.options_button = DigitalOutputObject("options", 1, [18])
        self.share_button = DigitalOutputObject("share", 1, [19])
        self.ps_button = DigitalOutputObject("ps", 1, [20])

        self.input_map = {
            # "x_button_1": self.x_button,
            # "circle_button_1": self.circle_button,
            # "triangle_button_1": self.triangle_button,
            # "square_button_1": self.square_button,
            # "down_button_1": self.down_button,
            # "up_button_1": self.up_button,
            # "right_button_1": self.right_button,
            # "left_button_1": self.left_button,
            # "r1_button_1": self.r1_digital,
            # "l1_button_1": self.l1_digital,
            # "r2_analog_1": self.r2_analog,
            # "l2_analog_1": self.l2_analog,
            # "r3_button_1": self.r3_button,
            # "l3_button_1": self.l3_button,
            # "r_joystick_x_analog_1": self.r_stick_x,
            # "l_joystick_x_analog_1": self.l_stick_x,
            # "r_joystick_y_analog_1": self.r_stick_y,
            # "l_joystick_y_analog_1": self.l_stick_y,
            # "share_button_1": self.share_button,
            # "options_button_1": self.options_button,
            # "ps_symbol_button_1": self.ps_button,

            "x_button_2": self.x_button,
            "circle_button_2": self.circle_button,
            "triangle_button_2": self.triangle_button,
            "square_button_2": self.square_button,
            "down_button_2": self.down_button,
            "up_button_2": self.up_button,
            "right_button_2": self.right_button,
            "left_button_2": self.left_button,
            "r1_button_2": self.r1_digital,
            "l1_button_2": self.l1_digital,
            "r2_analog_2": self.r2_analog,
            "l2_analog_2": self.l2_analog,
            "r3_button_2": self.r3_button,
            "l3_button_2": self.l3_button,
            "r_joystick_x_analog_2": self.r_stick_x,
            "l_joystick_x_analog_2": self.l_stick_x,
            "r_joystick_y_analog_2": self.r_stick_y,
            "l_joystick_y_analog_2": self.l_stick_y,
            "share_button_2": self.share_button,
            "options_button_2": self.options_button,
            "ps_symbol_button_2": self.ps_button
        }

    def process_input(self, input_object):
        output_object = self.input_map.get(input_object.name)
        if output_object is None:
            return
        input_value = input_object.value

        [out_channels, out_pulse] = output_object.get_output(input_value)

        print(input_object.name + ": " + str(input_value))
        print([out_channels, out_pulse])

        for i in range(output_object.get_num_channels()):
            self.servoBoard.setTarget(out_channels[i], int(out_pulse[i]))
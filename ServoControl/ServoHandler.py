from DigitalOutputObject import DigitalOutputObject
from AnalogOutputObject import AnalogOutputObject
import maestro

class ServoHandler:
    def __init__(self):
        self.servoBoard = maestro.Controller()
        # TODO: Multi-input object?
        self.right_ear = DigitalOutputObject("right ear", 1, [0])
        # TODO: Multi-input object?
        self.left_ear = DigitalOutputObject("left ear", 1, [1])
        self.top_eyelids = AnalogOutputObject("top eyelids", 1, [2])
        self.bottom_eyelids = AnalogOutputObject("bottom eyelids", 1, [3])
        self.eyes_horizontal = AnalogOutputObject("eyes horizontal", 2, [5, 7])
        self.eyes_vertical = AnalogOutputObject("eyes vertical", 2, [4, 6])
        # TODO: Create object for eyebrows to take 2 inputs and have 4 outputs
        self.eyebrows = AnalogOutputObject("eyebrows", 4, [8, 9, 10, 11])
        self.nose = DigitalOutputObject("nose", 1, [12])
        self.top_lip = DigitalOutputObject("top lip", 1, [13])
        # TODO: Multi-input object?
        self.left_lip = DigitalOutputObject("left lip", 2, [14, 15])
        # TODO: Multi-input object?
        self.right_lip = DigitalOutputObject("right lip", 2, [16, 17])
        # TODO: Determine if second mouth servo will be controlled
        self.jaw = AnalogOutputObject("jaw", 1, [18])
        # TODO: Create object for neck to take 3 inputs and have 3 outputs
        self.neck = AnalogOutputObject("neck", 3, [20, 21, 22])

        # TODO: Create map for input objects
        self.input_map = {
            "x_button_1": self.right_ear,
            "circle_button_1": self.right_ear,
            "triangle_button_1": self.nose,
            "square_button_1": None,
            "down_button_1": self.left_ear,
            "up_button_1": None,
            "right_button_1": None,
            "left_button_1": self.left_ear,
            "r1_button_1": None,
            "l1_button_1": None,
            "r2_analog_1": self.bottom_eyelids,
            "l2_analog_1": self.top_eyelids,
            "r3_button_1": None,
            "l3_button_1": None,
            "r_joystick_x_analog_1": self.eyebrows,
            "l_joystick_x_analog_1": self.eyes_horizontal,
            # "r_joystick_y_analog_1": self.eyebrows,
            "l_joystick_y_analog_1": self.eyes_vertical,
            "share_button_1": None,
            "options_button_1": None,
            "ps_symbol_button_1": None,

            "x_button_2": self.right_lip,
            "circle_button_2": self.right_lip,
            "triangle_button_2": None,
            "square_button_2": None,
            "down_button_2": self.left_lip,
            "up_button_2": None,
            "right_button_2": None,
            "left_button_2": self.left_lip,
            "r1_button_2": None,
            "l1_button_2": self.top_lip,
            # "r2_analog_2": self.neck,
            # "l2_analog_2": self.neck,
            "r3_button_2": None,
            "l3_button_2": None,
            "r_joystick_x_analog_2": None,
            # "l_joystick_x_analog_2": self.neck,
            "r_joystick_y_analog_2": self.jaw,
            "l_joystick_y_analog_2": self.neck,
            "share_button_2": None,
            "options_button_2": None,
            "ps_symbol_button_2": None
        }

    def process_input(self, input_object):
        # TODO: Document method
        output_object = self.input_map.get(input_object.name)
        if output_object is None:
            return
        input_value = input_object.value

        [out_channels, out_pulse] = output_object.get_output(input_value)

        print(input_object.name + ": " + str(input_value))
        print([out_channels, out_pulse])

        for i in range(output_object.get_num_channels()):
            self.servoBoard.setTarget(out_channels[i], int(out_pulse[i]))
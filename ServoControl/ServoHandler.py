from DigitalOutputObject import DigitalOutputObject
from AnalogOutputObject import AnalogOutputObject
from EyebrowsOutput import EyebrowsOutput
from NeckTiltOutput import NeckTiltOutput
from AnalogMixerOutput import AnalogMixerOutput
import maestro

class ServoHandler:
    def __init__(self):
        self.servoBoard = maestro.Controller()
        # Put both ears on L2-1 and top&bottom eyelids on R2-1?
        # TODO: Multi-input object?
        self.right_ear = AnalogOutputObject("right ear", 1, [0])
        # TODO: Multi-input object?
        self.left_ear = AnalogOutputObject("left ear", 1, [1])
        self.eyelids = AnalogOutputObject("top", 2, [2, 3])
        self.eyelids.set_outputs([5750, 6250], [7000, 5000], [4000, 8000])
        self.eyes_horizontal = AnalogOutputObject("eyes horizontal", 2, [5, 7])
        self.eyes_horizontal.set_outputs([5000, 5000], [7000, 7000], [6000, 6000])
        self.eyes_vertical = AnalogOutputObject("eyes vertical", 2, [4, 6])
        self.eyes_vertical.set_outputs([5000, 5000], [7000, 7000], [6000, 6000])
        # self.eyebrows = AnalogOutputObject("eyebrows", 4, [8, 9, 10, 11])
        # self.eyebrows.set_outputs([8000, 8000, 4000, 4000],[4000, 4000, 8000, 8000],[6000, 6000, 6000, 6000])
        self.eyebrows = EyebrowsOutput("eyebrows", 4, [8, 9, 10, 11], ["r_joystick_y_analog_1", "r_joystick_x_analog_1"])
        self.eyebrows.set_outputs([4000, 8000, 4000, 8000],[8000, 4000, 8000, 4000],[6000, 6000, 6000, 6000])
        self.nose = DigitalOutputObject("nose", 1, [12])
        self.nose.set_outputs([2000, 2000], [4000, 4000], [4000, 4000])
        self.top_lip = DigitalOutputObject("top lip", 1, [13])
        self.top_lip.set_outputs([6050], [4800], [4800])
        # TODO: Multi-input object?
        self.left_lip = DigitalOutputObject("left lip", 2, [14, 15])
        # TODO: Multi-input object?
        self.right_lip = DigitalOutputObject("right lip", 2, [16, 17])
        self.right_lip.set_outputs([4000, 4000], [8000, 8000], [6000, 6000])
        self.jaw = AnalogOutputObject("jaw", 2, [18, 19])
        self.jaw.set_outputs([8000, 4000], [6000, 6000], [4000, 8000])
        # self.neck_twist = AnalogMixerOutput("neck twist", 1, [20], ["r_joystick_x_analog_2", "r_joystick_y_analog_2"])
        self.neck_twist = AnalogOutputObject("neck twist", 1, [20])
        self.neck_tilt = NeckTiltOutput("neck tilt", 2, [21, 22], ["l_joystick_x_analog_2", "l_joystick_y_analog_2"])

        self.input_map = {
            "x_button_1": None,
            "circle_button_1": None,
            "triangle_button_1": None,
            "square_button_1": None,
            "down_button_1": None,
            "up_button_1": None,
            "right_button_1": None,
            "left_button_1": None,
            "r1_button_1": self.nose,
            "l1_button_1": None,
            "r2_analog_1": self.right_ear,
            "l2_analog_1": self.left_ear,
            "r3_button_1": None,
            "l3_button_1": None,
            "r_joystick_x_analog_1": self.eyebrows,
            "r_joystick_y_analog_1": self.eyebrows,
            "l_joystick_x_analog_1": self.eyes_horizontal,
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
            "r2_analog_2": self.jaw,
            "l2_analog_2": self.eyelids,
            "r3_button_2": None,
            "l3_button_2": None,
            "r_joystick_x_analog_2": self.neck_twist,
            "r_joystick_y_analog_2": None,
            "l_joystick_x_analog_2": self.neck_tilt,
            "l_joystick_y_analog_2": self.neck_tilt,
            "share_button_2": None,
            "options_button_2": None,
            "ps_symbol_button_2": None
        }

    def process_input(self, input_object):
        # TODO: Document method
        input_name = input_object.name
        output_object = self.input_map.get(input_name)
        if output_object is None:
            return
        input_value = input_object.value

        [out_channels, out_pulse] = output_object.get_output( input_name, input_value)

        # print( input_name + ": " + str(input_value))
        # print([out_channels, out_pulse])

        for i in range(output_object.get_num_channels()):
            self.servoBoard.setTarget(out_channels[i], int(out_pulse[i]))
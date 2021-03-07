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

    def process_input(self, input_object):
        # TODO: Create method and document
        pass
    
    # def move_servos(self, outputs):
    #         channels = outputs[0]
    #         positions = outputs[1]
    #         for i in range(len(channels)):
    #             self.servo.setTarget(channels[i],positions[i])
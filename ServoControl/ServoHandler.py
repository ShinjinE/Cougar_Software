from DigitalOutputObject import *
from AnalogOutputObject import *
# import maestro

class ServoHandler:
    def __init__(self):
        self.fake
    #     self.servo = maestro.Controller()
    
    # def move_servos(self, outputs):
    #         channels = outputs[0]
    #         positions = outputs[1]
    #         for i in range(len(channels)):
    #             self.servo.setTarget(channels[i],positions[i])

if __name__ == "__main__" :
    left_ear = AnalogOutputObject('left ear', 1)
    left_ear.set_control_direct()
    left_ear.set_outputs([4], [8000], [4000])
    print(left_ear.get_output(0.5))
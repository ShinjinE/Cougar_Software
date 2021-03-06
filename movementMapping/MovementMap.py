from DigitalOutputObject import DigitalOutputObject
from AnalogOutputObject import AnalogOutputObject
from EarOutput import EarOutput
from EyebrowsOutput import EyebrowsOutput
from SideLipOutput import SideLipOutput
from NeckTiltOutput import NeckTiltOutput
# from AnalogMixerOutput import AnalogMixerOutput
import maestro
from time import sleep

class MovementMap:
    """
    A class that handles controller inputs. Contains a mapping of input 
    objects to output objects.

    ...

    :Attributes:
        * **servoBoard**\ (\ *maestro.Controller*\ ) -- object that 
          establishes serial conection to the Maestro and has functions 
          to send commands to the board
        * **output_objects**\ (\ *[OutputObject]*\ ) -- list of all the 
          output objects, used to activate each output on the Maestro 
          board on startup
        * **right_ear**\ (\ *AnalogOutputObject*\ ) -- object to map 
          inputs to output for the right ear movements
        * **left_ear**\ (\ *AnalogOutputObject*\ ) -- object to map 
          inputs to output for the left ear movements
        * **eyelids**\ (\ *AnalogOutputObject*\ ) -- object to map input 
          to outputs for the top and bottom eyelid movements
        * **eyes_horizontal**\ (\ *AnalogOutputObject*\ ) -- object to 
          map input to outputs for the left and right eye horizontal 
          movements
        * **eyes_vertical**\ (\ *AnalogOutputObject*\ ) -- object to map 
          input to outputs for the left and right eye vertical movements
        * **eyebrows**\ (\ *EybrowsOutput*\ ) -- object to map inputs to 
          outputs for the eyebrow movements
        * **nose**\ (\ *DigitalOutputObject*\ ) -- object to map input to 
          output for the nose movements
        * **top_lip**\ (\ *DigitalOutputObject*\ ) -- object to map input 
          to output for the top lip movements
        * **right_lip**\ (\ *SideLipOutput*\ ) -- object to map inputs to 
          outputs for the right lip movements
        * **left_lip**\ (\ *SideLipOutput*\ ) -- object to map inputs to 
          outputs for the left lip movements
        * **jaw**\ (\ *AnalogOutputObject*\ ) -- object to map input to 
          outputs for the jaw movements
        * **neck_twist**\ (\ *AnalogOutputObject*\ ) -- object to map input 
          to output for the neck twist movements
        * **neck_tilt**\ (\ *NeckTiltOutput*\ ) -- object to map inputs to 
          outpus for the neck tilt movements
        * **input_map**\ (\ *dictionary [input_name (string): output_object 
          (OutputObject)]*\ ) -- mapping of the controller inputs to movement 
          outputs
    
    ...

    **Methods**

    """

    def __init__(self):
        """
        Class constructor. Creates needed output objects and sets their parameters. Also 
        creates the input map.

        """
        # Create connection to Maestro
        # If connection fails, unplug and replug the USB cable, then run code again
        self.servoBoard = maestro.Controller()

        # List to store each output object in
        self.output_objects = []

        # Right Ear
        self.right_ear = EarOutput("right ear", 1, [0], ["x_button_1", "circle_button_1"])
        self.right_ear.set_outputs([4000], [4000], [8000])
        self.output_objects.append(self.right_ear)

        # Left Ear
        self.left_ear = EarOutput("left ear", 1, [1], ["down_button_1", "left_button_1"])
        self.left_ear.set_outputs([4000], [4000], [8000])
        self.output_objects.append(self.left_ear)

        # Eyelids
        self.eyelids = AnalogOutputObject("eylids", 2, [2, 3])
        self.eyelids.set_outputs([6800, 5300], [6800, 5300], [6050, 6550])
        self.output_objects.append(self.eyelids)

        # Horizontal Eye Movement
        self.eyes_horizontal = AnalogOutputObject("eyes horizontal", 2, [5, 7])
        lh_eye_offset = 500 # Positive moves left
        rh_eye_offset = 600 # Positive moves left
        self.eyes_horizontal.set_outputs([7000+lh_eye_offset, 7000+rh_eye_offset], [6000+lh_eye_offset, 6000+rh_eye_offset], [5000+lh_eye_offset, 5000+rh_eye_offset])
        self.output_objects.append(self.eyes_horizontal)
        
        # Vertical Eye Movement
        self.eyes_vertical = AnalogOutputObject("eyes vertical", 2, [4, 6])
        lv_eye_offset = 500 # Positive moves up
        rv_eye_offset = 400 # Positive moves up
        self.eyes_vertical.set_outputs([7000+lv_eye_offset, 7000+rv_eye_offset], [6000+lv_eye_offset, 6000+rv_eye_offset], [5000+lv_eye_offset, 5000+rv_eye_offset])
        self.output_objects.append(self.eyes_vertical)

        # Eyebrows
        self.eyebrows = EyebrowsOutput("eyebrows", 4, [8, 9, 10, 11], ["r_joystick_y_analog_1", "r_joystick_x_analog_1"])
        self.eyebrows.set_outputs([8000, 8000, 4000, 4000], [6000, 6000, 6000, 6000], [4000, 4000, 8000, 8000])
        self.output_objects.append(self.eyebrows)

        # Nose
        self.nose = DigitalOutputObject("nose", 1, [12])
        self.nose.set_outputs([4000, 4000], [4000, 4000], [2000, 2000])
        self.output_objects.append(self.nose)

        # Top Lip
        self.top_lip = DigitalOutputObject("top lip", 1, [13])
        self.top_lip.set_outputs([4800], [4800], [6050])
        self.output_objects.append(self.top_lip)

        # Right Lip
        self.right_lip = SideLipOutput("right lip", 2, [14, 15], ["circle_button_2", "x_button_2"])
        self.right_lip.set_outputs([6500, 5000], [6000, 6000], [5500, 7000])
        self.output_objects.append(self.right_lip)
        
        # Left Lip
        self.left_lip = SideLipOutput("left lip", 2, [16, 17], ["left_button_2", "down_button_2"])
        self.left_lip.set_outputs([5500, 7000], [6000, 6000], [6500, 5000])
        self.output_objects.append(self.left_lip)

        # Jaw
        self.jaw = AnalogOutputObject("jaw", 2, [18, 19])
        self.jaw.set_outputs([6000, 6000], [6000, 6000], [7000, 5000])
        self.output_objects.append(self.jaw)

        # Neck Twist (Look left and right)
        self.neck_twist = AnalogOutputObject("neck twist", 1, [20])
        self.neck_twist.set_outputs([8000], [6000], [4000])
        self.output_objects.append(self.neck_twist)

        # Neck Tilt (Forward and backward, side to side)
        self.neck_tilt = NeckTiltOutput("neck tilt", 2, [21, 22], ["l_joystick_x_analog_2", "l_joystick_y_analog_2"])
        tilt_offset = 500 # Positive moves up
        self.neck_tilt.set_outputs([3000, 3000+tilt_offset], [6000, 6000+tilt_offset], [9000, 9000+tilt_offset])
        self.output_objects.append(self.neck_tilt)

        # Dictionary that maps inputs to the correlated output object
        # The key to the dictionary is the string name of the controller input
        # The value of the dictionary is the output object to send the input value to
        # If an input is not mapped to any output, the value for the dictionary is set to None
        self.input_map = {
            # Input mapping for controller 1
            "x_button_1": self.right_ear,
            "circle_button_1": self.right_ear,
            "triangle_button_1": None,
            "square_button_1": None,
            "down_button_1": self.left_ear,
            "up_button_1": None,
            "right_button_1": None,
            "left_button_1": self.left_ear,
            "r1_button_1": self.nose,
            "l1_button_1": None,
            "r2_analog_1": None,
            "l2_analog_1": self.eyelids,
            "r3_button_1": None,
            "l3_button_1": None,
            "r_joystick_x_analog_1": self.eyebrows,
            "r_joystick_y_analog_1": self.eyebrows,
            "l_joystick_x_analog_1": self.eyes_horizontal,
            "l_joystick_y_analog_1": self.eyes_vertical,
            "share_button_1": None,
            "options_button_1": None,
            "ps_symbol_button_1": None,

            # Input mapping for controller 2
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
            "l2_analog_2": None,
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

        # Start outputting to the Maestro board using starting positions
        self.start_outputs()

    def send_outputs(self, num_outputs, channel, output):
        """
        Sends the output to the corresponding channel from the given lists of channels and
        outputs.

        :param num_outputs: number of channels and outputs to loop through
        :param channel: channel numbers on the Maestro board to send outputs to
        :param output: values to output on the Maestro board, cast to int to ensure proper
            typing
        :type num_outputs: int
        :type channel: [int]
        :type output: [double]

        """
        for i in range(num_outputs):
            self.servoBoard.setTarget(channel[i], int(output[i]))

    def process_input(self, input_object):
        """
        Using the input map, determines the correct output object to send the input value to. 
        The returned outputs are passed to the maestro board.

        :param input_object: object containing the name of the input and its associated value 
            to be processed
        :type input_object: ControllerEvent

        """
        # Get info about input
        input_name = input_object.name
        output_object = self.input_map.get(input_name)

        # If the input is not linked to an output, do nothing
        if output_object is None:
            return
        input_value = input_object.value

        # Process the input
        [out_channels, out_pulse] = output_object.get_output(input_name, input_value)

        # print( input_name + ": " + str(input_value))
        # print([out_channels, out_pulse])

        # Send outputs to Maestro
        self.send_outputs(output_object.get_num_channels(), out_channels, out_pulse)

    def start_outputs(self):
        """
        Sends the starting outputs for each motor to the Maestro board to activate each channel
         in default positions.

        """
        # Time to delay between activating servo groups
        # Total time to activate is about 1 second for all 13 groups
        sleep_sec = 1.0/13.0

        # Loop to activate each movement group
        for output_object in self.output_objects:
            [out_channels, out_pulse] = output_object.get_default_outputs()
            self.send_outputs(output_object.get_num_channels(), out_channels, out_pulse)
            sleep(sleep_sec)
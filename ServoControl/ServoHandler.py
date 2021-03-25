from DigitalOutputObject import DigitalOutputObject
from AnalogOutputObject import AnalogOutputObject
# from EarOutput import EarOutput
from EyebrowsOutput import EyebrowsOutput
from SideLipOutput import SideLipOutput
from NeckTiltOutput import NeckTiltOutput
# from AnalogMixerOutput import AnalogMixerOutput
import maestro

class ServoHandler:
    """
    A class that handles controller inputs. Contains a mapping of input objects to output objects.

    ...

    Attributes
    ----------
    # TODO: Add all output members
    servoBoard : maestro.Controller
        object that establishes serial conection to the Maestro and has functions to send commands to the board
    # TODO: Change to a dictionary of each channel and it's default output so sequential startup can match relays
    output_objects : [OutputObject]
        list of all the output objects, used to activate each output on the Maestro board on startup
    right_ear : AnalogOutputObject
        object to map inputs to output for the right ear movements
    left_ear : AnalogOutputObject
        object to map inputs to output for the left ear movements
    eyelids : AnalogOutputObject
        object to map input to outputs for the top and bottom eyelid movements
    eyes_horizontal : AnalogOutputObject
        object to map input to outputs for the left and right eye horizontal movements
    eyes_vertical : AnalogOutputObject
        object to map input to outputs for the left and right eye vertical movements
    eyebrows : EybrowsOutput
        object to map inputs to outputs for the eyebrow movements
    nose : DigitalOutputObject
        object to map input to output for the nose movements
    top_lip : DigitalOutputObject
        object to map input to output for the top lip movements
    right_lip : SideLipOutput
        object to map inputs to outputs for the right lip movements
    left_lip : SideLipOutput
        object to map inputs to outputs for the left lip movements
    jaw : AnalogOutputObject
        object to map input to outputs for the jaw movements
    neck_twist : AnalogOutputObject
        object to map input to output for the neck twist movements
    neck_tilt : NeckTiltOutput
        object to map inputs to outpus for the neck tilt movements
    input_map : dictionary [input_name (string): output_object (OutputObject)]
        mapping of the controller inputs to movement outputs

    Methods
    -------
    __init_():
        Class constructor. Creates needed output objects and sets their parameters. Also creates the input map.
    send_outputs(num_outputs, channel, output):
        Sends the output to the corresponding channel from the given lists of channels and outputs.
    process_input(input_object):
        Using the input map, determines the correct output object to send the input value to. The returned outputs are passed to the maestro board.
    start_outputs():
        Sends the starting outputs for each motor to the Maestro board to activate each channel in default positions.
    """

    def __init__(self):
        """
        Class constructor. Creates needed output objects and sets their parameters. Also creates the input map.

        Parameters
        ----------
        None
        """
        # Create connection to Maestro
        # If connection fails, unplug and replug the USB cable, then run code again
        self.servoBoard = maestro.Controller()

        # List to store each output object in
        self.output_objects = []

        # TODO: Put ears on left&down and x&circle, with top&bottom eyelids on L2-1

        # TODO: Set ears to move like side lips
        self.right_ear = AnalogOutputObject("right ear", 1, [0])
        self.output_objects.append(self.right_ear)

        # TODO: Set ears to move like side lips
        self.left_ear = AnalogOutputObject("left ear", 1, [1])
        self.output_objects.append(self.left_ear)

        self.eyelids = AnalogOutputObject("eylids", 2, [2, 3])
        self.eyelids.set_outputs([6500, 5000], [6500, 5000], [5750, 6250])
        self.output_objects.append(self.eyelids)

        self.eyes_horizontal = AnalogOutputObject("eyes horizontal", 2, [5, 7])
        self.eyes_horizontal.set_outputs([7000, 7000], [6000, 6000], [5000, 5000])
        self.output_objects.append(self.eyes_horizontal)

        self.eyes_vertical = AnalogOutputObject("eyes vertical", 2, [4, 6])
        self.eyes_vertical.set_outputs([7000, 7000], [6000, 6000], [5000, 5000])
        self.output_objects.append(self.eyes_vertical)

        self.eyebrows = EyebrowsOutput("eyebrows", 4, [8, 9, 10, 11], ["r_joystick_y_analog_1", "r_joystick_x_analog_1"])
        self.eyebrows.set_outputs([8000, 4000, 8000, 4000], [6000, 6000, 6000, 6000], [4000, 8000, 4000, 8000])
        self.output_objects.append(self.eyebrows)

        self.nose = DigitalOutputObject("nose", 1, [12])
        self.nose.set_outputs([4000, 4000], [4000, 4000], [2000, 2000])
        self.output_objects.append(self.nose)

        self.top_lip = DigitalOutputObject("top lip", 1, [13])
        self.top_lip.set_outputs([4800], [4800], [6050])
        self.output_objects.append(self.top_lip)

        self.right_lip = SideLipOutput("right lip", 2, [14, 15], ["circle_button_2", "x_button_2"])
        self.right_lip.set_outputs([6500, 5000], [6000, 6000], [5500, 7000])
        self.output_objects.append(self.right_lip)
        
        self.left_lip = SideLipOutput("left lip", 2, [16, 17], ["left_button_2", "down_button_2"])
        self.left_lip.set_outputs([5500, 7000], [6000, 6000], [6500, 5000])
        self.output_objects.append(self.left_lip)

        self.jaw = AnalogOutputObject("jaw", 2, [18, 19])
        self.jaw.set_outputs([6000, 6000], [6000, 6000], [7000, 5000])
        self.output_objects.append(self.jaw)

        self.neck_twist = AnalogOutputObject("neck twist", 1, [20])
        self.neck_twist.set_outputs([8000], [6000], [4000])
        self.output_objects.append(self.neck_twist)

        self.neck_tilt = NeckTiltOutput("neck tilt", 2, [21, 22], ["l_joystick_x_analog_2", "l_joystick_y_analog_2"])
        offset = 500
        self.neck_tilt.set_outputs([3000, 3000+offset], [6000, 6000+offset], [9000, 9000+offset])
        self.output_objects.append(self.neck_tilt)

        # Dictionary that maps inputs to the correlated output object
        # The key to the dictionary is the string name of the controller input
        # The value of the dictionary is the output object to send the input value to
        # If an input is not mapped to any output, the value for the dictionary is set to None
        self.input_map = {
            # Input mapping for controller 1
            # TODO: Put right ear on x and circle
            "x_button_1": None,
            "circle_button_1": None,
            "triangle_button_1": None,
            "square_button_1": None,
            # TODO: Put left ear on down and left
            "down_button_1": None,
            "up_button_1": None,
            "right_button_1": None,
            "left_button_1": None,
            "r1_button_1": self.nose,
            "l1_button_1": None,
            "r2_analog_1": self.right_ear,
            # TODO: Put eyelids on L2
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
            # TODO: Put eyelids on L2-1
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

        # TODO: Uncomment this to activate Maestro when program begins
        # # Start outputting to the Maestro board using starting positions
        # self.start_outputs()

    def send_outputs(self, num_outputs, channel, output):
        """
        Sends the output to the corresponding channel from the given lists of channels and outputs.

        Parameters
        ----------
        num_outputs : int
            number of channels and outputs to loop through
        channel : [int]
            channel numbers on the Maestro board to send outputs to
        output : [double]
            values to output on the Maestro board, cast to int to ensure proper typing

        Returns
        -------
        None
        """
        for i in range(num_outputs):
            self.servoBoard.setTarget(channel[i], int(output[i]))

    def process_input(self, input_object):
        """
        Using the input map, determines the correct output object to send the input value to. The returned outputs are passed to the maestro board.

        Parameters
        ----------
        input_object : ControllerEvent
            object containing the name of the input and its associated value to be processed

        Returns
        -------
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
        Sends the starting outputs for each motor to the Maestro board to activate each channel in default positions.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        for output_object in self.output_objects:
            [out_channels, out_pulse] = output_object.get_default_outputs()
            self.send_outputs(output_object.get_num_channels(), out_channels, out_pulse)

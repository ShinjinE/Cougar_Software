=========================
Changing the Movement Map
=========================

The movement mapping code is constructed in a way to be easily adaptable. 
For example, if the number of servos used in a movement group change, this 
can be adjusted using the concepts discussed in :ref:`pyrange`. The two 
main areas of interest that could be changed are if a movement group is 
added, changed, or removed, and the way inputs are mapped to outputs need 
to be changed.

.. note:: This section assumes familiarity with Python classes and objects.

Movement Groups
===============

The output objects are designed to easily have the following attributes 
changed:

1. Number of output channels
2. Which output channels to use
3. Min, default, and max output values
4. Correlated PS4 input(s)

**Attributes 1 and 2**

These attributes are always set using the constructor of the object. 
The following example has the "jaw" movement sending outputs on two 
channels. These channels are 18 and 19.

.. code-block:: python

    self.jaw = AnalogOutputObject("jaw", 2, [18, 19])

**Attribute 3**

This attribute is always dependant on the *set_outputs* method that each 
output object class inherits. This was already discussed in the section, 
:ref:`pyrange`. However, here is an example of the method being used.

.. code-block:: python

    self.jaw.set_outputs([6000, 6000], [6000, 6000], [7000, 5000])

**Attribute 4**

This attribute is mostly determined by an attribute of the MovementMap 
class called *input_map*\ . This MovementMap attribute is a python 
dictionary that links input names from the two PS4 controllers to the 
movement groups they control. This enables the MovementMap class to pass 
the inputs to the correct output objects quickly based on the input name.

The following is the mapping for the first controller:

.. code-block:: python

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
    "ps_symbol_button_1": None

For the dictionary keys that have a value of *None*, those inputs 
don't control anything on Cosmotron and will be ignored by the 
MovementMap class. To make a new mapping between a PS4 input and an 
movement group, replace *None* with the corresponding output object.
To remove a mapping, change the value for the input key to *None*. 
To change a currently used mapping, change the output object in the 
value to the output object for the desired movement group.

There is a secondary place where attribute 4 is set. This is in the 
constructor for some of the more complex output objects, like the 
eyebrows. These output object determine their output based off of 
two PS4 inputs. These output objects take an additional parameter in 
their constructor. This parameter is a list of the input names. The 
order of this list matters. To see how to order the list, look at 
the code for the corresponding output object.

.. note:: These complex objects that use multiple PS4 inputs need to 
    have the input names passed into their constructor be the same 
    as the key-value pairs set be the *input_map* attribute.

Here is the constructor being called for the eyebrow output object 
as an example:

.. code-block:: python

    self.eyebrows = EyebrowsOutput("eyebrows", 4, [8, 9, 10, 11], ["r_joystick_y_analog_1", "r_joystick_x_analog_1"])
     
Notice how in the section of the *input_map* attribute shown above, 
the object, *eyebrows*, is associated with "r_joystick_y_analog_1" 
and "r_joystick_x_analog_1", which are the same input names passed 
into the constructor for the eyebrows movement group.

Output Mapping
==============

Currently each output object class has a linear mapping of inputs 
to outputs. The following is the default mapping equation:

``output_value = (input_value - input_min) * (out_max - out_min) / (input_max - input_min) + out_min``

Out max and min are set by the *set_outputs* method for the output 
object. Input max and min are dependant on whether the output object 
accepts a digital or analog input. For digital, the max is 1 and the 
min is 0. For analog, the max is 255 and the min is 0. Input value is 
the value associated with the corresponding PS4 input being processed.
The output value is what is sent to the Maestro board.

For the output objects that take multiple PS4 inputs, this linear 
mapping is not changed. However, the mixing of inputs is done before 
the input value is sent to the mapping equation.

To change this mapping to follow an exponential growth or decay, or 
any other behavior, it is recommended to create a new output object 
for the desired movement group which inherits from the object that 
movement group was previously set to. Then overide the *map_values* 
method which contains the mapping equation. In the overidden method, 
create the new desired mapping equation. This will enable custom 
mappings to be set without changing the behavior of the other 
movement groups.
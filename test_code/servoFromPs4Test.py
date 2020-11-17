import time
import adafruit_pca9685
import busio
import board
from adafruit_servokit import ServoKit
import pygame

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class TextPrint(object):
    """
    This is a simple class that will help us print to the screen
    It has nothing to do with the joysticks, just outputting the
    information.
    """

    def __init__(self):
        """ Constructor """
        self.reset()
        self.x_pos = 10
        self.y_pos = 10
        self.font = pygame.font.Font(None, 20)

    def print(self, my_screen, text_string):
        """ Draw text onto the screen. """
        text_bitmap = self.font.render(text_string, True, BLACK)
        my_screen.blit(text_bitmap, [self.x_pos, self.y_pos])
        self.y_pos += self.line_height

    def reset(self):
        """ Reset text to the top of the screen. """
        self.x_pos = 10
        self.y_pos = 10
        self.line_height = 15

    def indent(self):
        """ Indent the next line of text """
        self.x_pos += 10

    def unindent(self):
        """ Unindent the next line of text """
        self.x_pos -= 10


# init servo
i2c = busio.I2C(board.SCL, board.SDA)
hat = adafruit_pca9685.PCA9685(i2c)

hat.frequency = 50
led_channel = hat.channels[1]

kit = ServoKit(channels=16)

# init game
pygame.init()

# Set the width and height of the screen [width,height]
size = [500, 700]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("My Game")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Initialize the joysticks
pygame.joystick.init()

# Get ready to print
textPrint = TextPrint()

# set global variables
joystick = pygame.joystick.Joystick(0)
joystick.init()

xButton = joystick.get_button(0)
circleButton = joystick.get_button(1)
triangleButton = joystick.get_button(2)
squareButton = joystick.get_button(3)

# -------- Main Program Loop -----------
while not done:
    # EVENT PROCESSING STEP
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN
        # JOYBUTTONUP JOYHATMOTION
        if event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")
        if event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")

    # DRAWING STEP
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(WHITE)
    textPrint.reset()

    # Get the name from the OS for the controller/joystick
    name = joystick.get_name()
    textPrint.print(screen, "Joystick name: {}".format(name))

    # Get number of buttons
    buttons = joystick.get_numbuttons()
    textPrint.print(screen, "Number of buttons: {}".format(buttons))
    textPrint.indent()

    # Go through all buttons and do x
    for i in range(buttons):
        button = joystick.get_button(i)
        if button == xButton:
            kit.servo[0].angle = 180
            time.sleep(1)
            kit.servo[0].angle = 0
            time.sleep(1)
            kit.servo[0].angle = 90
        elif button == circleButton:
            for i in range(0x0, 0xffff, 0xf):
                led_channel.duty_cycle = i

            # Decrease brightness:
            for i in range(0xffff, 0, -0xf):
                led_channel.duty_cycle = i

        textPrint.print(screen, "Button {:>2} value: {}".format(i, button))
    textPrint.unindent()

    textPrint.unindent()

    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()

import time
import adafruit_pca9685
import busio
import board
from adafruit_servokit import ServoKit
import pygame
import numpy

# init servo
i2c = busio.I2C(board.SCL, board.SDA)
hat = adafruit_pca9685.PCA9685(i2c)

hat.frequency = 50
kit = ServoKit(channels=16)

# init game
pygame.init()

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Initialize the joysticks
pygame.joystick.init()

# set global variables
ps4 = pygame.joystick.Joystick(0)
ps4.init()

xButton = 0
circleButton = 1
triangleButton = 2
squareButton = 3

# Get the name from the OS for the controller/joystick
gamepadName = ps4.get_name()
print("Joystick name: {}".format(gamepadName))

# Usually axis run in pairs, up/down for one, and left/right for
# the other.
numAxes = ps4.get_numaxes()
print("Number of axes: {}".format(numAxes))

# Get number of buttons
numButtons = ps4.get_numbuttons()
print("Number of buttons: {}".format(numButtons))

listenAxis = True
isMacroA = False
isMacroB = False

# -------- Main Program Loop -----------
try:
    while not done:
        # EVENT PROCESSING STEP
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN
            # JOYBUTTONUP JOYHATMOTION
            if event.type == pygame.JOYBUTTONDOWN:
                if ps4.get_button(xButton) == 1:
                    print("X button pressed.")
                    isMacroA = not isMacroA
                    if isMacroA:
                        isMacroB = False
                        kit.servo[0].angle = 180
                elif ps4.get_button(circleButton) == 1:
                    print("Circle button pressed.")
                    isMacroB = not isMacroB
                    if isMacroB:
                        isMacroA = False
                        kit.servo[0].angle = 0
            if event.type == pygame.JOYBUTTONUP:
                print("Button released.")

        if not (isMacroA or isMacroB):
            manualAngle = ps4.get_axis(1)
            kit.servo[0].angle = numpy.interp(manualAngle,[-1,1],[0,180])
        # Limit to 60 frames per second
        clock.tick(60)

except KeyboardInterrupt:
    print("EXITING NOW")

# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()

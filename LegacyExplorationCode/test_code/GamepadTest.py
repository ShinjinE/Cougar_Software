import pygame

pygame.init()
pygame.joystick.init()

joystickCount = pygame.joystick.get_count()
print("Num Joysticks available: {}".format(joystickCount))

for i in range(joystickCount):
    joystick = pygame.joystick.Joystick(i)
    joystick.init()
    print("Joystick {}".format(i))
    
    name = joystick.get_name()
    print("\tName: {}".format(name))
    
    axes = joystick.get_numaxes()
    print("\tNum of axes: {}".format(axes))
    
    for i in range(axes):
        axis = joystick.get_axis(i)
        print("\t\tAxis {} value: {:>6.3f}".format(i,axis))
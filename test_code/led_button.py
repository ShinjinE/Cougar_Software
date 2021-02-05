# from gpiozero import LED
# from gpiozero import Button

# led = LED(17)
# button = Button(27,pull_up = False)

# while True:
#     if button.is_active:
#         led.on
#     else:
#         led.off
from gpiozero import LED, Button
from time import sleep
from signal import pause

led = LED(17)
button = Button(27,pull_up = False)

# while True:
#     led.on()
#     sleep(1)
#     led.off()
#     sleep(1)
# button.wait_for_press()
# led.on()
# sleep(3)
# led.off()
button.when_pressed = led.on
button.when_released = led.off

pause()
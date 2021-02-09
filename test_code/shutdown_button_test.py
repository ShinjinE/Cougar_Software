from gpiozero import Button, LED
from subprocess import check_call
from signal import pause

def shutdown():
    buttonLed.off()
    powerLed.blink()
    check_call(['sudo', 'poweroff'])

buttonLed = LED(27)
powerLed = LED(22)
shutdown_btn = Button(17, hold_time=3)

shutdown_btn.when_pressed = buttonLed.on
shutdown_btn.when_released = buttonLed.off
shutdown_btn.when_held = shutdown

powerLed.on()

pause()
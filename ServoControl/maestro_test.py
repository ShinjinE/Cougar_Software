from ServoHandler import ServoHandler, DigitalOutputObject, AnalogOutputObject
from time import sleep

servoHandler = ServoHandler()
inputTestDigital = DigitalOutputObject('test digital', 2, [0, 1])
inputTestDigital.set_outputs([8000, 4000],[4000, 8000])
inputTestAnalog = AnalogOutputObject('test analog', 2, [0, 1])
inputTestAnalog.set_outputs([8000, 4000],[4000, 8000])

for x in [False, True]:
    print("Digital: " + str(x))
    [out_channels, out_pulse] = inputTestDigital.get_output(x) 
    print([out_channels, out_pulse])
    for i in range(inputTestDigital.get_num_channels()):
        servoHandler.servoBoard.setTarget(out_channels[i], int(out_pulse[i]))
    sleep(.5)

sleep(.5)

for x in [-1, -.5, 0, .5, 1]:
    print("Analog: " + str(x))
    [out_channels, out_pulse] = inputTestAnalog.get_output(x) 
    print([out_channels, out_pulse])
    for i in range(inputTestAnalog.get_num_channels()):
        servoHandler.servoBoard.setTarget(out_channels[i], int(out_pulse[i]))
    sleep(.5)

servoHandler.servoBoard.close()
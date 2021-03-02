import maestro
from time import sleep

servoBoard = maestro.Controller()

smallServo = 0
largeServo = 1
rangeMin = 1000*4
rangeMax = 2000*4
currPosSmall = rangeMin
currPosLarge = rangeMax
for x in range(5):
    while currPosSmall < rangeMax:
        servoBoard.setTarget(smallServo,currPosSmall)
        servoBoard.setTarget(largeServo,currPosLarge)
        currPosSmall += 1
        currPosLarge -= 1
        sleep(.001)
    while currPosSmall > rangeMin:
        servoBoard.setTarget(smallServo,currPosSmall)
        servoBoard.setTarget(largeServo,currPosLarge)
        currPosSmall -= 1
        currPosLarge += 1

servoBoard.close()
import maestro
from time import sleep

servo = maestro.Controller()
# servo.setAccel(0,4)      #set servo 0 acceleration to 4
# servo.setTarget(5,1792*4)  #set servo to move to center position
# sleep(1)
# servo.setTarget(5,2496*4)  #set servo to move to center position
# sleep(1)
# servo.setTarget(5,(1792+2496)*2)  #set servo to move to center position
# servo.setSpeed(1,10)     #set speed of servo 1
# x = servo.getPosition(1) #get the current position of servo 1
# print(x)

channel = 5
rangeMin = 1792*4
rangeMax = 2496*4
currPos = rangeMin
for x in range(5):
    while currPos < rangeMax:
        servo.setTarget(channel,currPos)
        currPos += 1
        sleep(.001)
    # sleep(0.5)
    while currPos > rangeMin:
        servo.setTarget(channel,currPos)
        currPos -= 1
        # sleep(.001)
servo.close()
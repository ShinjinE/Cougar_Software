from adafruit_servokit import ServoKit
import board
import busio
import adafruit_pca9685
import time
i2c = busio.I2C(board.SCL, board.SDA)
hat = adafruit_pca9685.PCA9685(i2c)

hat.frequency = 50

kit = ServoKit(channels=16)

kit.servo[0].angle = 180

time.sleep(1)

kit.servo[0].angle = 0

time.sleep(1)

kit.servo[0].angle = 90

import board
import busio
import adafruit_pca9685
i2c = busio.I2C(board.SCL, board.SDA)
hat = adafruit_pca9685.PCA9685(i2c)

hat.frequency = 60
led_channel = hat.channels[0]

# led_channel.duty_cycle = 0xffff

# led_channel.duty_cycle = 0

# led_channel.duty_cycle = 1000

for i in range(0x0, 0xffff, 0xf):
    led_channel.duty_cycle = i

# Decrease brightness:
for i in range(0xffff, 0, -0xf):
    led_channel.duty_cycle = i
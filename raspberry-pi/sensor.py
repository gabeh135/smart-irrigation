import board
import busio
from collections import deque

from adafruit_ads1x15.ads1115 import ADS1115
from adafruit_ads1x15.analog_in import AnalogIn


i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS1115(i2c)

channel = AnalogIn(ads, 0)

readings = deque(maxlen=10)


def get_moisture():
    readings.append(channel.voltage)
    return sum(readings) / len(readings)

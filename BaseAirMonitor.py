import os
import sys
import time
from serial import *


class BaseAirMonitor:
    def __init__(self, serial_device="/dev/tty.usbserial", baudrate=9600, bytesize=EIGHTBITS, parity=PARITY_NONE, stopbits=STOPBITS_ONE, timeout=1):
        self.serial_device = serial_device
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.timeout=timeout
        self.sensor_inst = Serial(self.serial_device, self.baudrate, self.bytesize, self.parity, self.stopbits, self.timeout)

    def __del__(self):
        self.sensor_inst.close()

    def get_data(self):
        pass

    def run(self, callback_fun=None, delay=1):
        while True:
            # get dict data from sensor and trigger the callback function
            callback_fun(self.get_data())
            time.sleep(1)


if __name__ == '__main__':
    pass

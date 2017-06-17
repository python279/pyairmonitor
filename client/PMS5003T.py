# -*- coding: utf-8 -*-
#
# lhq@python279.org

import pytz
import logging
from serial import *
import time
from datetime import datetime
from BaseAirMonitor import BaseAirMonitor


class PMS5003T(BaseAirMonitor):
    def __init__(self, serial_device='/dev/tty.SLAB_USBtoUART', baudrate=9600, bytesize=EIGHTBITS, parity=PARITY_NONE, stopbits=STOPBITS_ONE):
        self.serial_device = serial_device
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.sensor_inst = Serial(self.serial_device, self.baudrate, self.bytesize, self.parity, self.stopbits)
        BaseAirMonitor.__init__(self)

    def __del__(self):
        BaseAirMonitor.__del__(self)
        self.sensor_inst.close()

    def __invalid_sample_value(self, sample_data):
        max_sample = {
            'pm1.0': 500,
            'pm2.5': 500,
            'pm10': 500,
            'temperature': 100,
            'humidity': 100,
        }
        for k in max_sample.keys():
            if abs(sample_data[k] > max_sample[k]):
                return True
        return False

    def get_data(self):
        while True:
            checksum = 0
            while self.sensor_inst.read(1) != '\x42':
                pass
            checksum += 0x42
            while self.sensor_inst.read(1) != '\x4d':
                pass
            checksum += 0x4d
            length = bytearray(self.sensor_inst.read(2))
            checksum += int(length[0])
            checksum += int(length[1])
            sample = bytearray(self.sensor_inst.read(length[1]))
            sample_hex = [int(i) for i in sample]
            for i in sample_hex[0:-2]:
                checksum += i
            if checksum != sample_hex[-2]*256+sample_hex[-1]:
                continue
            sample_readable = {
                'timestamp': datetime.now().strftime('%Y%m%d%H%M%S'),
                'pm1.0': sample_hex[6]*256+sample_hex[7],
                'pm2.5': sample_hex[8]*256+sample_hex[9],
                'pm10': sample_hex[10]*256+sample_hex[11],
                'temperature': (sample_hex[20]*256+sample_hex[21])/10,
                'humidity': (sample_hex[22]*256+sample_hex[23])/10,
                'switch1': 0,
                'switch2': 1,
            }
            if self.__invalid_sample_value(sample_readable):
                continue
            return sample_readable


if __name__ == '__main__':
    timezone = pytz.timezone('Asia/Shanghai')

    def every_minute(self):
        data = self.get_data()
        print data

    sensor = PMS5003T()
    sensor.every_minute_job(every_minute)
    while True:
        time.sleep(10)


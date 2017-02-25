from serial import *
from BaseAirMonitor import BaseAirMonitor


class PMS5003T(BaseAirMonitor):
    def __init__(self, serial_device="/dev/tty.SLAB_USBtoUART", baudrate=9600, bytesize=EIGHTBITS, parity=PARITY_NONE, stopbits=STOPBITS_ONE, timeout=1):
        BaseAirMonitor.__init__(self, serial_device, baudrate, bytesize, parity, stopbits, timeout)

    def get_data(self):
        while self.sensor_inst.read(1) != '\x42':
            pass
        while self.sensor_inst.read(1) != '\x4d':
            pass
        length = bytearray(self.sensor_inst.read(2))
        sample = bytearray(self.sensor_inst.read(length[1]))
        sample_hex = [int(i) for i in sample]
        sample_readable = {
            'pm1' : sample_hex[6]*256+sample_hex[7],
            'pm2.5' : sample_hex[8]*256+sample_hex[9],
            'pm10' : sample_hex[10]*256+sample_hex[11],
            'temperature' : (sample_hex[20]*256+sample_hex[21])/10,
            'humidity' : (sample_hex[22]*256+sample_hex[23])/10,
        }
        return sample_readable

if __name__ == '__main__':
    while True:
        pms5003t = PMS5003T()
        print pms5003t.get_data()
        time.sleep(1)

# -*- coding: utf-8 -*-
#
# lhq@python279.org

import pytz
import random
from BaseAirMonitor import BaseAirMonitor


class Simulator(BaseAirMonitor):
    def __init__(self):
        BaseAirMonitor.__init__(self)

    def __del__(self):
        BaseAirMonitor.__del__(self)

    def get_data(self):
        random.seed(time.time())
        sample_readable = {
            'pm1': random.randint(30, 100),
            'pm2.5': random.randint(30, 100),
            'pm10': random.randint(30, 100),
            'temperature': random.randint(1, 50),
            'humidity': random.randint(10, 90),
        }
        return sample_readable


if __name__ == '__main__':
    import time
    timezone = pytz.timezone('Asia/Shanghai')

    def every_minute(self):
        t = int(time.time())
        data = self.get_data()
        print t, data

    sensor = Simulator()
    sensor.every_minute_job(every_minute)
    while True:
        time.sleep(10)

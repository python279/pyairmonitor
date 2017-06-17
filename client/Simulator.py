# -*- coding: utf-8 -*-
#
# lhq@python279.org

import pytz
import random
import time
from datetime import datetime
from BaseAirMonitor import BaseAirMonitor


class Simulator(BaseAirMonitor):
    def __init__(self):
        BaseAirMonitor.__init__(self)

    def __del__(self):
        BaseAirMonitor.__del__(self)

    def get_data(self):
        random.seed(time.time())
        sample_readable = {
            'timestamp': datetime.now().strftime("%Y%m%d%H%M%S"),
            'pm1.0': random.randint(30, 100),
            'pm2.5': random.randint(30, 100),
            'pm10': random.randint(30, 100),
            'temperature': random.randint(1, 50),
            'humidity': random.randint(10, 90),
            'switch1': 0,
            'switch2': 0,
        }
        return sample_readable


if __name__ == '__main__':
    timezone = pytz.timezone('Asia/Shanghai')

    def every_minute(self):
        data = self.get_data()
        print data

    sensor = Simulator()
    sensor.every_minute_job(every_minute)
    while True:
        time.sleep(10)

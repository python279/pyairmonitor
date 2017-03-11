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
            'time': datetime.now().strftime("%Y%m%d%H%M%S"),
            'pm1': random.randint(30, 100),
            'pm2.5': random.randint(30, 100),
            'pm10': random.randint(30, 100),
            'temperature': random.randint(1, 50),
            'humidity': random.randint(10, 90),
        }
        return sample_readable

    # override the every_minute_job for debug purpose, every minute -> every second
    def every_minute_job(self, callback_fun=None):
        def __every_minute_job(self):
            callback_fun(self)
        self.add_job(__every_minute_job, trigger='cron', args=(self,), id='every_minute_job_'+str(time.time()), second='*')

    # override the every_minute_job for debug purpose, every hour -> every minute
    def every_hour_job(self, callback_fun=None):
        def __every_hour_job(self):
            callback_fun(self)
        self.add_job(__every_hour_job, trigger='cron', args=(self,), id='every_hour_job_'+str(time.time()), minute='*')


if __name__ == '__main__':
    timezone = pytz.timezone('Asia/Shanghai')

    def every_minute(self):
        data = self.get_data()
        print data

    sensor = Simulator()
    sensor.every_minute_job(every_minute)
    while True:
        time.sleep(10)

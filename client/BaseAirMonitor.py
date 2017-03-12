# -*- coding: utf-8 -*-
#
# lhq@python279.org

import pytz
import time
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(5)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3
}


class BaseAirMonitor(BackgroundScheduler):
    def __init__(self):
        BackgroundScheduler.__init__(self)
        self.configure(executors=executors, job_defaults=job_defaults, timezone=pytz.timezone('Asia/Shanghai'))
        self.start()

    def __del__(self):
        self.shutdown()

    # subclass should override this function
    def get_data(self):
        pass

    def every_minute_job(self, callback_fun=None):
        def __every_minute_job(self):
            callback_fun(self)
        self.add_job(__every_minute_job, trigger='cron', args=(self,), id='every_minute_job_'+str(id(__every_minute_job)), minute='*')

    def every_hour_job(self, callback_fun=None):
        def __every_hour_job(self):
            callback_fun(self)
        self.add_job(__every_hour_job, trigger='cron', args=(self,), id='every_hour_job_'+str(id(__every_hour_job)), hour='*')


if __name__ == '__main__':
    pass

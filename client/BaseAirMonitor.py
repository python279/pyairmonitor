import pytz
from serial import *
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
    def __init__(self, serial_device='/dev/tty.usbserial', baudrate=9600, bytesize=EIGHTBITS, parity=PARITY_NONE, stopbits=STOPBITS_ONE, timeout=1):
        BackgroundScheduler.__init__(self)
        self.serial_device = serial_device
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.timeout = timeout
        self.sensor_inst = Serial(self.serial_device, self.baudrate, self.bytesize, self.parity, self.stopbits, self.timeout)
        self.configure(executors=executors, job_defaults=job_defaults, timezone=pytz.timezone('Asia/Shanghai'))
        self.start()

    def __del__(self):
        self.shutdown()
        self.sensor_inst.close()

    # subclass should override this function
    def get_data(self):
        pass

    def every_minute_job(self, callback_fun=None):
        def __every_minite_job(self):
            callback_fun(self)
        self.add_job(__every_minite_job, trigger='cron', args=(self,), id='every_minute_job', minute='*')

    def every_hour_job(self, callback_fun=None):
        def __every_minite_job(self):
            callback_fun(self)
        self.add_job(__every_minite_job, trigger='cron', args=(self,), id='every_hour_job', hour='*')


if __name__ == '__main__':
    pass

# -*- coding: utf-8 -*-
#
# lhq@python279.org

import sys
import pytz
import time
from datetime import datetime
import logging
import logging.handlers
from optparse import OptionParser
from PMS5003T import PMS5003T
from Simulator import Simulator


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding("utf-8")
    timezone = pytz.timezone('Asia/Shanghai')
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    #console = logging.StreamHandler(sys.stdout)
    #console.setLevel(logging.INFO)
    #logging.getLogger().addHandler(console)
    try:
        syslog = logging.handlers.SysLogHandler(address="/dev/log", facility=logging.handlers.SysLogHandler.LOG_LOCAL7)
        syslog.setLevel(logging.INFO)
        logging.getLogger().addHandler(syslog)
    except:
        pass

    parser = OptionParser()
    parser.add_option("-s", "--simulator", action="store_true", dest="simulator", default=False, help="simulator")
    options, args = parser.parse_args()

    hour_data = []

    def sensor_data_process(self):
        # every minute job, get sensor data and append to hour_data
        # upload the hour_data to server every hour
        global hour_data
        data = self.get_data()
        hour_data.append(data)
        logging.info("\nnow %s got minute data, append to hour data" % datetime.now().strftime("%Y%m%d%H%M%S"))
        logging.info(repr(data))
        if datetime.now().strftime("%M") == '59' and len(hour_data):
            # TODO: transfer hour_data to server every hour
            logging.info("\nnow %s upload hour data to server" % datetime.now().strftime("%Y%m%d%H%M%S"))
            logging.info(repr(hour_data))
            with open("data.csv", "a") as f:
                csv = ""
                for d in hour_data:
                    csv += "%s:%d:%d:%d:%d:%d\n" % (d['time'], d['temperature'], d['humidity'], d['pm2.5'], d['pm10'], d['pm1'])
                f.write(csv)
            hour_data = []

    def remote_command_process(self):
        # every minute job, retrieve command from server
        # TODO:
        logging.info("\nnow %s retrieve command from server" % datetime.now().strftime("%Y%m%d%H%M%S"))
        pass

    def firmware_upgrade_process(self):
        # every hour job, firmware upgrade from server
        # TODO:
        logging.info("\nnow %s firmware upgrade from server" % datetime.now().strftime("%Y%m%d%H%M%S"))
        pass


    if options.simulator:
        sensor = Simulator()
    else:
        sensor = PMS5003T()

    sensor.every_minute_job(sensor_data_process)
    sensor.every_minute_job(remote_command_process)
    sensor.every_hour_job(firmware_upgrade_process)

    while True:
        time.sleep(10)

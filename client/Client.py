# -*- coding: utf-8 -*-
#
# lhq@python279.org

import sys
import pytz
import logging
import logging.handlers
from optparse import OptionParser
from PMS5003T import PMS5003T
from Simulator import Simulator


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding("utf-8")
    import time
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

    def every_minute(self):
        global hour_data
        data = self.get_data()
        hour_data.append(data)
        logging.info("\nnow %s got minute data, append to hour data" % data['time'])
        logging.info(repr(data))
        if data['time'][-2:] == '59' and len(hour_data):
            # TODO: transfer hour_data to server every hour
            logging.info("\nnow %s upload hour data to server" % data['time'])
            logging.info(repr(hour_data))
            with open("data.csv", "a") as f:
                csv = ""
                for d in hour_data:
                    csv += "%s:%d:%d:%d:%d:%d\n" % (d['time'], d['temperature'], d['humidity'], d['pm2.5'], d['pm10'], d['pm1'])
                f.write(csv)
            hour_data = []

    if options.simulator:
        sensor = Simulator()
    else:
        sensor = PMS5003T()
    sensor.every_minute_job(every_minute)

    while True:
        time.sleep(10)

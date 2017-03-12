# -*- coding: utf-8 -*-
#
# lhq@python279.org

import os
import sys
import pytz
import time
import ConfigParser
from datetime import datetime
import logging
import logging.handlers
from optparse import OptionParser
from error import trace_msg
from httpRequest import HttpRequest
from PMS5003T import PMS5003T
from Simulator import Simulator


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding("utf-8")
    timezone = pytz.timezone('Asia/Shanghai')

    config = ConfigParser.SafeConfigParser()
    config.readfp(open("Client.cfg"))
    client = dict(config.items("Client"))

    os.mkdir(client["datahouse"]) if not os.path.exists(client["datahouse"]) else True
    os.mkdir(client["loghouse"]) if not os.path.exists(client["loghouse"]) else True

    logging.basicConfig(level=logging.INFO, format="%(message)s")
    trfh = logging.handlers.TimedRotatingFileHandler(os.path.join(client["loghouse"], "client.log"), "d", 1, 10)
    trfh.setLevel(logging.INFO)
    logging.getLogger().addHandler(trfh)

    parser = OptionParser()
    parser.add_option("-s", "--simulator", action="store_true", dest="simulator", default=False, help="simulator")
    options, args = parser.parse_args()

    hour_data = []

    def sensor_data_process(self):
        # every minute job, get sensor data and append to hour_data
        # upload the hour_data to server every hour
        global hour_data
        global client
        data = self.get_data()
        hour_data.append(data)
        logging.info("\nnow %s got minute data, append to hour data" % datetime.now().strftime("%Y%m%d%H%M%S"))
        logging.info(repr(data))
        if datetime.now().strftime("%M") == '59' and len(hour_data):
            # flush hour_data to local fs every hour
            filename = os.path.join(client["datahouse"], "data-%s.csv" % datetime.now().strftime("%Y%m%d%H"))
            logging.info("\nnow %s upload hour data to server" % datetime.now().strftime("%Y%m%d%H%M%S"))
            logging.info(repr(hour_data))
            with open(filename, "w") as f:
                csv = ""
                for d in hour_data:
                    csv += "%s:%d:%d:%d:%d:%d\n" % (d['timestamp'], d['temperature'], d['humidity'], d['pm2.5'], d['pm10'], d['pm1'])
                f.write(csv)
            hour_data = []

    def upload_data_process(self):
        # every hour job, upload the hour_data to server every hour
        global client
        logging.info("\nnow %s upload hour data to server" % datetime.now().strftime("%Y%m%d%H%M%S"))
        filelist = os.listdir(client["datahouse"])
        for f in filelist:
            fullpath = os.path.join(client["datahouse"], f)
            if os.path.isfile(fullpath) and fullpath.endswith(".csv") and os.path.getsize(fullpath):
                logging.info("\nnow %s upload hour data %s to server" % (datetime.now().strftime("%Y%m%d%H%M%S"), fullpath))
                with open(fullpath, "r") as fd:
                    try:
                        HttpRequest(client["server"]).post({'data': fd.read()})
                        fd.close()
                        os.remove(fullpath)
                    except:
                        logging.error(trace_msg())

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
        serial = client["serial"].split(",")
        for s in serial:
            try:
                sensor = PMS5003T(serial_device=s)
                break
            except:
                sensor = None
                logging.error(trace_msg())

    exit(255) if sensor is None else True

    sensor.every_minute_job(sensor_data_process)
    sensor.every_hour_job(upload_data_process)
    sensor.every_minute_job(remote_command_process)
    sensor.every_hour_job(firmware_upgrade_process)

    while True:
        time.sleep(10)

# -*- coding: utf-8 -*-
#
# lhq@python279.org

import os
import sys
import pytz
import ConfigParser
from datetime import datetime
import logging
import logging.handlers
from error import trace_msg
from PMS5003T import PMS5003T
import Queue
import web
import json


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    timezone = pytz.timezone('Asia/Shanghai')

    config = ConfigParser.SafeConfigParser()
    config.readfp(open('Client.cfg'))
    client = dict(config.items('Client'))

    os.mkdir(client['datahouse']) if not os.path.exists(client['datahouse']) else True
    os.mkdir(client['loghouse']) if not os.path.exists(client['loghouse']) else True

    logging.basicConfig(level=logging.INFO, format='%(message)s')
    trfh = logging.handlers.TimedRotatingFileHandler(os.path.join(client['loghouse'], 'client.log'), 'd', 1, 10)
    trfh.setLevel(logging.INFO)
    logging.getLogger().addHandler(trfh)

    data_queue = Queue.Queue(1000)

    def sensor_data_process2(self):
        # every 10second job, get sensor data and append to a queue
        global data_queue
        data = self.get_data()
        if data_queue.full():
            data_queue.get(False)
        data_queue.put(data, False)
        with open(os.path.join(client['datahouse'], 'data.csv'), 'w') as f:
            f.write("%d:%d:%d:%d:%d:%d:%d:%d\n" % (data['timestamp'], data['temperature'], data['humidity'], data['pm2.5'], data['pm10'], data['pm1.0'], data['switch1'], data['switch2']))
        logging.info('\nnow %s got 10second data, append to data queue' % datetime.now().strftime('%Y%m%d%H%M%S'))
        logging.info(repr(data))

    serial = client['serial'].split(',')
    for s in serial:
        try:
            sensor = PMS5003T(serial_device=s)
            break
        except:
            sensor = None
            logging.error(trace_msg())

    exit(255) if sensor is None else True

    sensor.every_10second_job(sensor_data_process2)

    urls = (
        '/pyairmonitor', 'pyairmonitor'
    )
    app = web.application(urls, globals())

    class pyairmonitor:
        def GET(self):
            data = []
            while not data_queue.empty():
                data.append(data_queue.get())
            web.header('Content-Type', 'text/json')
            return json.dumps(data)

        def POST(self):
            post_data = web.input()
            print post_data['switch1']
            print post_data['switch2']
            pass

    app.run()


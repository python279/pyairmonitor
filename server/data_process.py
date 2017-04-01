# -*- coding: utf-8 -*-
#
# lhq@python279.org

import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


if __name__ == '__main__':
    columns = ['timestamp', 'temperature', 'humidity', 'pm2.5', 'pm10', 'pm1.0']
    columns_without_index = ['temperature', 'humidity', 'pm2.5', 'pm10', 'pm1.0']
    dtype = {'temperature': np.int32, 'humidity': np.int32, 'pm2.5': np.int32, 'pm10': np.int32, 'pm1.0': np.int32}
    df = pd.DataFrame(columns=columns)
    for f in os.listdir('.'):
        if f.endswith('.csv'):
            s = pd.read_csv(f, engine='c', sep=':', header=None, names=columns, dtype=dtype, parse_dates=True,
                            index_col='timestamp', date_parser=lambda x: pd.to_datetime(x, format='%Y%m%d%H%M%S'))
            df = df.append(s)
    #
    df.drop_duplicates()

    days = sorted(set(df.index.date))
    print days
    for d in days:
        day_data = df.loc[d.strftime('%Y-%m-%d'), columns_without_index]
        aggregated_day_data = pd.DataFrame(columns=columns)
        hours = sorted(set(day_data.index.hour))
        for h in hours:
            hour_data = day_data.loc['%s %02d' % (d.strftime('%Y-%m-%d'), h), columns_without_index]
            aggregated_day_data = aggregated_day_data.append(pd.DataFrame(hour_data.mean()).T, ignore_index=True)[columns_without_index]
        aggregated_day_data.insert(0, 'hour', pd.DataFrame(hours, dtype=np.int32))
        aggregated_day_data = aggregated_day_data.set_index('hour')
        print aggregated_day_data
        plt.figure()
        aggregated_day_data.plot(subplots=True, figsize=(24, 12), title=u'%s' % d.strftime('%Y-%m-%d'), fontsize=20)
        #plt.show()
        plt.savefig(d.strftime('%Y-%m-%d') + '.png')

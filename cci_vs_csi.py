# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 21:28:40 2016

@author: tfalcoff
"""

import pandas as pd
import pandas.io.data as web
import datetime, pylab, quandl, scipy
from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY
from matplotlib.finance import candlestick_ohlc
import matplotlib.pyplot as plt
from matplotlib.dates import date2num
import numpy as np


s = datetime.datetime(2010, 1,1)
e = datetime.datetime(2015, 1, 1)

csi = quandl.get("UMICH/SOC1", authtoken="zo7kqTM5GbbuJUNsTKVa", 
                 start_date=s, end_date=e)

cci = quandl.get("OECD/KEI_CSCICP02_USA_ST_M", authtoken="zo7kqTM5GbbuJUNsTKVa", 
                 start_date=s, end_date=e)

x = csi['Index']
y = cci['Value']


#stats

print('corrcoef: {}'.format(np.corrcoef(x,y)[1,0]))

df = pd.DataFrame({'csi':x, 'cci':y})

pct_change = df.apply(lambda x: np.log(x) - np.log(x.shift(1)))

print('var csi: {}'.format(np.mean(pct_change['csi'])))
print('var cci: {}'.format(np.mean(pct_change['cci'])))


# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 21:12:42 2016

@author: tfalcoff
"""

import pandas as pd
import datetime, pylab, quandl
import matplotlib.pyplot as plt
import numpy as np

pylab.rcParams['figure.figsize'] = (10,6)

s = datetime.datetime(2010, 1,1)
e = datetime.datetime(2015, 1, 1)

dow = quandl.get("YAHOO/INDEX_DJI", authtoken="zo7kqTM5GbbuJUNsTKVa", 
                 start_date=s, end_date=e, collapse='monthly')

csi = quandl.get("UMICH/SOC1", authtoken="zo7kqTM5GbbuJUNsTKVa", 
                 start_date=s, end_date=e)
                 
df = pd.DataFrame({'^DJI': dow['Adjusted Close'], 'CSI': csi['Index']})

x = df['^DJI'] 
y = df['CSI']


#first plot

fig = pylab.figure()

ax1 = fig.add_subplot(111)
ax1.set_ylabel('CSI', color='g')
line1 = ax1.plot(y, 'g')

ax2 = fig.add_subplot(111, sharex=ax1, frameon=False)
ax2.yaxis.tick_right()
ax2.yaxis.set_label_position('right')
ax2.set_ylabel('^DJI', color='b')
line2 = ax2.plot(x, 'b')

pylab.show()


#second

fig, ax = plt.subplots()

fit = np.polyfit(x,y,1)
ax.plot(x, fit[0]*x+fit[1], color='red')
ax.scatter(x,y)
plt.xlabel('^DJI')
plt.ylabel('CSI')
plt.grid()
fig.show()


#third

pct_change = df.apply(lambda x: np.log(x) - np.log(x.shift(1)))

b = pct_change['^DJI'].dropna()
a = pct_change['CSI'].dropna()

fig, ax = plt.subplots()
fit2 = np.polyfit(a,b,1)
ax.plot(b, fit2[0]*b+fit2[1], color='red')
ax.scatter(a,b)
plt.xlabel('pct change ^DJI')
plt.ylabel('pct change CSI')
plt.grid()
fig.show()


#stats

print('corrcoef: {}'.format(np.corrcoef(x,y)[1,0]))

print('var pct change in ^DJI: {}'.format(np.var(a)))
print('var pct change in CSI: {}'.format(np.var(b)))




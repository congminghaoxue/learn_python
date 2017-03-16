#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-06-27 08:58:55
# @Author  : Zhou Bo (zhoub@suooter.com)
# @Link    : http://onlyus.online
# @Version : $Id$

import math

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class d():


ts = pd.Series(np.random.randn(1000), index=pd.date_range('1/1/2000', periods=1000))
ts = ts.cumsum()
# ts.plot()


df = pd.DataFrame(np.random.randn(1000, 4), index=ts.index, columns=['A', 'B', 'C', 'D'])
df = df.cumsum()
# print(df)
plt.figure()
df.plot()
plt.legend(loc='best')
plt.show()
# print('hello world')

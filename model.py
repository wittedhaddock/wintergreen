# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 17:15:17 2015

@author: james
"""

from __future__ import division

import numpy
import sqlite3
import pandas
from sklearn.neighbors import KNeighborsClassifier
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import numpy as np


connection = sqlite3.connect("./device_data.db")

query = """

SELECT * FROM data

"""
df = pandas.read_sql(query, connection)
connection.close()
x_ind = df.milliseconds.cumsum()
x_ind.plot()

time_series = [i-x_ind[0] for i in x_ind]
g_d = {"g_x" : df.g_x, "g_y" : df.g_y, "g_z" : df.g_z}
g_df = pandas.DataFrame(data=g_d, index=range(len(time_series)))

a_d = {"a_x" : df.a_x, "a_y" : df.a_y, "a_z" : df.a_z}
a_df = pandas.DataFrame(data=a_d, index=range(len(time_series)))
df.plot()

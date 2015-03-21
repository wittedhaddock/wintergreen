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


connection = sqlite3.connect("./device_data.db")

query = """

SELECT * FROM data

"""
df = pandas.read_sql(query, connection)
connection.close()
x_ind = df.milliseconds
x_ind.plot()

x_df.plot()

df.plot()

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
x_ind = df.milliseconds
x_ind.plot()

[i for i in df.g_x]
time_series = [round(float(i)-float(df.g_x[0]), 7) for i in df.g_x]

g_d = {"g_x" : df.g_x, "g_y" : df.g_y, "g_z" : df.g_z}
g_df = pandas.DataFrame(data=g_d, index=df.milliseconds)

a_d = {"a_x" : df.a_x, "a_y" : df.a_y, "a_z" : df.a_z}
a_df = pandas.DataFrame(data=a_d, index=range(len(time_series)))
df.plot()

holdout_number = round(len(df) * 0.2, 0) #save 1/5 for cross validation

test_indices = numpy.random.choice(df.index, holdout_number, replace = False)
train_indices = df[~df.index.isin(test_indices)]

Jon_df = df[df.name == "JonBlum"]
James_df = df[df.name == "James"]

jj_d = {"James X Rotation" : James_df.g_x, "Jon X Rotation" : Jon_df.g_x}
jj_df = pandas.DataFrame(data=jj_d, index = range(len(time_series)))
jj_df.plot()
knn = KNeighborsClassifier()

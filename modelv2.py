# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 18:52:54 2015

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
import sklearn.grid_search as gs
from sklearn.cluster import KMeans



connection = sqlite3.connect("./device_data.db")

query = """

SELECT * FROM data

"""
df = pandas.read_sql(query, connection)
connection.close()

explanatory_header_names = ["milliseconds", "g_x", "g_y", "g_z", "a_x", "a_y", "a_z"]

df = df.replace(to_replace="James", value = 1, inplace=False)
df = df.replace(to_replace="JonBlum", value = 2, inplace = False)
df = df.replace(to_replace="Andrew", value = 3, inplace = False)


df_james = df[df.name == 1]
df_james = df_james[df_james.milliseconds - df_james.milliseconds[0] < 5000]
df_james = df_james[df_james.milliseconds - df_james.milliseconds[0] > 4000]

df_james.g_x.plot()
df_james.g_y.plot()
df_james.g_z.plot()

df_james.a_x.plot()
df_james.a_y.plot()
df_james.a_z.plot()


james_gyroscope_x = df_james.g_x
def derivative(dataFrameColumn):
    deltas = []
    j = 0
    while j < 1000:
        j = j + 1
        deltas.append( dataFrameColumn[j] - dataFrameColumn[j - 1])
    return deltas
    
james_gyroscope_x_derivative = derivative(james_gyroscope_x)

james_gyroscope_x_concavity = derivative(james_gyroscope_x_derivative)

a_df = pandas.DataFrame(data=a_d, index=range(len(time_series)))
james_gyroscope_x[:1000].plot()
james_gryoscope_x_derivative_df = pandas.DataFrame(data=james_gyroscope_x_derivative, index = range(len(james_gyroscope_x_derivative) ))
df_slice = df#[df.milliseconds - df.milliseconds[0] < 000]
df_slice = df[df_slice.milliseconds - df.milliseconds[0] > 4000]

kmeans_est = KMeans(n_clusters=3)
kmeans_est.fit(df_slice)
plt.scatter(df_slice.g_x, df_slice.name, s=60, c=kmeans_est.labels_)

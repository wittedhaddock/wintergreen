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

df_james = df[df.name == "James"]
df_james = df_james[df_james.milliseconds - df_james.milliseconds[0] < 13000]
df_james = df_james[df_james.milliseconds - df_james.milliseconds[0] > 4000]

df_james.g_x.plot()
df_james.g)

kmeans_est = KMeans(n_clusters=3)
kmeans_est.fit(df[["milliseconds", "g_x"]])
plt.scatter(df.milliseconds, df.g_x, s=60, c=kmeans_est.labels_)

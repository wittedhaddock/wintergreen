# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 20:44:55 2015

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
from sklearn.decomposition import PCA

connection = sqlite3.connect("./device_data.db")

query = """

SELECT * FROM data

"""
df = pandas.read_sql(query, connection)

def dictByTime(dataframe):
    for i in dataframe:
        print i
        
dictByTime(df)

df2 = pandas.DataFrame(data=df[["g_x", "g_y", "g_z"]], index=df.milliseconds, columns=[i for i in df.columns if i not in ["name", "milliseconds"]])

connection.close()

pandas.DataFrame(index=[1,2,3], columns=[1,2,3])

#convert strings to ints
j = 0
for i in set(df.name):
    df.replace(to_replace=i, value=j, inplace=True)
    j = j + 1
    

def createDictIndexedByTimeFromDataFrameIndexedUniformly(dataframe):
    resultantDictionary = dict()
    for i in dataframe.values:
        resultantDictionary[i[1]] = [j for j in i if j != i[1]]
    return resultantDictionary

timeKeyedDict = createDictIndexedByTimeFromDataFrameIndexedUniformly(df)

df3 = pandas.DataFrame(data=timeKeyedDict)
df3.plot()


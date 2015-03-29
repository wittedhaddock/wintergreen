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
import sklearn.grid_search as gs


connection = sqlite3.connect("./device_data.db")

query = """

SELECT * FROM data

"""
df = pandas.read_sql(query, connection)
df.nam
connection.close()
x_ind = df.milliseconds
x_ind.plot()

[i for i in df.g_x]
time_series = [round(float(i)-float(df.g_x[0]), 7) for i in df.g_x]

name_int_series = []
for name in df.name:
    if name == "James":
        name_int_series.append(1)
    if name == "JonBlum":
        name_int_series.append(2)
ni_series = pandas.Series(data = name_int_series, index = df.index)

g_d = {"g_x" : df.g_x, "g_y" : df.g_y, "g_z" : df.g_z}
g_df = pandas.DataFrame(data=g_d, index=df.milliseconds)

a_d = {"a_x" : df.a_x, "a_y" : df.a_y, "a_z" : df.a_z}
a_df = pandas.DataFrame(data=a_d, index=range(len(time_series)))

df.plot()

holdout_number = round(len(df) * 0.2, 0) #save 1/5 for cross validation

#WARNING: IMPLEMENTATION ASSUMES UNIFORM DISTRUBTION WHEN TIME SERIES IS NOT UNIFORM. RESULTS ARE SKEWED.
response_df_unfilled = df.name
response_df = response_df_unfilled.replace(to_replace="James", value = 1, inplace=False)
response_df = response_df.replace(to_replace="JonBlum", value = 2, inplace = False)

explanatory_df = df[["g_x", "g_y", "g_z", "a_x", "a_y", "a_z"]]


test_indices = numpy.random.choice(df.index, holdout_number, replace = False)
train_indices = df[~df.index.isin(test_indices)]


#find out for certain what the difference between indexing without the end comma stoccato       
response_df_train = response_df.ix[response_df.index,]
test = response_df.ix[response_df.index]
explanatory_df_train = explanatory_df.ix[response_df.index,]

response_df_test = response_df.ix[test_indices,]
explanatory_df_test = explanatory_df.ix[test_indices,]




knn = KNeighborsClassifier(n_neighbors = 9)
knn.fit(explanatory_df_train, response_df_train)

neighbor_span = range(1, 30)
param_grid = dict(n_neighbors = neighbor_span)

gscv = gs.GridSearchCV(knn, param_grid = param_grid, cv = 50, scoring="accuracy")
gscv.fit(explanatory_df, response_df)

gscv.best_estimator_

response_prediction = knn.predict(explanatory_df_test)
response_predicted_prob = knn.predict_proba(explanatory_df_test)

def nonDefinitiveDiscernmentsOfProbabilityDistribution(predicted_probs):
    amalgamate = []
    for i, val in enumerate(predicted_probs):
        for j in val:
            if j == 1 or j == 0:
                break
            amalgamate.append((i, val))
    return amalgamate

number_correct = len(response_df_test[response_df_test == response_prediction]) 
total_number = len(response_df_test)
accuracy = number_correct / total_number

#crude visualization
Jon_df = df[df.name == "JonBlum"]
James_df = df[df.name == "James"]
jj_d = {"James X Rotation" : James_df.g_x, "Jon X Rotation" : Jon_df.g_x, "James Y Rotation" : James_df.g_y, "Jon y Rotation" : Jon_df.g_y}
jj_df = pandas.DataFrame(data=jj_d, index = range(len(time_series)))
jj_df.plot()

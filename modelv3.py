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

import statsmodels as sm

#TODO
#organize by person, individuated by session
#train on multiple user sessions to "learn person" agnostic their session
#Develop confidence interval to describe probability of "this is the person I was trained to know"
#test, iterate, remove all assumptions, hypothesize, test, iterate, repeat x 1000000

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
i = 0
for j in set(df.name):
    print j
    if j == "James":
        df.replace(to_replace="James", value = 1, inplace=True)
    else:
        df.replace(to_replace=j, value=0, inplace=True)
    

def createDictIndexedByTimeFromDataFrameIndexedUniformly(dataframe):
    resultantDictionary = dict()
   
    for i in dataframe.values:
        resultantDictionary[i[1]] = [j for j in i if j != i[1]]
    return resultantDictionary

timeKeyedDict = createDictIndexedByTimeFromDataFrameIndexedUniformly(df)

df3 = pandas.DataFrame(data=timeKeyedDict)
df3 = df3.T #columns are attributes, rows indexed by time

df3


df_fft = numpy.fft.fftn(df)
df_ifft = numpy.fft.ifftn(df_fft)
df.milliseconds[0] - df.milliseconds[1000]

train_columns = df.columns[1:]
logit = sm.discrete.discrete_model.Logit(df.name, df[train_columns])
result = logit.fit()
result.summary()

dataframe_fft = pandas.DataFrame(data=df_fft)
logit_ff = sm.discrete.discrete_model.Logit(df.name, dataframe_fft)
result_ff = logit_ff.fit()
result_ff.summary()


mean_gx = np.mean(df.g_x)
mean_gy = np.mean(df.g_y)
mean_gz = np.mean(df.g_z)
mean_ax = np.mean(df.a_x)
mean_ay = np.mean(df.a_y)
mean_az = np.mean(df.a_z)

mean_motion_vector = np.array([[mean_gx, mean_gy, mean_gz, mean_ax, mean_ay, mean_az]])
covariance_matrix = np.cov([df.g_x, df.g_y, df.g_z, df.a_x, df.a_y, df.a_z])

eig_val_cov, eig_vec_cov = np.linalg.eig(covariance_matrix)


from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d
from matplotlib.patches import FancyArrowPatch


class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        FancyArrowPatch.draw(self, renderer)

fig = plt.figure(figsize=(7,7))
ax = fig.add_subplot(111, projection='3d')

ax.plot(df.g_x, df.g_y,
    df.g_z, 'o', markersize=8, color='green', alpha=0.02)
ax.plot([mean_gx], [mean_gy], [mean_gz], 'o', \
    markersize=10, color='red', alpha=0.2)
for v in eig_vec_cov.T: 
    a = Arrow3D([mean_gx, v[0]], [mean_gy, v[1]],\
        [mean_gz, v[2]], mutation_scale=40, lw=3, arrowstyle="-|>", color="r")
    ax.add_artist(a)
ax.set_xlabel('gyroscope_x_values')
ax.set_ylabel('gyroscope_y_values')
ax.set_zlabel('gyroscope_z_values')

plt.title('Eigenvectors')

plt.show()

##check that eigen vector magnitude is one (actually checking close to, rather than absolute, due to rounding error)
for ev in eig_vec_cov:
    np.testing.assert_almost_equal(1.0, np.linalg.norm(ev))
    

eigen_pairs = [(np.abs(eig_val_cov[i]), eig_vec_cov[:,i]) for i in range(len(eig_vec_cov))]  #wondering about the absolute value
eigen_pairs.sort()
eigen_pairs.reverse()

for i in eigen_pairs:
    print i[0]
    
#transformation onto subspace
#via   y = W(Transposed) * x
top3Matrix = np.hstack((eigen_pairs[0][1].reshape(6, 1), eigen_pairs[1][1].reshape(6, 1), eigen_pairs[2][1].reshape(6, 1)))
transformed_data = top3Matrix.T.dot(df[["g_x", "g_y", "g_z", "a_x", "a_y", "a_z"]].T)
transformed_data[:,:10]



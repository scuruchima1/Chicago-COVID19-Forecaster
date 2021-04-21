from pandas import read_csv
from pandas.plotting import scatter_matrix
from matplotlib import pyplot
import numpy as np
import csv

dataset = read_csv('avg.csv')
data = np.genfromtxt("avg.csv", delimiter=",")
data = list(filter(([]).__ne__, data))
pyplot.plot(data)
scatter_matrix(dataset)
dataset.plot(kind='box', subplots=True, layout=(2,2), sharex=False, sharey=False)
pyplot.show()

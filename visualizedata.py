from pandas import read_csv
from pandas.plotting import scatter_matrix
from matplotlib import pyplot
import numpy as np
import csv

dataset = read_csv('trenddata.csv')
data = np.genfromtxt("trenddata.csv", delimiter=",")
dataset = list(filter(([]).__ne__, dataset))
pyplot.plot(data)
pyplot.show()

from pandas import read_csv
from pandas.plotting import scatter_matrix
from matplotlib import pyplot
import numpy as np

#Get 7-day moving average data set
dataset = read_csv(r'data/avg.csv')
data = np.genfromtxt(r"data/avg.csv", delimiter=",")
data = list(filter(([]).__ne__, data))

#Plot data, make scatter matrix, and a box and whisker plot
pyplot.plot(data)
scatter_matrix(dataset)
dataset.plot(kind='box', subplots=True, layout=(2,2), sharex=False, sharey=False)
pyplot.show()

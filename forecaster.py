from pandas import read_csv
from matplotlib import pyplot
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
import numpy as np
import csv

#Training dataset 
dataset = read_csv(r'data/avgshifted3.csv')

# Create a training dataset
array = dataset.values
X = array[:,2:]
X=X.astype('int')
y = array[:,1]
y=y.astype('int')

# Scale independent variables
scaler = StandardScaler()
scaler.fit(X)
X = scaler.transform(X)

# Data split for training and validation 
X_train, X_validation, Y_train, Y_validation = train_test_split(X, y, test_size=0.20, random_state=693)

# Make decision tree classifier model with training data
model = DecisionTreeClassifier(random_state=0)
model.fit(X_train, Y_train)

# Data set for 3-day prediction
test = read_csv(r'data/avg.csv')
array1 = test.values
X = array1[:-3,2:]
X = X.astype('int')

# Scale independent values for prediction data set
scaler.fit(X)
X = scaler.transform(X)

# Real data set to add prediction values
avgvalues = read_csv(r'data/trend.csv')
array2 = avgvalues.values
y = array2[:-3,1]
y=y.astype('int')

# Prediction results
predictions = model.predict(X)

# Append 3-day case predictions to real case data set
lastvalues = predictions[-3:]
for val in lastvalues:
	y = np.append(y, val)

# Find 7-day moving average of real and prediction case data 
y = np.convolve(y, np.ones(7), 'valid') / 7

# Find 7-day moving average of raw predictions 
predictions = np.convolve(predictions, np.ones(7), 'valid') / 7
# Append 0 at index 0 to offset 3 day gap and 7-day moving average
for i in range(9):
	predictions = np.insert(predictions, 0,0, axis=0)

# Take 11 real case days + 3 predicted case days for data set
predictedthree = y.tolist()
predictedthree = predictedthree[-14:]
predictedthree = np.array(predictedthree)
predicted = np.reshape(predictedthree, (-1,1))
writer = csv.writer(open(r'data/prediction.csv', 'w'))
writer.writerows(predicted)

#Take 3 predicted case days to graph
predictedthree = predictedthree[-4:]

#Plot data 
pyplot.plot(y)
pyplot.plot(predictions)
pyplot.plot([len(y)-4,len(y)-3,len(y)-2,len(y)-1],predictedthree)
# pyplot.show()
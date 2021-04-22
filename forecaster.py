from pandas import read_csv
from numpy import genfromtxt
from numpy import delete
from pandas.plotting import scatter_matrix
from matplotlib import pyplot
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
import numpy as np
from sklearn import tree
import csv

dataset = read_csv(r'data/avgshifted3.csv')

# Create a validation dataset
array = dataset.values
X = array[:,2:]
X=X.astype('int')
y = array[:,1]
y=y.astype('int')

# Scale dataset
scaler = StandardScaler()
scaler.fit(X)
X = scaler.transform(X)

X_train, X_validation, Y_train, Y_validation = train_test_split(X, y, test_size=0.20, random_state=693)

# Make predictions on validation dataset
# tr_score = []
# ts_score = []

# for j in range(1000):
# 	X_train, X_test, y_train, y_test = train_test_split(X, y , random_state =j,     test_size=0.20)
# 	model = DecisionTreeClassifier(random_state = 1)
# 	model.fit(X_train, y_train)

# 	tr_score.append(model.score(X_train, y_train))
# 	ts_score.append(model.score(X_test, y_test))

# J = ts_score.index(np.max(ts_score))
# print(np.max(ts_score))
# print(J)
# X_train, X_test, y_train, y_test = train_test_split(X, y , random_state = 693, test_size=0.20)
# model = DecisionTreeClassifier(random_state=693)
# model.fit(X_train,y_train)
# y_pred = model.predict(X_test)

#693 68
#2 3 15 19 26 28 31 35 87 89

model = DecisionTreeClassifier(random_state=0)
model.fit(X_train, Y_train)
# scores.append(model.score(X_validation, Y_validation))

test = read_csv(r'data/avg.csv')
array1 = test.values
X = array1[:-3,2:]
X = X.astype('int')

avgvalues = read_csv(r'data/trend.csv')
array2 = avgvalues.values
y = array2[:-3,1]
y=y.astype('int')



scaler.fit(X)
X = scaler.transform(X)

predictions = model.predict(X)

lastvalues = predictions[-3:]
print(lastvalues)
for val in lastvalues:
	y = np.append(y, val)

# print(y)
y = np.convolve(y, np.ones(7), 'valid') / 7
predictions = np.convolve(predictions, np.ones(7), 'valid') / 7
predictions = np.insert(predictions, 0,0, axis=0)
predictions = np.insert(predictions, 0,0, axis=0)
predictions = np.insert(predictions, 0,0, axis=0)

predictions = np.insert(predictions, 0,0, axis=0)
predictions = np.insert(predictions, 0,0, axis=0)
predictions = np.insert(predictions, 0,0, axis=0)
predictions = np.insert(predictions, 0,0, axis=0)
predictions = np.insert(predictions, 0,0, axis=0)
predictions = np.insert(predictions, 0,0, axis=0)

predictedthree = y.tolist()
predictedthree = predictedthree[-10:]
predictedthree = np.array(predictedthree)
print(predictedthree)
# print(predictions)
# pyplot.plot(predictions)
predicted = np.reshape(predictedthree, (-1,1))
print(predicted)
writer = csv.writer(open(r'data/prediction.csv', 'w'))
writer.writerows(predicted)
predictedthree = predictedthree[-3:]
pyplot.plot(y)
pyplot.plot([len(y)-3,len(y)-2,len(y)-1],predictedthree)
pyplot.show()
#fix prediction days 

# J = scores.index(np.max(scores))
# print(np.max(scores))
# print(J)
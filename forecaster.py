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
import numpy


dataset = read_csv('trendnobikeshifted.csv')
# print(dataset.head(20))
# print(dataset.describe())
# scatter_matrix(dataset)
# pyplot.show()

#Create a validation dataset
array = dataset.values
X = array[:,2:]
X=X.astype('int')
print(X)
y = array[:,1]
y=y.astype('int')
print(y)
X_train, X_validation, Y_train, Y_val2idation = train_test_split(X, y, test_size=0.30, random_state=1)

# Spot Check Algorithms
models = []
models.append(('LR', LogisticRegression(solver='liblinear', multi_class='ovr')))
models.append(('LDA', LinearDiscriminantAnalysis()))
models.append(('KNN', KNeighborsClassifier()))
models.append(('CART', DecisionTreeClassifier()))
models.append(('NB', GaussianNB()))
models.append(('SVM', SVC(gamma='auto')))

# evaluate each model in turn
results = []
names = []
for name, model in models:
	kfold = StratifiedKFold(n_splits=4, random_state=1, shuffle=True)
	cv_results = cross_val_score(model, X_train, Y_train, cv=kfold, scoring='accuracy')
	results.append(cv_results)
	names.append(name)
	print('%s: %f (%f)' % (name, cv_results.mean(), cv_results.std()))

# Make predictions on validation dataset
model = LinearDiscriminantAnalysis()
model.fit(X_train, Y_train)
# test = numpy.array(X_validation)
# test = numpy.array([[45.2,955.2]])
test = read_csv('trendnobike.csv')
array = test.values
X = array[:,2:]
X=X.astype('int')
test = X
y = array[:,1]
y=y.astype('int')
predictions = model.predict(test)
print(test)
print(predictions)
pyplot.plot(predictions)
pyplot.plot(y)
pyplot.show()
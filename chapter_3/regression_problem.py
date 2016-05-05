import pandas as pd
import numpy as np
from sklearn import cross_validation
from sklearn import svm
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error



df = pd.read_csv('housing.csv',sep=',',header=None)
#shuffle the data
df = df.iloc[np.random.permutation(len(df))]
X= df[df.columns[:-1]].values
Y = df[df.columns[-1]].values

cv = 10
print 'linear regression'
lin = LinearRegression()
scores = cross_validation.cross_val_score(lin, X, Y, cv=cv)
print("accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
predicted = cross_validation.cross_val_predict(lin, X,Y, cv=cv)
print 'MSE:',mean_squared_error(Y,predicted)

print 'ridge regression'
ridge = Ridge(alpha=1.0)
scores = cross_validation.cross_val_score(ridge, X, Y, cv=cv)
print("accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
predicted = cross_validation.cross_val_predict(ridge, X,Y, cv=cv)
print 'MSE:',mean_squared_error(Y,predicted)

print 'lasso regression'
lasso = Lasso(alpha=0.1)
scores = cross_validation.cross_val_score(lasso, X, Y, cv=cv)
print("accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
predicted = cross_validation.cross_val_predict(lasso, X,Y, cv=cv)
print 'MSE:',mean_squared_error(Y,predicted)

#trees
print 'decision tree regression'
tree = DecisionTreeRegressor(random_state=0)
scores = cross_validation.cross_val_score(tree, X, Y, cv=cv)
print("accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
predicted = cross_validation.cross_val_predict(tree, X,Y, cv=cv)
print 'MSE:',mean_squared_error(Y,predicted)

print 'random forest regression'
forest = RandomForestRegressor(n_estimators=50, max_depth=None,min_samples_split=1, random_state=0)
scores = cross_validation.cross_val_score(forest, X, Y, cv=cv)
print("accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
predicted = cross_validation.cross_val_predict(forest, X,Y, cv=cv)
print 'MSE:',mean_squared_error(Y,predicted)

#svm
print 'linear svm'
svm_lin = svm.SVR(epsilon=0.2,kernel='linear',C=1)
scores = cross_validation.cross_val_score(svm_lin, X, Y, cv=cv)
print("accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
predicted = cross_validation.cross_val_predict(svm_lin, X,Y, cv=cv)
print 'MSE:',mean_squared_error(Y,predicted)

print 'svm rbf'
clf = svm.SVR(epsilon=0.2,kernel='rbf',C=1.)
scores = cross_validation.cross_val_score(clf, X, Y, cv=cv)
print("accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
predicted = cross_validation.cross_val_predict(clf, X,Y, cv=cv)
print 'MSE:',mean_squared_error(Y,predicted)

print 'knn'
knn = KNeighborsRegressor()
scores = cross_validation.cross_val_score(knn, X, Y, cv=cv)
print("accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
predicted = cross_validation.cross_val_predict(knn, X,Y, cv=cv)
print 'MSE:',mean_squared_error(Y,predicted)
#print 'poly svm'
#clf = svm.SVR(epsilon=0.2,kernel='poly',C=1,random_state=0).fit(X_train, y_train)
#print clf.score(X_test, y_test)

from sklearn.feature_selection import RFE
best_features=4
print 'feature selection on linear regression'
rfe_lin = RFE(lin,best_features).fit(X,Y)
mask = np.array(rfe_lin.support_)
scores = cross_validation.cross_val_score(lin, X[:,mask], Y, cv=cv)
print("R2: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
predicted = cross_validation.cross_val_predict(lin, X[:,mask],Y, cv=cv)
print 'MSE:',mean_squared_error(Y,predicted)

print 'feature selection ridge regression'
rfe_ridge = RFE(ridge,best_features).fit(X,Y)
mask = np.array(rfe_ridge.support_)
scores = cross_validation.cross_val_score(ridge, X[:,mask], Y, cv=cv)
print("R2: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
predicted = cross_validation.cross_val_predict(ridge, X[:,mask],Y, cv=cv)
print 'MSE:',mean_squared_error(Y,predicted)

print 'feature selection on lasso regression'
rfe_lasso = RFE(lasso,best_features).fit(X,Y)
mask = np.array(rfe_lasso.support_)
scores = cross_validation.cross_val_score(lasso, X[:,mask], Y, cv=cv)
print("R2: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
predicted = cross_validation.cross_val_predict(lasso, X[:,mask],Y, cv=cv)
print 'MSE:',mean_squared_error(Y,predicted)

print 'feature selection on decision tree'
rfe_tree = RFE(tree,best_features).fit(X,Y)
mask = np.array(rfe_tree.support_)
scores = cross_validation.cross_val_score(tree, X[:,mask], Y, cv=cv)
print("R2: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
predicted = cross_validation.cross_val_predict(tree, X[:,mask],Y, cv=cv)
print 'MSE:',mean_squared_error(Y,predicted)

print 'feature selection on random forest'
rfe_forest = RFE(forest,best_features).fit(X,Y)
mask = np.array(rfe_forest.support_)
scores = cross_validation.cross_val_score(forest, X[:,mask], Y, cv=cv)
print("R2: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
predicted = cross_validation.cross_val_predict(forest, X[:,mask],Y, cv=cv)
print 'MSE:',mean_squared_error(Y,predicted)

print 'feature selection on linear support vector machine'
rfe_svm = RFE(svm_lin,best_features).fit(X,Y)
mask = np.array(rfe_svm.support_)
scores = cross_validation.cross_val_score(svm_lin, X[:,mask], Y, cv=cv)
print("R2: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
predicted = cross_validation.cross_val_predict(svm_lin, X,Y, cv=cv)
print 'MSE:',mean_squared_error(Y,predicted)
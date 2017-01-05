#coding:UTF-8
#trainModel

from __future__ import print_function
from sklearn import svm
from sklearn import decomposition
from sklearn import gaussian_process
from sklearn import neighbors
from sklearn import tree
from sklearn import ensemble
from sklearn import naive_bayes
from sklearn import lda
from sklearn import qda
from sklearn.externals import joblib

from getData import getTrainData
import numpy as np
import matplotlib.pyplot as plt

features = getTrainData()
features_train = features[0:-50]
features_test = features[-50:]

pca = decomposition.PCA(n_components=24)
pca.fit(features_train)
joblib.dump(pca, 'pcaModel.model')

features_train = pca.transform(features_train)
features_test = pca.transform(features_test)

ratings = np.loadtxt('ratings.txt', delimiter=',')
ratings_train = ratings[0:-50]
ratings_test = ratings[-50:]

# regr = neighbors.KNeighborsClassifier(16)
# regr = svm.SVC(kernel="linear", C=0.025)
# regr = svm.SVC(gamma=1, kernel='poly', C=0.1)
# regr = tree.DecisionTreeClassifier(max_depth=25)  #param
# regr = ensemble.RandomForestClassifier(max_depth=24, n_estimators=24, max_features=24)  #param
# regr = naive_bayes.GaussianNB()
regr = lda.LDA()

print(features_train.shape)

print(ratings_train.shape)

regr.fit(features_train, ratings_train)
joblib.dump(regr, 'trainModel.model')



# ratings_predict = regr.predict(features_test)
# corr = np.corrcoef(ratings_predict, ratings_test)[0, 1]
# print 'Correlation:', corr
#
# residue = np.mean((ratings_predict - ratings_test) ** 2)
# print 'Residue:', residue
#
# truth, = plt.plot(ratings_test, 'r')
# prediction, = plt.plot(ratings_predict, 'b')
# plt.legend([truth, prediction], ["Ground Truth", "Prediction"])
#
# plt.show()

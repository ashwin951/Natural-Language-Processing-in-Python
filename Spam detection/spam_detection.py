from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import AdaBoostClassifier
import pandas as pd
import numpy as np 



# import dataset
data = pd.read_csv('spambase.data').as_matrix()
np.random.shuffle(data)


# classify data into features and label
X = data[:, :57]
Y = data[:, -1]

# split dataset into train test
Xtrain = X[:-100,]
Ytrain = Y[:-100,]
Xtest = X[-100:,]
Ytest = Y[-100:,]

# model
# Naive Bayes

model = MultinomialNB()
model.fit(Xtrain, Ytrain)

print("classification rate for NB:", model.score(Xtest,Ytest))

# model AdaBoostClassifier

model_ada = AdaBoostClassifier()
model_ada.fit(Xtrain,Ytrain)

print("Classification rate for Adaboost:",model_ada.score(Xtest,Ytest))
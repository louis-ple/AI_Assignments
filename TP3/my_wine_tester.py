"""
Team:
<<<<< TEAM NAME >>>>>
Authors:
<<<<< Frédérique Roy - 1894397 >>>>>
<<<<< Louis Plessis - 1933334 >>>>>
"""

from wine_testers import WineTester

import numpy as np

from sklearn.dummy import DummyClassifier
from sklearn.naive_bayes import BernoulliNB
from sklearn.tree import A
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
from sklearn.feature_selection import RFE

class MyWineTester(WineTester):
    def __init__(self):
        # TODO: initialiser votre modèle ici:
        self.classifier = DecisionTreeClassifier()
        pass

    def train(self, X_train, y_train):
        """
        train the current model on train_data
        :param X_train: 2D array of data points.
                each line is a different example.
                each column is a different feature.
                the first column is the example ID.
        :param y_train: 2D array of labels.
                each line is a different example.
                the first column is the example ID.
                the second column is the example label.
        """
        # TODO: entrainer un modèle sur X_train & y_train

        # Deleting the first column (id) since it's not relevant for the prediction
        X_train = np.delete(X_train, 0, 1)
        y_train = np.delete(y_train, 0, 1).flatten()

        # Converting white/red to 0/1 category
        for i in range(len(X_train)):
            if X_train[i][0] == 'white':
                X_train[i][0] = 0
            elif X_train[i][0] == 'red':
                X_train[i][0] = 1

        # Train/Valid 80/20 split
        X_valid = X_train[3600:]
        y_valid = y_train[3600:]
        X_train = X_train[:3600]
        y_train = y_train[:3600]

        # Feature selection
        selector = RFE(DecisionTreeClassifier(), n_features_to_select=10, step=1)
        selector = selector.fit(X_train, y_train)
        print(selector.ranking_)

        # Deleting white/red wine column
        X_train = np.delete(X_train, 0, 1)
        X_valid = np.delete(X_valid, 0, 1)

        # Deleting fixed acidity column
        X_train = np.delete(X_train, 0, 1)
        X_valid = np.delete(X_valid, 0, 1)

        # Model
        params = [{'max_depth': [17, 18, 19], 'n_estimators': [400, 700, 1000]}]
        self.classifier = GridSearchCV(RandomForestClassifier(criterion='entropy'), params, refit=True)
        #self.classifier = RandomForestClassifier(max_depth=18, n_estimators=400)
        self.classifier = self.classifier.fit(X_train, y_train)

        print(self.classifier.best_params_)

        predictions_valid = self.classifier.predict(X_valid)
        print("Validation accuracy: ", accuracy_score(y_valid, predictions_valid))

    def predict(self, X_data):
        """
        predict the labels of the test_data with the current model
        and return a list of predictions of this form:
        [
            [<ID>, <prediction>],
            [<ID>, <prediction>],
            [<ID>, <prediction>],
            ...
        ]
        :param X_data: 2D array of data points.
                each line is a different example.
                each column is a different feature.
                the first column is the example ID.
        :return: a 2D list of predictions with 2 columns: ID and prediction
        """
        # TODO: make predictions on X_data and return them

        # Deleting the first column (id)
        X_data = np.delete(X_data, 0, 1)
        # Deleting white/red wine column
        X_data = np.delete(X_data, 0, 1)
        # Deleting fixed acidity column
        X_data = np.delete(X_data, 0, 1)

        predictions = self.classifier.predict(X_data)

        submission = []
        for i in range(len(predictions)):
            submission.append([i, predictions[i]])

        return submission
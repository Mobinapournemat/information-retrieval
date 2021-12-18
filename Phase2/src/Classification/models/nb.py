import typing as th  # Literals are available for python>=3.8
from sklearn.base import BaseEstimator, ClassifierMixin
import numpy as np

class NaiveBayes(BaseEstimator, ClassifierMixin):
    def __init__(self, kind, threshold):
        self.kind = kind
        self.threshold = threshold

    def fit(self, x, y, **fit_params):
        if self.kind == 'bernoulli':
            return self.bernoulli_fit(x, y)
        elif self.kind == 'gaussian':
            return self.gaussian_fit(x, y)

    def predict(self, x, probabilities):
        if self.kind == 'bernoulli':
            return self.bernoulli_predict(x, probabilities)
        elif self.kind == 'gaussian':
            return self.gaussian_predict(x, probabilities)


    def bernoulli_fit(self, x, y):
        prior = [0, 0]
        probabilities = []
        probabilities.append([[0, 0] for i in range(len(x[0]))])
        probabilities.append([[0, 0] for i in range(len(x[0]))])
        for i in range(len(y)):
            prior[y[i]] += 1
            for j in range(len(x[i])):
                value = 0
                if x[i][j] >= self.threshold[j]:
                    value = 1
                probabilities[y[i]][j][value] += 1
        prior[0] /= prior[0] + prior[1]
        prior[1] /= prior[0] + prior[1]
        for j in range(len(x[0])):
            probabilities[0][j][0] /= sum(probabilities[0][j])
            probabilities[0][j][1] /= sum(probabilities[0][j])
            probabilities[1][j][0] /= sum(probabilities[1][j])
            probabilities[1][j][1] /= sum(probabilities[1][j])
        return probabilities


    def gaussian_fit(self, x, y):
        prior = [0, 0]
        probabilities = []
        probabilities.append([[0, 0, 0] for i in range(len(x[0]))])
        probabilities.append([[0, 0, 0] for i in range(len(x[0]))])
        for i in range(len(y)):
            for j in range(len(x[i])):
                probabilities[y[i]][j][0] += x[i][j]
                probabilities[y[i]][j][2] += 1
            prior[y[i]] += 1
        prior[0] /= prior[0] + prior[1]
        prior[1] /= prior[0] + prior[1]
        for j in range(len(x[0])):
            probabilities[0][j][0] /= probabilities[0][j][2]
            probabilities[1][j][0] /= probabilities[1][j][2]
        for i in range(len(y)):
            for j in range(len(x[i])):
                probabilities[y[i]][j][1] += (x[i][j] - probabilities[y[i]][j][0])**2
        for j in range(len(x[0])):
            probabilities[0][j][1] /= probabilities[0][j][2]
            probabilities[1][j][1] /= probabilities[1][j][2]
        return probabilities


    def bernoulli_predict(self, x, probabilities):
        label = [0] * len(x)
        for i in range(len(x)):
            label_p = [0, 0]
            for j in range(len(x[i])):
                value = 0
                if int(x[i][j]) >= int(self.threshold[j]):
                    value = 1
                label_p[0] += np.log(probabilities[0][j][value])
                label_p[1] += np.log(probabilities[1][j][value])
            label[i] = 0
            if label_p[0] < label_p[1]:
                label[i] = 1
        return label

    def gaussian_predict(self, x, probabilities):
        label = []
        for i in range(len(x)):
            label_p = [0, 0]
            for j in range(len(x[i])):
                label_p[0] += -1 * (x[i][j] - probabilities[0][j][0])**2 / (2*probabilities[0][j][1]) - np.log(np.sqrt(probabilities[0][j][1]) * np.sqrt(2 * np.pi))
                label_p[1] += -1 * (x[i][j] - probabilities[1][j][0])**2 / (2*probabilities[1][j][1]) - np.log(np.sqrt(probabilities[1][j][1]) * np.sqrt(2 * np.pi))
            value = 0
            if label_p[0] < label_p[1]:
                value = 1 
            label.append(value)
        return label
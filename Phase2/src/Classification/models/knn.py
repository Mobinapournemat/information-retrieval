import typing as th
from sklearn.base import BaseEstimator, ClassifierMixin
import numpy as np
from collections import Counter


class KNN(BaseEstimator, ClassifierMixin):
    def __init__(
            self,
            k,
    ):
        self.k = k

    def fit(self, x, y, **fit_params):
        self.X_train = x
        self.y_train = y

    def predict(self, x):
        out = []
        for i in range(len(x)):
            d = []
            votes = []
            for j in range(len(x)):
                dist = np.linalg.norm(x[j] - x[i])
                d.append([dist, j])
            d.sort()
            d = d[0:self.k]
            for d, j in d:
                votes.append(self.y_train[j])
            ans = Counter(votes).most_common(1)[0][0]
            out.append(ans) 
        return out

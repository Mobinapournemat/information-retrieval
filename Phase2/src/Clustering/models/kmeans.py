import typing as th
from sklearn.base import TransformerMixin, ClusterMixin, BaseEstimator
import numpy as np

class KMeans(TransformerMixin, ClusterMixin, BaseEstimator):
    def __init__(
            self,
            k,
            max_iter
    ):
        self.k = k
        self.centroids = None
        self.max_iter = max_iter
    
    
    def calculate_centroids(self, x, y):
        k = self.k
        counter = [0]*k
        centroids = np.zeros((k, x[0].shape[0]))
        for i in range(len(x)):
            counter[y[i]] += 1
            centroids[y[i]] += x[i].flatten()
        for i in range(k):
            centroids[i] /= counter[i]
        return centroids


    def fit(self, x):
        k = self.k
        max_iter = self.max_iter
        count = 0
        centroids = x[np.random.randint(len(x), size=k), :]
        while count < max_iter:
            labels = [0]*len(x)
            for t in range(len(x)):
                temp = x[t]
                value = np.inf
                j = -1
                for i in range(k):
                    subt = temp - centroids[i]
                    tvalue = np.linalg.norm(subt)
                    if tvalue < value:
                        j = i
                        value = tvalue
                labels[t] = j
            centroids = self.calculate_centroids(x, labels)
            count += 1
        self.centroids = centroids
        return self


    def predict(self, x):
        k = self.k
        centroids = self.centroids
        labels = [0]*len(x)
        for t in range(len(x)):
                temp = x[t]
                value = np.inf
                j = -1
                for i in range(k):
                    subt = temp - centroids[i]
                    tvalue = np.linalg.norm(subt)
                    if tvalue < value:
                        j = i
                        value = tvalue
                labels[t] = j
        return labels
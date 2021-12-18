import typing as th
from abc import ABCMeta
from sklearn.base import DensityMixin, BaseEstimator

# since you can use sklearn (or other libraries) implementations for this task,
#   you can either initialize those implementations in the provided format or use them as you wish
from sklearn.mixture import GaussianMixture


class GMM(DensityMixin, BaseEstimator, metaclass=ABCMeta):
    def __init__(
            self,
            n_components: int,
            max_iter: int,
            covariance_type,
    ):
        self.gmm = GaussianMixture(n_components=n_components, max_iter=max_iter, covariance_type=covariance_type, init_params='kmeans')

    def fit(self, x):
        self.gmm.fit(x)
        return self

    def predict(self, x):
        return self.gmm.predict(x)

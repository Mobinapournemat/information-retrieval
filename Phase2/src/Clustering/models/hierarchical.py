import typing as th
from sklearn.base import ClusterMixin, BaseEstimator
# since you can use sklearn (or other libraries) implementations for this task,
#   you can either initialize those implementations in the provided format or use them as you wish
from sklearn.cluster import AgglomerativeClustering


class Hierarchical(ClusterMixin, BaseEstimator):
    def __init__(
            self,
            n_clusters: int,
            affinity
    ):
        self.clustering = AgglomerativeClustering(n_clusters=n_clusters, affinity=affinity)

    def fit_predict(self, x, **kwargs):
        self.clustering.fit(x)
        return self.clustering.labels_

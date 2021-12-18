import typing as th
from sklearn.base import BaseEstimator, ClassifierMixin

# since you can use sklearn (or other libraries) implementations for this task,
#   you can either initialize those implementations in the provided format or use them as you wish
from sklearn.svm import SVC


class SVM(BaseEstimator, ClassifierMixin):
    def __init__(
            self,
            kernel
    ):
        self.svc = SVC(kernel= kernel)

    def fit(self, x, y, **fit_params):
        self.svc.fit(x, y)
        return self

    def predict(self, x, y=None):
        return self.svc.predict(x)

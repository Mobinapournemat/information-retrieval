import typing as th
from sklearn.base import BaseEstimator, ClassifierMixin

# since you can use sklearn (or other libraries) implementations for this task,
#   you can either initialize those implementations in the provided format or use them as you wish
from sklearn.neural_network import MLPClassifier


class NeuralNetwork(BaseEstimator, ClassifierMixin):
    def __init__(
            self,
            solver,
            hidden_layer_sizes,
            random_state,
            max_iter,
            activation
    ):
        self.MLP = MLPClassifier(solver = solver , hidden_layer_sizes = hidden_layer_sizes, random_state = random_state, max_iter = max_iter, activation = activation)

    def fit(self, x, y, **fit_params):
        self.MLP.fit(x, y)
        return self

    def predict(self, x):
        return self.MLP.predict(x)

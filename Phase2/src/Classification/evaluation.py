import typing as th

from sklearn.metrics import accuracy_score, fbeta_score, precision_score, recall_score

def accuracy(y, y_hat) -> float:
    return accuracy_score(y, y_hat)


def f1(y, y_hat, alpha: float = 0.5, beta: float = 1.):
    return fbeta_score(y, y_hat, beta=beta)


def precision(y, y_hat) -> float:
    return precision_score(y, y_hat)


def recall(y, y_hat) -> float:
    return recall_score(y, y_hat)


evaluation_functions = dict(accuracy=accuracy, f1=f1, precision=precision, recall=recall)


def evaluate(y, y_hat) -> th.Dict[str, float]:
    """
    :param y: ground truth
    :param y_hat: model predictions
    :return: a dictionary containing evaluated scores for provided values
    """
    return {name: func(y, y_hat) for name, func in evaluation_functions.items()}

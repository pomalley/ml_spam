"""Functions for computing metrics for evaluating the classifiers' performance.
"""
from __future__ import absolute_import, division

import numpy as np


def accuracy(labels, predictions):
    """Simple accuracy -- number of correct predictions.

    Args:
        labels (np.ndarray): true labels for the data; 1 = spam, 0 = ham; dtype should be bool or int
        predictions (np.ndarray): predictions for the data, same form as labels

    Returns:
        float: the accuracy
    """
    return 1 - np.abs(labels - predictions).mean()


def precision(labels, predictions):
    """Precision tells us how, well, precise our classifier is at determining spam.

    "Fraction of retrieved instances that are relevant", according to Wikipedia.

    precision = true positive / (true positive + false positive)

    Args:
        labels (np.ndarray): true labels for the data; 1 = spam, 0 = ham; dtype should be bool or int
        predictions (np.ndarray): predictions for the data, same form as labels

    Returns:
        float: the precision
    """
    tp = np.logical_and(predictions == 1, labels == 1).sum()
    fp = np.logical_and(predictions == 1, labels == 0).sum()
    return tp / (tp + fp)


def recall(labels, predictions):
    """Recall tell us how many of the total number of spam emails we identified.

    "Fraction of relevant instances that are retrieved", according to Wikipedia.

    recall = true positive / (true positive + false negative)

    Args:
        labels (np.ndarray): true labels for the data; 1 = spam, 0 = ham; dtype should be bool or int
        predictions (np.ndarray): predictions for the data, same form as labels

    Returns:
        float: the recall
    """
    tp = np.logical_and(predictions == 1, labels == 1).sum()
    fn = np.logical_and(predictions == 0, labels == 1).sum()
    return tp / (tp + fn)


def f1(labels, predictions):
    """The F1 score is the harmonic mean of precision and recall.

    Args:
        labels (np.ndarray): true labels for the data; 1 = spam, 0 = ham; dtype should be bool or int
        predictions (np.ndarray): predictions for the data, same form as labels

    Returns:
        float: the F1 score
    """
    p, r = precision(labels, predictions), recall(labels, predictions)
    return 2 * p * r / (p + r)

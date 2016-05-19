"""Functions for creating and plotting learning curves."""

from __future__ import absolute_import
import numpy as np
from matplotlib import pyplot as plt


def make_learning_curve(x_train, y_train, x_cv, y_cv, classifier, metric, n_points=10):
    """Generate a learning curve for the given classifier using the given data.

    We run the classifier n_points times, each time using more of the training data, and evaluate the classifier's
    performance as a function of training set size.

    Args:
        x_train (numpy.ndarray): the training data (2D array)
        y_train (numpy.ndarray): the training labels (1D array)
        x_cv (numpy.ndarray): the cross-validation data
        y_cv (numpy.ndarray): the cross-validation labels
        classifier: the classifier to use; must have `fit` and `predict` methods, i.e. the ones from sklearn will work
        metric ((numpy.ndarray, numpy.ndarray) -> float): metric evaluation function
        n_points (int): number of times to run the classifier to get a curve

    Returns:
        (np.ndarray, np.ndarray, np.ndarray): x-axis (size of training set), metric on training data, metric on CV data
    """
    m, n = x_train.shape  # number of samples, number of features
    inds = np.arange(m)
    ms, metric_train, metric_cv = np.zeros(n_points), np.zeros(n_points), np.zeros(n_points)
    for i in range(n_points):
        ms[i] = int(m * (float(i+1) / n_points))
        np.random.shuffle(inds)
        clf = classifier.fit(x_train[inds[:ms[i]], :], y_train[inds[:ms[i]]])
        predict_train = clf.predict(x_train[inds[:ms[i]], :])
        predict_cv = clf.predict(x_cv)
        metric_train[i] = metric(y_train[inds[:ms[i]]], predict_train)
        metric_cv[i] = metric(y_cv, predict_cv)
    return ms, metric_train, metric_cv


def plot_learning_curve(ms, metric_train, metric_cv, metric_name):
    ax = plt.figure().add_subplot(111)
    ax.plot(ms, metric_train, '-o', label='Training Data')
    ax.plot(ms, metric_cv, '-o', label='CV Data')
    ax.set_xlabel('Size of Training Set')
    ax.set_ylabel(metric_name)
    ax.legend(numpoints=1, loc='best')
    plt.show()

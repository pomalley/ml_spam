"""Apply an SVM to the classification problem.

We use the SVM implementation from scikit-learn.
"""

from __future__ import absolute_import

from sklearn import svm


# noinspection PyPep8Naming
def train(X, y):
    """Train an SVM classifier on the given X and y data.

    Args:
        X (np.ndarray): m x n matrix of stacked feature vectors.
        y (np.ndarray): n-length labeling vector of 1=spam, 0=ham.

    Returns:
        svm.SVC: trained SVM classifier
    """
    clf = svm.SVC()
    clf.fit(X, y)
    return clf

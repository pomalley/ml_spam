from __future__ import absolute_import

import pytest

from . import load_data


def test_make_sets():
    tolerance = 0.5
    train = 0.6
    cv = 0.2
    test = 1 - train - cv
    spam = range(1000)
    ham = range(1000)
    spam_train, ham_train, spam_cv, ham_cv, spam_test, ham_test = load_data.make_sets(spam, ham, train=train, cv=cv)
    assert abs(float(len(spam_train)) / len(spam) - train) < tolerance
    assert abs(float(len(ham_train)) / len(ham) - train) < tolerance
    assert abs(float(len(spam_cv)) / len(spam) - cv) < tolerance
    assert abs(float(len(ham_cv)) / len(ham) - cv) < tolerance
    assert abs(float(len(spam_test)) / len(spam) - test) < tolerance
    assert abs(float(len(ham_test)) / len(ham) - test) < tolerance
    for x in spam:
        assert x in spam_train or x in spam_cv or x in spam_test
    for x in ham:
        assert x in ham_train or x in ham_cv or x in ham_test

if __name__ == '__main__':
    pytest.main(['-v', __file__])

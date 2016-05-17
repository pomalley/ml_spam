from __future__ import absolute_import

import logging
import time

import numpy as np

from . import load_data, preprocess, features, svm


def prep_data(mode='symmetric difference', check_and_download=True):
    """Load the SpamAssassin data, preprocess it, generate features, and split into sets; return X and y data.

    The X data are (m x n) matrices of stacked feature vectors, the y data are m-long vectors with 1=spam, 0=ham.
    m = # samples, n = # features

    To see what's taking so long, turn on logging at the info level: `logging.getLogger().setLevel(logging.INFO)`.

    Args:
        mode (str): method for generating feature words. See features.make_feature_dict.
        check_and_download (bool): if True, run load_data.check_and_download()

    Returns:
        x_train, y_train, x_cv, y_cv, x_test, y_test

    """
    if check_and_download:
        load_data.check_and_download()
    t = time.time()
    logging.info("Loading SpamAssassin data")
    spams, hams = load_data.load_all_spamassassin()
    t = _log_time(t)
    logging.info("Preprocessing spam")
    spam_word_lists = [preprocess.make_word_list(x) for x in spams]
    t = _log_time(t)
    logging.info("Preprocessing ham")
    ham_word_lists = [preprocess.make_word_list(x) for x in hams]
    t = _log_time(t)
    logging.info("Counting words")
    spam_counts = features.count_words(spam_word_lists)
    ham_counts = features.count_words(ham_word_lists)
    t = _log_time(t)
    logging.info("Making feature lists")
    spam_words = features.get_top_words(spam_counts)
    ham_words = features.get_top_words(ham_counts)
    feature_dict = features.make_feature_dict(spam_words, ham_words, mode=mode)
    t = _log_time(t)
    logging.info("Building data")
    spam_data = [features.featurize(x, feature_dict) for x in spam_word_lists]
    ham_data = [features.featurize(x, feature_dict) for x in ham_word_lists]
    spam_train, ham_train, spam_cv, ham_cv, spam_test, ham_test = load_data.make_sets(spam_data, ham_data)
    x_train, y_train = features.make_arrays(spam_train, ham_train)
    x_cv, y_cv = features.make_arrays(spam_cv, ham_cv)
    x_test, y_test = features.make_arrays(spam_test, ham_test)
    _log_time(t)
    return x_train, y_train, x_cv, y_cv, x_test, y_test


def use_svm(x_train, y_train, x_cv, y_cv, x_test, y_test):
    t = time.time()
    logging.info("Training SVM classifier")
    clf = svm.train(x_train, y_train)
    t = _log_time(t)
    logging.info("Predicting CV set")
    pred_cv = clf.predict(x_cv)
    t = _log_time(t)
    print "CV error rate: {:.2f}%".format(np.abs(pred_cv-y_cv).mean()*100)
    logging.info("Predicting test set")
    pred_test = clf.predict(x_test)
    _log_time(t)
    print "Test error rate: {:.2f}%".format(np.abs(pred_test-y_test).mean()*100)
    return clf


def _log_time(t):
    logging.info("\t{:.4f} s".format(time.time() - t))
    return time.time()


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    stuff = prep_data()
    print
    use_svm(*stuff)

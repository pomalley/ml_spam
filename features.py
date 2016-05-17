"""Make features and featurize the entries."""
from __future__ import absolute_import
import operator

import numpy as np


def count_words(word_lists, deduplicate=True):
    """Count words from a list of word lists.

    Args:
        word_lists (list[list[unicode]]): list of converted emails.
        deduplicate (bool): optionally deduplicate each word list; i.e. count only the occurrence of a word in an email,
            not the number of times it appears

    Returns:
        dict[unicode, int]: word counts
    """
    d = {}
    for wl in word_lists:
        if deduplicate:
            wl = set(wl)
        for word in wl:
            d[word] = d.get(word, 0) + 1
    return d


def get_top_words(counts, threshold=100, maximum=0):
    """Get the top words from the given word counts.

    Args:
        counts (dict[unicode, int]): word->count mapping
        threshold (int): take all words with a count >= threshold
        maximum (int): max number of words to take, 0 for unlimited.

    Returns:
        list[unicode]: final word list. will be sorted by count, descending
    """
    l = []
    counts = sorted(counts.items(), key=operator.itemgetter(1), reverse=True)
    for word, count in counts:
        if count > threshold and (not maximum or len(l) < maximum):
            l.append(word)
    return l


def make_feature_dict(spam_words, ham_words=None, mode='spam only'):
    """Get a feature dict from a list of words.

    Modes are:
        'spam only': just use the spam words
        'spam-ham': use the set of spam words - the set of ham words
        'symmetric difference': use the symmetric difference of the two sets.

    Args:
        spam_words (list[unicode]): list of spam words, from e.g. get_top_words
        ham_words (list[unicode]): list of ham words, may or may not be used depending on mode
        mode (str): how to combine the word lists

    Returns:
        dict[unicode, int]: maps word -> index for building feature vectors
    """
    if mode == 'spam only':
        return dict((w, i) for i, w in enumerate(spam_words))
    if mode == 'spam-ham':
        return dict((w, i) for i, w in enumerate(set(spam_words) - set(ham_words)))
    if mode == 'symmetric difference':
        return dict((w, i) for i, w in enumerate(set(spam_words).symmetric_difference(ham_words)))
    raise ValueError('Unknown make_feature_dict mode: {}'.format(mode))


def featurize(word_list, feature_dict):
    """Convert a word_list into a feature vector, given a feature word list.

    Args:
        word_list (list[unicode]): list of words
        feature_dict (dict[unicode, int]): maps feature -> index

    Returns:
        np.ndarray: feature vector, 1 in indices where word is present, 0 otherwise
    """
    v = np.zeros(len(feature_dict))
    for w in word_list:
        if w in feature_dict:
            v[feature_dict[w]] = 1
    return v

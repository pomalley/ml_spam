"""preprocess.py -- functions to pre-process an email.

TODOs:
* strip the header, or use it somehow
* use real HTML recognition
* use a real url finder

"""
from __future__ import absolute_import
import re

from nltk.stem.snowball import EnglishStemmer
stemmer = EnglishStemmer()

# compile regexes on module import. I know Python caches "the most recent patterns" but I don't know how many that is.
regexes = {
    'email': re.compile(r'<?[^@\s]+?@[^@\s]+?\.[^@\s]+>?'),
    'html': re.compile(r'<[^<]*?>'),
    'url': re.compile(r'(http|https)://[^\s]*'),
    'number': re.compile(r'\d+'),
    'dollar': re.compile(r'\$+'),
    'clean': re.compile(r'[^\w\s]+'),
    'space': re.compile(r'[\s]+'),
}
replacements = {
    'email': ' emailaddr ',
    'html': ' ',
    'url': ' httpaddr ',
    'number': ' number ',
    'dollar': ' dollar '
}
replace_order = ['email', 'url', 'html', 'number', 'dollar']


def make_word_list(email):
    """Convert an email into a word list, applying all the normalizations, etc.

    Args:
        email (unicode): the email to convert, as a string

    Returns:
        list[unicode]: list of words.
    """
    return stem(to_list(clean(normalize(lower(strip_header(email))))))


def lower(email):
    """Convert the email to lower case.

    Args:
        email (unicode): the email

    Returns:
        unicode: the email in lower case
    """
    return email.lower()


def normalize(email):
    """Normalize features like URLs, email addresses, etc.

    Args:
        email (unicode): the email string

    Returns:
        unicode: the email string, normalized
    """
    for word in replacements:
        while re.search(regexes[word], email):
            email = re.sub(regexes[word], replacements[word], email)
    return email


def stem(words):
    """Apply stemming to a list of words.

    Args:
        words (list[unicode]): the word list

    Returns:
        unicode: the stemmed word list
    """
    return [stemmer.stem(word) for word in words if word]


def clean(email):
    """Remove any remaining non-words from the email.

    Args:
        email (unicode): the email

    Returns:
        unicode: the email, now with words only, one space between each
    """
    email = re.sub(regexes['clean'], ' ', email)
    email = re.sub(regexes['space'], ' ', email)
    return email


def to_list(email):
    """Convert the final email to a list of words.

    Args:
        email (unicode): the email

    Returns:
        list[unicode]: list of words
    """
    return email.split(' ')


def strip_header(email):
    """Remove the header by dropping all lines before the first empty line.

    Args:
        email (unicode): the email

    Returns:
        unicode: email with header removed
    """
    email = email.partition('\n\n')[-1]
    return email

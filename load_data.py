"""Load the data for processing.

"""
import os
import tarfile

spam_path = os.path.join('data', 'spam')
ham_path = os.path.join('data', 'ham')
spamassassin_spams = ['20021010_spam.tar.bz2', '20030228_spam.tar.bz2', '20030228_spam_2.tar.bz2']
spamassassin_hams = ['20021010_easy_ham.tar.bz2', '20021010_hard_ham.tar.bz2', '20030228_easy_ham.tar.bz2',
                     '20030228_easy_ham_2.tar.bz2', '20030228_hard_ham.tar.bz2']


def load_spamassassin_tbz(filename, max_emails=0):
    """Load a list of emails from the SpamAssassin public corpus.

    Args:
        filename (str): the .tar.bz2 file. each email is its own file inside.
        max_emails (int): maximum number of emails to load, or 0 for all.

    Returns:
        list[unicode]: list of emails
    """
    emails = []
    num = 0
    with tarfile.open(filename, 'r:bz2') as f:
        for info in f:
            if not info.isfile():
                continue
            email = f.extractfile(info).read()
            emails.append(email)
            num += 1
            if 0 < max_emails <= num:
                break
    return emails


def load_all_spamassassin():
    """Load all SpamAssassin emails.

    Returns:
        (list[unicode], list[unicode]): list of spam emails, list of ham emails
    """
    spams, hams = [], []
    for spam_file in spamassassin_spams:
        spams.extend(load_spamassassin_tbz(os.path.join(spam_path, spam_file)))
    for ham_file in spamassassin_hams:
        hams.extend(load_spamassassin_tbz(os.path.join(ham_path, ham_file)))
    return spams, hams

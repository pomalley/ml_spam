"""Load the data for processing.

"""
import os
import tarfile

spam_path = os.path.join('data', 'spam')
ham_path = os.path.join('data', 'ham')


def load_spamassassin(filename, max_emails=0):
    """Load a list of emails from the SpamAssassin public corpus.

    Args:
        filename (str): the .tar.gz file. each email is its own file inside.
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

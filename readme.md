# Spam Classifier

This is a toy spam classifier using machine learning techniques, in
Python. I'm putting this together just for fun, having recently taken 
the machine learning course by Andrew Ng on Coursera. Note that exercise
6 (when I took the course) implemented a support vector machine for spam
classification, so this project is not particularly groundbreaking.

The main purpose is to (1) see if I can do it and (2) see how much of a
difference various ML methods and features makes.

## The Process

Pipeline is simple: pre-process the emails, and then feed them to the
classifier.

**Vocabulary**

* _ham_: not spam
* _SVM_: support vector machine
* _NN_: neural network

### Pre-processing

The goal is to convert an email into a feature vector ready for 
processing.

Features:

* Presence of a given word in the email (0 or 1)
  - The words to use will be the most common words the spam emails in
    the training dataset.
  - Perhaps also try the most common words in the ham emails? I suppose
    the symmetric difference of the sets would make sense.
  - Vary the number of 
* Something to encode punctuation.
  - Fraction of punctuation? Words containing punctuation/numbers as 
    well as letters?
  - Presence of dollar signs?
* Length of email? Guessing it won't make a difference.
* Capitalization?
* Presence of a url/email address (or number thereof?)
* How shall we use the headers?

Pre-processing workflow:

1. Load the text of the email
2. Normalize:
  * capitalization
  * strip HTML
  * URLs -- replace with 'httpaddr' or similar
  * email addresses -- replace with 'emailaddr' or similar
  * number -- replace with 'number'?
  * punctuation -- replace $ with 'dollar'? or other punctuation?
3. Word stemming -- make this optional
4. Remove non-words, leaving only a list of words for the email

Now choose X of the most common words (possibly a symmetric difference
of these from the spam and ham) to determine the features. Then convert
each list of words to a feature vector, and we're ready to go.


### The Classifier

I guess we'll try to compare logistic regression vs NN (of various
 geometries) vs SVM...
 
## Data Sources

* SpamAssassin Public Corpus
  http://spamassasin.apache.or/publiccorpus
* My own emails, exported as mbox format
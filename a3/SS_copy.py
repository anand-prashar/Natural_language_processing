'''
Created on Sep 21, 2017

@author: anand
'''
"""Assignment 7: (Adversarial) Stylometry

Please add your code where indicated by "YOUR CODE HERE". You may conduct a
superficial test of your code by executing this file in a python interpreter.

This assignment asks you to replicate some aspects of the Brennan, Afroz, and Greenstadt (2012)
article on "adversarial stylometry."

"""

# Reminder: you may use any packages which come with Anaconda Python or are
# installed on the linux cluster. nltk and scikit-learn (sklearn) are among
# these packages.

import nltk
import sklearn
import pandas as pd
import string
import numpy as np
from collections import Counter


def character_count(text):
    """Count of characters.

    Args:
        text (str)

    Returns:
        int: character count

    """
    # TODO: ADD YOUR CODE HERE
    return len(text.replace(' ', ''))

def average_characters_per_word(text):
    """Average characters per word.

    Args:
        text (str)

    Returns:
        float: average characters per word

    """
    # TODO: ADD YOUR CODE HERE
    return character_count(text)/len(text.split())

def character_frequency(text):
    """Frequency of characters (a-z, case insensitive).

    Args:
        text (str)

    Returns:
        tuple of int: character frequency, a-z

    """
    # TODO: ADD YOUR CODE HERE
    return tuple(text.lower().count(x) for x in string.ascii_lowercase)

def character_2gram_frequency(text):
    """Character 2grams (e.g. aa, ab etc.), case insensitive.

    2grams are taken only within words (do not cross adjacent words).

    Including space to represent beginning-of-sequence and end-of-sequence
    there are 27 * 27 - 1 = 728 possible character 2grams. Some, such as "vq" are
    vanishingly rare.

    Args:
    text (str)

    Returns:
    tuple of int: character 2gram frequency

    """
    # TODO: ADD YOUR CODE HERE
    alphabets = ' ' + string.ascii_lowercase
    combs = [x+y for x in alphabets for y in alphabets]
    combs.remove('  ')
    return tuple(text.lower().count(bigram) for bigram in combs)



def pos_tag_frequency(text):
    """Frequencies of part-of-speech tags.

    Use "universal" tags or the Penn Treebank tags.

    Using universal tags, the sentence "Chairs have legs." yields the
    part-of-speech tag sequence ('NOUN', 'VERB', 'NOUN'), and two 2grams
    ('NOUN', 'VERB') and ('VERB', NOUN').


    Args:
        text (str): Text

    Returns:
        tuple of str: Frequency of part-of-speech tags

    """
    # TODO: ADD YOUR CODE HERE
    words = nltk.word_tokenize(text)
    postags = nltk.pos_tag(words, tagset='universal')
    tagset = ['ADJ','ADP','ADV','CONJ','DET','NOUN','NUM','PRT','PRON','VERB','.','X']
    tags = [tag[1] for tag in postags]
    return tuple(tags.count(tag) for tag in tagset)


def pos_tag_2gram_frequency(text):
    """Frequencies of part-of-speech tag 2grams.

    Uses the "universal" tagset.

    Some part-of-speech 2grams rarely occur.

    Using universal tags, the sentence "Chairs have legs." yields the
    part-of-speech tag sequence ('NOUN', 'VERB', 'NOUN'), and two 2grams
    ('NOUN', 'VERB') and ('VERB', NOUN').

    Args:
    text (str): Text

    Returns:
    tuple of str: Frequency of part-of-speech 2grams.

    """
    # TODO: ADD YOUR CODE HERE

    tagset = ['ADJ','ADP','ADV','CONJ','DET','NOUN','NUM','PRT','PRON','VERB','.','X']
    words = nltk.word_tokenize(text)
    tagged = nltk.pos_tag(words, tagset='universal')
    postags = tuple(part[1] for part in tagged)
    bigrams = list(nltk.bigrams(postags))
    tag_fd = nltk.FreqDist(bigram for bigram in bigrams)
    #print(list(tuple((val for key,val in tag_fd.items()))))
    return tuple((val for key,val in tag_fd.items()))

def punctuation_freq(text):
    punctuations = ':;?.!,"' + "'"
    return [text.count(punctuation) for punctuation in punctuations] 


def extract_features(texts):
    features = []
    for text in texts:
        row = [len(text.split())] + [average_characters_per_word(text)] + [character_count(text)] + [sum([char.isdigit() for char in text])*100/len(text)]
        row += [sum([char.isupper() for char in text])*100/len(text)] + [text.count(x) for x in '#$%&\()*+/<=>@[\\]^_{|}~'] + list(character_frequency(text))
        row += [text.lower().count(char) for char in string.digits]
        row += [len([word for word in text.split() if len(word) <=3])] + [get_hapax_dis(text, 1)/get_hapax_dis(text, 2)]
        row += list(pos_tag_frequency(text)) + punctuation_freq(text) + [text.count(word) for word in nltk.corpus.stopwords.words('english')]
        features.append(row)
    #print (features)
    return features

def get_hapax_dis(text, n):
    freq = nltk.FreqDist(word for word in text.split())
    hapax = [key for key,val in freq.items() if val==n]
    return len(hapax)

def predict_author_many(texts, texts_known_authors, known_authors):
    """Predict the author of one or more texts.

    Assumes that the author of each text in `texts` is by one of the known
    authors.

    FYI: the classifier Brennan, Afroz, and Greenstadt (2012) report using
    (successfully) is SVM with a polynomial kernel. This classifier is
    implemented as part of sklearn: ``sklearn.svm.SVC(kernel='poly')``.

    The Brennan-Greenstadt corpus is included in the repository.

    Args:
        texts (list of str): text(s) of unknown authorship
        texts_known_authors (list of str): texts of authors (for training)
        known_authors (list of int or str): labels for known authors (for training)

    Returns:
        tuple of int or str: predicted label(s) for texts with unknown authors

    """
    # TODO: ADD YOUR CODE HERE

    train = np.array(extract_features(texts_known_authors))
    test = np.array(extract_features(texts))
    y = np.array(known_authors)
    clf = sklearn.svm.SVC(kernel='poly')
    clf.fit(train,y)
    #print(sklearn.metrics.accuracy_score(known_authors, clf.predict(train)))
    return clf.predict(test)


# DO NOT EDIT CODE BELOW THIS LINE


import os
import unittest
import zipfile


_UNIVERSAL_TAGS_COUNT = 12
_PENN_TREEBANK_TAGS_COUNT = 36


class TestAssignment7(unittest.TestCase):

    #===========================================================================
    # def setUp(self):
    #     corpus_filename = os.path.join(os.path.dirname(__file__), 'data', 'brennan-greenstadt-corpus.zip')
    #     self.texts_known_authors = []
    #     self.known_authors = []
    #     with zipfile.ZipFile(corpus_filename, 'r') as myzip:
    #         for filepath in sorted(myzip.namelist()):
    #             filename = os.path.basename(filepath)
    #             if not filename.startswith(('a_', 'c_')):
    #                 continue
    #             if 'imitation' in filename or 'obfuscation' in filename:
    #                 continue
    #             self.known_authors.append(filename[0])  # 'a' or 'c'
    #             text = myzip.open(filepath, 'r').read().decode('latin1')
    #             self.texts_known_authors.append(text)
    #===========================================================================

    def test_character_count1(self):
        self.assertGreater(character_count('chairs have legs.'), 0)

    def test_average_characters_per_word1(self):
        self.assertGreater(average_characters_per_word('chairs have legs.'), 3)

    def test_character_frequency1(self):
        self.assertEqual(sum(character_frequency('chairs')), 6)

    #===========================================================================
    # def test_character_2gram_frequency(self):
    #     # answer may vary (slightly) depending on how function is implemented
    #     freq = character_2gram_frequency('chairs')
    #     self.assertGreaterEqual(sum(freq), 5)
    #     self.assertLessEqual(sum(freq), 7)
    #===========================================================================

    def test_pos_tag_frequency1(self):
        # answer may vary (slightly) depending on how function is implemented
        freq = pos_tag_frequency('Chairs have legs.')
        self.assertGreaterEqual(sum(freq), 3)
        self.assertLessEqual(sum(freq), 5)

    def test_pos_tag_2gram_frequency1(self):
        # answer may vary (slightly) depending on how function is implemented
        freq = pos_tag_2gram_frequency('Chairs have legs.')
        self.assertGreaterEqual(sum(freq), 2)
        self.assertLessEqual(sum(freq), 5)

    #===========================================================================
    # def test_predict_author_many1(self):
    #     texts = [self.texts_known_authors[0]]
    #     authors = [self.known_authors[0]]
    #     # target text is included as part of training, should be easy
    #     authors_pred = predict_author_many(texts, self.texts_known_authors, self.known_authors)
    #     self.assertGreater(len(authors_pred), 0)
    #     self.assertEqual(authors[0], authors_pred[0])
    #===========================================================================


if __name__ == '__main__':
    unittest.main()

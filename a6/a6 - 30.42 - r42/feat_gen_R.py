#!/bin/python

from dateutil.parser import parse
from nltk.corpus import stopwords
import string
stop_words = set(stopwords.words('english'))

def containDate(string):
    try:
        parse(string)
        return True
    except ValueError:
        return False


def preprocess_corpus(train_sents):
    """Use the sentences to do whatever preprocessing you think is suitable,
    such as counts, keeping track of rare features/words to remove, matches to lexicons,
    loading files, and so on. Avoid doing any of this in token2features, since
    that will be called on every token of every sentence.

    Of course, this is an optional function.

    Note that you can also call token2features here to aggregate feature counts, etc.
    """
    #print 1
    def removeStopWords(train_sents):
        #print 2
        resultwords = []
        stop_words = set(stopwords.words('english'))
        # print "text before===",text
        for k in train_sents:
            for ii in k:
                # print ii
                if ii.lower() in stop_words:
                    k.remove(ii)
        # text = ' '.join(resultwords)
        print train_sents
        print "DONE REMOVING STOP WORDS"

    def reomovePunctuation(train_sents):
        for x in train_sents:
            x = [''.join(c for c in s if c not in string.punctuation) for s in x]
            x = [s for s in x if s]
        print train_sents
        print "Done removing Punctuation"

    removeStopWords(train_sents)
    reomovePunctuation(train_sents)

    import os
    direc = "./data/lexicon"
    ext = '.txt'
    file_dict = {}
    txt_files = [i for i in os.listdir(direc)]
    print txt_files
    for f in txt_files:
        # Open them and assign them to file_dict
        with open(os.path.join(direc, f)) as file_object:
            file_dict[f] = file_object.read()

def token2features(sent, i, add_neighs = True):
    """Compute the features of a token.

    All the features are boolean, i.e. they appear or they do not. For the token,
    you have to return a set of strings that represent the features that *fire*
    for the token. See the code below.

    The token is at position i, and the rest of the sentence is provided as well.
    Try to make this efficient, since it is called on every token.

    One thing to note is that it is only called once per token, i.e. we do not call
    this function in the inner loops of training. So if your training is slow, it's
    not because of how long it's taking to run this code. That said, if your number
    of features is quite large, that will cause slowdowns for sure.

    add_neighs is a parameter that allows us to use this function itself in order to
    recursively add the same features, as computed for the neighbors. Of course, we do
    not want to recurse on the neighbors again, and then it is set to False (see code).
    """
    ftrs = []
    # bias
    ftrs.append("BIAS")
    # position features
    if i == 0:
        ftrs.append("SENT_BEGIN")
    if i == len(sent)-1:
        ftrs.append("SENT_END")

    # the word itself
    word = unicode(sent[i])
    ftrs.append("WORD=" + word)
    ftrs.append("LCASE=" + word.lower())
    # some features of the word
    if word.isalnum():
        ftrs.append("IS_ALNUM")
    if word.isnumeric():
        ftrs.append("IS_NUMERIC")
    if word.isdigit():
        ftrs.append("IS_DIGIT")
    if word.isupper():
        ftrs.append("IS_UPPER")
    if word.islower():
        ftrs.append("IS_LOWER")
    # ************************************************
    if len(word) > 15:
        ftrs.append("IS_LENGTHY")
    if word[0].upper():
        ftrs.append("IS_FIRST_UPPER")
    if word.containDate():
        ftrs.append("IS_DATE")
    if word.__contains__("http"):
        ftrs.append("IS_HYPERLINK")





    # previous/next word feats
    if add_neighs:
        if i > 0:
            for pf in token2features(sent, i-1, add_neighs = False):
                ftrs.append("PREV_" + pf)
        if i < len(sent)-1:
            for pf in token2features(sent, i+1, add_neighs = False):
                ftrs.append("NEXT_" + pf)

    # return it!
    return ftrs

if __name__ == "__main__":
    sents = [
    [ "I", "love", "food" ,"Reshmabhatia","??","Hello?","@joshHnumber1fan"]
    ]
    preprocess_corpus(sents)
    print sents
    # for sent in sents:
    #     for i in xrange(len(sent)):
    #         print sent[i], ":", token2features(sent, i)

#!/bin/python

from dateutil.parser import parse
from nltk.corpus import stopwords
import nltk
import string
from os import listdir, getcwd, path
import operator

stop_words = set(stopwords.words('english'))

global lookupLexiconDict

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
    global lookupLexiconDict
    lookupLexiconDict = {}
    
    lexiconDir = getcwd()+'\\data\\lexicon'
    filesList = [hfile for hfile in listdir(lexiconDir) if path.isfile(lexiconDir+'\\'+hfile) ]
    
    fileMappingDict = \
        {
        'architecture.museum':'facility',
        'automotive.make':'product',
        'automotive.model':'product',
        'award.award':'musicartist',
        'base.events.festival_series':'geo-loc',
         #'bigdict':'@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@',
        'book.newspaper':'company',
        'broadcast.tv_channel':'tvshow',
        'business.brand':'company',
        'business.consumer_company':'company',
        'business.consumer_product':'product',
        'business.sponsor':'company',
        'cap.1000':'geo-loc',
        'cvg.computer_videogame':'product',
        'cvg.cvg_developer':'company',
        'cvg.cvg_platform':'product',
        'education.university':'facility',
        'english.stop':'O',
        'firstname.5k':'person',
        'government.government_agency':'company',
        'internet.website':'company',
        'lastname.5000':'person',
        'location':'geo-loc',
        'location.country':'geo-loc',
        'lower.5000':'O',
        'people.family_name':'person',
        'people.person':'person',
        'people.person.lastnames':'person',   # <-----------------------------
        'product':'product',
        'sports.sports_league':'sportsteam',
        'sports.sports_team':'sportsteam',
        'time.holiday':'O',
        'time.recurring_event':'O',
        'transportation.road':'geo-loc',
        'tv.tv_network':'tvshow',
        'tv.tv_program':'tvshow',
        'venture_capital.venture_funded_company':'company',
        'venues':'geo-loc'
        }

    for lexFile in filesList:
        if lexFile not in fileMappingDict: continue
        print 'Processing ', lexFile
        
        with open(lexiconDir+'\\'+lexFile) as f:
            for line in f:
                line = line.lower().split()
                if len(line) == 1: low=0
                else:low=1
                for i in range(low,len(line)):
                    key = tuple(line[:i+1])
                    if key not in lookupLexiconDict:
                        lookupLexiconDict[key] = [fileMappingDict[lexFile]]
                    else:
                        lookupLexiconDict[key].append(fileMappingDict[lexFile])  

        
    #pass        

def token2features(sent, i, add_neighs=True):
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
    
    def add_lexicon_feats(tpl, lookupLexiconDict, usedTags):
        if tpl in lookupLexiconDict:
            for cls in lookupLexiconDict[tpl]:
                if cls not in usedTags:
                    ftrs.append(cls)              #<--------------------
                    usedTags[cls]=1
                else:
                    usedTags[cls]+=1
             
    
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
    word_lcase = word.lower()
    ftrs.append("LCASE=" + word_lcase)
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

    # USE LEXICONS################################################## !
    maxTries=5
    usedTags = {}
    
    #look front up to 5 places    
    if type(sent[0])== str: lSent = map(str.lower, sent)
    else:   lSent = map(unicode.lower, sent)
    while(maxTries!=0):

        if len(lSent)-i>=maxTries:
            tpl = tuple(lSent[i:maxTries+i])
            add_lexicon_feats(tpl, lookupLexiconDict, usedTags)
        maxTries-=1
    
    #also look backwards: lexicons
    #===========================================================================
    # if i>=1:
    #     tpl = tuple(lSent[i-1:i+1])  # size 2
    #     add_lexicon_feats(tpl, lookupLexiconDict, usedTags)
    #     if i<len(lSent) : 
    #         tpl = tuple(lSent[i-1:i+2])  # size 3
    #         add_lexicon_feats(tpl, lookupLexiconDict, usedTags)
    #===========================================================================
            
    #analyze and add bias towards max used classification  
    if usedTags:
        usedTags = list(usedTags.iteritems())
        maxused = max(usedTags, key=operator.itemgetter(1))
        minused = min(usedTags, key=operator.itemgetter(1))    
        if minused[1]!=maxused[1]:
            ftrs.append('BIAS='+maxused[0])
            

    #R ************************************************
    if len(word) > 15:
        ftrs.append("IS_LENGTHY")
    if word[0].upper():
        ftrs.append("IS_FIRST_UPPER")
    if word.__contains__("http"):
        ftrs.append("IS_HYPERLINK")
    if any(x.isupper() for x in word):
        ftrs.append("IS_MIXEDCASE")
    if word.isupper():
        ftrs.append("ALL_UPPERCASE")
    if word.__contains__("@"):
        ftrs.append("IS_TAG")
    if word.__contains__("#"):
        ftrs.append("IS_HASHTAG")
    if word in stop_words:
        ftrs.append("IS_STOPWORD")
    if word in ['ing','ly','ed','ious','ies','ive','es','s','ment']:
        ftrs.append("CONTAINS_SUFFIX")
    ftrs.append( nltk.pos_tag([word])[0][1] )

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
        ["I", "love", "food",'Consultants','Awards']
    ]
    preprocess_corpus(sents)
    print sents
    for sent in sents:
        for i in xrange(len(sent)):
            print sent[i], ":", token2features(sent, i)

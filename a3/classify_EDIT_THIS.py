#!/usr/bin/env python
from collections import defaultdict
from csv import DictReader, DictWriter

import nltk
import codecs
import sys
from nltk.corpus import wordnet as wn
from nltk.tokenize import TreebankWordTokenizer
import string
from string import punctuation

kTOKENIZER = TreebankWordTokenizer()

def morphy_stem(word):
    """
    Simple stemmer
    """
    stem = wn.morphy(word)
    if stem:
        return stem.lower()
    else:
        return word.lower()

class FeatureExtractor:
    

    def __init__(self):
        """
        You may want to add code here
        """
        self.lookup_punctuation = set(punctuation)
        self.lookup_uppercase = set(string.ascii_uppercase)
        self.lookup_lowercase = set(string.ascii_lowercase)
        self.lookup_digits = set(string.digits)
        self.stop_words = set(nltk.corpus.stopwords.words('english'))
        self.tagVector = ['NOUN','PRON','VERB','ADV','ADJ','ADP','CONJ','PRT','DET','NUM','X','.']
        None
    
    def f1_char_count(self,text, existingVector):
        existingVector['char_count'] = len(text.replace(' ', ''))
        
    def f2_avg_chars_per_word(self,text, existingVector):
        if 'char_count' in existingVector:
            existingVector['avg_chars'] = existingVector['char_count'] / len(text.split())*100/len(text)
    
    def f3_no_of_digits(self,text, existingVector):
        existingVector['digit_count'] = sum([char in self.lookup_digits for char in text])*100/len(text)
    
    def f4_uppercases(self,text, existingVector):
        existingVector['upper_count'] =  sum([char in self.lookup_uppercase for char in text])*100/len(text)
    
    def f5_special_chars(self,text, existingVector):
        
        for char in text:
            if char in self.lookup_punctuation: 
                existingVector[char] += 10

    def f6_char_frequency(self, text, existingVector):  
        
        for char in text:
            if char in self.lookup_lowercase: existingVector[char] += 1

    def f7_digit_frequency(self,text, existingVector):
        
        for char in text:
            if char in self.lookup_digits: existingVector[char] += 1
 
    def f8_smaller_words(self, text, existingVector):
        
        for word in text.split():
            if len(word) <= 3: existingVector[word]+=1

    def f9_single_to_double_word_ratio(self, text, existingVector):
          
        freq = nltk.FreqDist(word for word in text.split())
        single_wcnt = len( [key for key,val in freq.items() if val<=2])
        double_wcnt = len( [key for key,val in freq.items() if val>2])
        if double_wcnt == 0: existingVector['single_to_double_count'] = 0
        else:existingVector['single_to_double_count'] = float(single_wcnt) / double_wcnt *10
    
    def f10_parts_of_speech(self, text, existingVector):
        
        words = nltk.word_tokenize(text)
        word_pos_tuple = nltk.pos_tag(words, tagset='universal')
        
        prevPos = None
        for word, pos in word_pos_tuple:
            existingVector[pos]+=1
    
    def f11_large_word_count(self, text, existingVector):
        
        large_wcnt = 0  
        for word in kTOKENIZER.tokenize(text): 
            if len(word)>4: large_wcnt+=1

        existingVector['single_to_double_count'] = large_wcnt *10
        
    def f12_consecutive_commas(self,text, existingVector):
        existingVector['comma_bias'] =0  
        for char in text:
            if char == ',': existingVector['comma_bias'] +=1
        
        if existingVector['comma_bias'] > 1: existingVector['comma_bias']=10
        else: existingVector['comma_bias']=0 

        
        
    def features(self, text):
        existingVector = defaultdict(int)
        for ii in kTOKENIZER.tokenize(text):
            existingVector[ morphy_stem(ii) ] += 1
            
        self.f1_char_count(text, existingVector)
        self.f2_avg_chars_per_word(text, existingVector) 
        self.f3_no_of_digits(text, existingVector)
        self.f4_uppercases(text, existingVector)
        self.f5_special_chars(text, existingVector)
        #self.f6_char_frequency(text, existingVector)
        self.f7_digit_frequency(text, existingVector)
        self.f8_smaller_words(text, existingVector)
        self.f9_single_to_double_word_ratio(text, existingVector)
        self.f10_parts_of_speech(text, existingVector) 
        self.f11_large_word_count(text, existingVector)
        #self.f12_consecutive_commas(text, existingVector)
        return existingVector
    
reader = codecs.getreader('utf8')
writer = codecs.getwriter('utf8')


def prepfile(fh, code):
  if type(fh) is str:
    fh = open(fh, code)
  ret = gzip.open(fh.name, code if code.endswith("t") else code+"t") if fh.name.endswith(".gz") else fh
  if sys.version_info[0] == 2:
    if code.startswith('r'):
      ret = reader(fh)
    elif code.startswith('w'):
      ret = writer(fh)
    else:
      sys.stderr.write("I didn't understand code "+code+"\n")
      sys.exit(1)
  return ret

if __name__ == "__main__":

    trainfile = prepfile('train.tsv', 'r')
    testfile = None             #testfile = prepfile(args.testfile, 'r')
    outfile = prepfile('resultClassify.tsv', 'w')
    args_subsample = 1.0
    
    # Create feature extractor (you may want to modify this)
    fe = FeatureExtractor()
    
    # Read in training data
    train = DictReader(trainfile, delimiter='\t')
    
    # Split off dev section
    dev_train = []
    dev_test = []
    full_train = []
    AP_TRAIN_LIST = []
    for ii in train:
        if args_subsample < 1.0 and int(ii['id']) % 100 > 100 * args_subsample:
            continue
        feat = fe.features(ii['text'])
        if int(ii['id']) % 5 == 0:
            dev_test.append((feat, ii['cat']))
            AP_TRAIN_LIST.append([ii['text'], ii['cat']])
        else:
            dev_train.append((feat, ii['cat']))
            
            
        full_train.append((feat, ii['cat']))

    # Train a classifier
    sys.stderr.write("Training classifier ...\n")
    classifier = nltk.classify.NaiveBayesClassifier.train(dev_train)
    
    import csv
    ANAND_writer = csv.writer(open('ANAND_INCORRECT_RESULTS_TEST.csv','wb'),delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    ANAND_index = 0
    
    right = 0
    total = len(dev_test)
    for ii in dev_test:
        prediction = classifier.classify(ii[0])
        if prediction == ii[1]:
            right += 1
        else:
            ANAND_writer.writerow(AP_TRAIN_LIST[ANAND_index]+[prediction])
        ANAND_index+=1    
    sys.stderr.write("Accuracy on dev: %f\n" % (float(right) / float(total)))

    if testfile is None:
        sys.stderr.write("No test file passed; stopping.\n")
    else:
        # Retrain on all data
        classifier = nltk.classify.NaiveBayesClassifier.train(dev_train + dev_test)

        # Read in test section
        test = {}
        for ii in DictReader(testfile, delimiter='\t'):
            test[ii['id']] = classifier.classify(fe.features(ii['text']))

        # Write predictions
        o = DictWriter(outfile, ['id', 'pred'])
        o.writeheader()
        for ii in sorted(test):
            o.writerow({'id': ii, 'pred': test[ii]})

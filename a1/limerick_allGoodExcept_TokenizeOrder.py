#!/usr/bin/env python
import argparse
import sys
import codecs
if sys.version_info[0] == 2:
    from itertools import izip
else:
    izip = zip
from collections import defaultdict as dd
import re
import os.path
import gzip
import tempfile
import shutil
import atexit

# https://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string-in-python
from string import punctuation

import nltk

# Use word_tokenize to split raw text into words
from nltk.tokenize import word_tokenize



scriptdir = os.path.dirname(os.path.abspath(__file__))


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

def addonoffarg(parser, arg, dest=None, default=True, help="TODO"):
  ''' add the switches --arg and --no-arg that set parser.arg to true/false, respectively'''
  group = parser.add_mutually_exclusive_group()
  dest = arg if dest is None else dest
  group.add_argument('--%s' % arg, dest=dest, action='store_true', default=default, help=help)
  group.add_argument('--no-%s' % arg, dest=dest, action='store_false', default=default, help="See --%s" % arg)



class LimerickDetector:

    def __init__(self):
        """
        Initializes the object to have a pronunciation dictionary available
        """
        self._pronunciations = nltk.corpus.cmudict.dict()


    def num_syllables(self, word):
        """
        Returns the number of syllables in a word.  If there's more than one
        pronunciation, take the shorter one.  If there is no entry in the
        dictionary, return 1.
        """

        if word in self._pronunciations:
            
            shorterLengthPronc = self._pronunciations[word][0]
            for proncn in self._pronunciations[word]:
                if len(proncn) < shorterLengthPronc:
                    shorterLengthPronc = proncn
            
            syllbs = [ x for x in shorterLengthPronc if len(x)==3]
            return len(syllbs)
        else:                
            return 1


    def rhymes(self, a, b):
        """
        Returns True if two words (represented as lower-case strings) rhyme,
        False otherwise.
        """

        # WHAT IF - A WORD IS NOT FOUND IN DICTIONARY ??????????
        def vowelStartsAt(l):
            for index in range(len(l)): 
                if len(l[index] ) == 3: return index
            return -1
                
        def soundsMatch(clippedSoundList1, clippedSoundList2):  
            reversedList1 = list( reversed(clippedSoundList1))  # reverse, to check in reverse
            reversedList2 = list( reversed(clippedSoundList2))
            smallerList = None; largerList = None
            if len(reversedList1) < len(reversedList2): smallerList = reversedList1; largerList = reversedList2
            else: smallerList = reversedList2; largerList = reversedList1
                
            if smallerList == largerList[: len(smallerList)]:return True # 1-1 sound compare        
            return False    
            
        a=a.lower(); b=b.lower()
        if a in self._pronunciations:  ListOf_Prlists_a = self._pronunciations[a] 
        else: ListOf_Prlists_a = []
        if b in self._pronunciations:  ListOf_Prlists_b = self._pronunciations[b] 
        else: ListOf_Prlists_b = []
            
        for pra in ListOf_Prlists_a:
            for prb in ListOf_Prlists_b:
                a_vStart = vowelStartsAt(pra)
                b_vStart = vowelStartsAt(prb)

                if soundsMatch(pra[a_vStart:], prb[b_vStart:]): 
                    return True            
        return False        

        
    def is_limerick(self, text):
        """
        Takes text where lines are separated by newline characters.  Returns
        True if the text is a limerick, False otherwise.

        A limerick is defined as a poem with the form AABBA, where the A lines
        rhyme with each other, the B lines rhyme with each other, and the A lines do not
        rhyme with the B lines.


        Additionally, the following syllable constraints should be observed:
          * No two A lines should differ in their number of syllables by more than two.
          * The B lines should differ in their number of syllables by no more than two.
          * Each of the B lines should have fewer syllables than each of the A lines.
          * No line should have fewer than 4 syllables

        (English professors may disagree with this definition, but that's what
        we're using here.)
    
        """
        # TODO: provide an implementation!
        
        def getTotalSyllCount(wordList):
            syllCount = 0
            for word in wordList:
                syllCount+=self.num_syllables(word)
            return syllCount    
        
        def check2SyllGap(syllCountList):
            base = syllCountList[0]
            for index in range( len(syllCountList)):
                if abs( base - syllCountList[index]) > 2: return False
                base = syllCountList[index]
            return True
                
        linesList = text.split('\n')
        linesList = [line for line in linesList if line.strip() != '' ]
        if len(linesList) != 5: return False    # edge case 0 .............. IS 5 OKAY ?????????????????????????????
        
        cleansedLinesList = map( lambda line: line.translate(None, punctuation) , linesList)
        
        A_lines = [cleansedLinesList[i] for i in [0,1,4]]  ################ impacted by 4 lines ????????????????????
        B_lines = [cleansedLinesList[i] for i in [2,3]]

        A_lines_tokenized = map ( lambda line : word_tokenize(line), A_lines )
        B_lines_tokenized = map ( lambda line : word_tokenize(line), B_lines )
        
        A_lines_syll_count = sorted( map ( lambda chosenLine_WordList :getTotalSyllCount( chosenLine_WordList) ,  A_lines_tokenized))
        B_lines_syll_count = sorted( map ( lambda chosenLine_WordList :getTotalSyllCount( chosenLine_WordList) ,  B_lines_tokenized))
        
        #####################################################################
        
        if not ( check2SyllGap(A_lines_syll_count) and check2SyllGap(B_lines_syll_count) ):  # edge case 1, 2
            return False
        
        if A_lines_syll_count[0] <= B_lines_syll_count[-1]:  # B's highest must be lower than A's lowest  - edge case 3
            return False
        
        if A_lines_syll_count[0] < 4 or B_lines_syll_count[0] < 4:  # edge case 4
            return False  
        
        A_lines_rhymes = map ( lambda wordList: wordList[-1], A_lines_tokenized)   # get last word of each line
        B_lines_rhymes = map ( lambda wordList: wordList[-1], B_lines_tokenized)
        
        A_Rhymes_Status = self.rhymes( A_lines_rhymes[0], A_lines_rhymes[1])
        B_Rhymes_Status = self.rhymes( B_lines_rhymes[0], B_lines_rhymes[1])
        if len(A_lines_rhymes) == 3:
            A_Rhymes_Status  = A_Rhymes_Status and \
                                self.rhymes( A_lines_rhymes[0], A_lines_rhymes[2]) and \
                                self.rhymes( A_lines_rhymes[1], A_lines_rhymes[2])
             
        return A_Rhymes_Status and B_Rhymes_Status
    
# The code below should not need to be modified
def main():
  parser = argparse.ArgumentParser(description="limerick detector. Given a file containing a poem, indicate whether that poem is a limerick or not",
                                   formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  addonoffarg(parser, 'debug', help="debug mode", default=False)
  parser.add_argument("--infile", "-i", nargs='?', type=argparse.FileType('r'), default=sys.stdin, help="input file")
  parser.add_argument("--outfile", "-o", nargs='?', type=argparse.FileType('w'), default=sys.stdout, help="output file")




  try:
    args = parser.parse_args()
  except IOError as msg:
    parser.error(str(msg))

  infile = prepfile(args.infile, 'r')
  outfile = prepfile(args.outfile, 'w')

  ld = LimerickDetector()
  lines = ''.join(infile.readlines())
  outfile.write("{}\n-----------\n{}\n".format(lines.strip(), ld.is_limerick(lines)))

if __name__ == '__main__':
  main()

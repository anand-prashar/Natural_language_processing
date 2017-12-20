'''
Created on Oct 27, 2017

@author: anand
'''

import gensim
import logging
from os import getcwd


def readFile(reasoningFile):
    
    reasoningData = set()
    with open(reasoningFile) as f:
        key = None
        for line in f:
            if len(line)==0 or line[:2] == '//': continue
            if line[0] == ':': 
                key = line[2:].strip() 
                continue
            if key == None:
                print 'Invalid file format'; exit
            
            reasoningData.update( set([word.strip() for word in line.split(' ') if word!='']) )
    
    reasoningData = list(reasoningData)        
    
    return reasoningData   



# Logging code taken from http://rare-technologies.com/word2vec-tutorial/
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# Load Google's pre-trained Word2Vec model.
model = gensim.models.KeyedVectors.load_word2vec_format('C:\\Users\\anand\\Downloads\\word2Vec\\file.bin', binary=True)  

# Does the model include stop words?
print("Does it include the stop words like \'a\', \'and\', \'the\'? %d %d %d" % ('a' in model.vocab, 'and' in model.vocab, 'the' in model.vocab))

# Retrieve the entire list of "words" from the Google Word2Vec model, and write
# these out to text files so we can peruse them.
vocab = model.vocab.keys()

fileNum = 1
print 'STARTED'
wordsInVocab = len(vocab) /10 #anand
wordsPerFile = int(100E3)

print 'STARTING PRINT'

opFile = open('ANAND_W2Vec','wb')

for word in readFile('C:\\Users\\anand\\Google Drive\\Eclipse-O-ws\\CSC_544_NLP\\a5\\word-test.v3.txt'):
    #word = line.split(' ')[0]
    print 'WORD=>', word
    vectr =model[ word ]
    opFile.write(word+' '+str(vectr)[1:-1])
        
opFile.close()
print 'DONE'
#===============================================================================
# wv = model['information']
# 
# 
# print 'Length is ',len(wv)
# 
# print wv.shape
#===============================================================================

#===============================================================================
# for i in wv:
#     print wv
#===============================================================================

    
#===============================================================================
# # Write out the words in 100k chunks.
# for wordIndex in range(0, wordsInVocab, wordsPerFile):
#     # Write out the chunk to a numbered text file.    
#     with open(getcwd()+"\\vocabulary\\vocabulary_%.2d.txt" % fileNum, 'w') as f:
#         # For each word in the current chunk...        
#         for i in range(wordIndex, wordIndex + wordsPerFile):
#             # Write it out and escape any unicode characters.            
#             f.write(vocab[i].encode('UTF-8') + '\n')
#     
#     fileNum += 1
# print 'DONEEEEEEEEEEEE'   
#===============================================================================

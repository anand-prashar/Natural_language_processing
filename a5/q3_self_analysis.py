'''
Created on Oct 15, 2017

@author: anand
'''
import distsim
word_to_ccdict = distsim.load_contexts("nytcounts.4k")
print "Cosine similarity between cat and dog" ,distsim.cossim_sparse(word_to_ccdict['cat'],word_to_ccdict['dog'])
print "Cosine similarity between cat and university" ,distsim.cossim_sparse(word_to_ccdict['cat'],word_to_ccdict['university'])
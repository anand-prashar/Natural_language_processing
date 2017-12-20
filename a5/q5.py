#!/usr/bin/env python
import distsim
# you may have to replace this line if it is too slow 
word_to_vec_dict = distsim.load_word2vec("nyt_word2vec.4k")


### provide your answer below
experiment_list = ['edward','school','red','saved',  'eyebrows','church']
###Answer examples

for e_word in experiment_list:
    print 'Experiment =',e_word
    if e_word not in word_to_vec_dict: 
        print e_word ,' does not exist in lookup dictionary'; continue
    for i, (word, score) in enumerate( distsim.show_nearest(word_to_vec_dict, word_to_vec_dict[e_word],set([e_word]),distsim.cossim_dense), start=1):
        print("{}: {} ({})".format(i, word, score))  
    
    print '\n---------------------------------------------\n'    


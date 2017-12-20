from __future__ import division
import sys,json
import os
import numpy as np
from math import sqrt

def load_word2vec(filename):
    # Returns a dict containing a {word: numpy array for a dense word vector} mapping.
    # It loads everything into memory.
    
    w2vec={}
    with open(filename,"r") as f_in:
        for line in f_in:
            line_split=line.replace("\n","").split()
            w=line_split[0]
            vec=np.array([float(x) for x in line_split[1:]])
            w2vec[w]=vec
    return w2vec

def load_contexts(filename):
    # Returns a dict containing a {word: contextcount} mapping.
    # It loads everything into memory.

    data = {}
    for word,ccdict in stream_contexts(filename):
        data[word] = ccdict
    print "file %s has contexts for %s words" % (filename, len(data))
    return data

def stream_contexts(filename):
    # Streams through (word, countextcount) pairs.
    # Does NOT load everything at once.
    # This is a Python generator, not a normal function.
    for line in open(filename):
        word, n, ccdict = line.split("\t")
        n = int(n)
        ccdict = json.loads(ccdict)
        yield word, ccdict

def cossim_sparse(v1,v2):
    # Take two context-count dictionaries as input
    # and return the cosine similarity between the two vectors.
    # Should return a number beween 0 and 1

    ## TODO: delete this line and implement me
    
    if type(v1)  == np.ndarray and type(v2) == np.ndarray:
        return cossim_dense(v1, v2)
    
    dot_prod = 0; mod_v1 = 0; mod_v2 = 0
    
    for word,count in v1.iteritems():
        if word in v2:
            dot_prod+=count * v2[word]
        mod_v1+=pow( count, 2)   
    
    for word, count in v2.iteritems():
        mod_v2+=pow( count, 2)
    
    mod_v1 = sqrt(mod_v1)
    mod_v2 = sqrt(mod_v2)
    
    if mod_v1!=0 and mod_v2!=0:
        return dot_prod/(mod_v1*mod_v2)
    return 0   

def cossim_dense(v1,v2):
    # v1 and v2 are numpy arrays
    # Compute the cosine simlarity between them.
    # Should return a number between -1 and 1
    
    ## TODO: delete this line and implement me
    if type(v1) == dict and type(v2) == dict:
        return cossim_sparse(v1, v2)

    assert len(v1) == len(v2)
    
    dot_prod = np.dot(v1,v2)
    mod_v1 = np.linalg.norm(v1)
    mod_v2 = np.linalg.norm(v2)
    
    if mod_v1!=0 and mod_v2!=0:
        return dot_prod/(mod_v1*mod_v2)
    return 0  

def show_nearest2(word_2_vec, w_vec, exclude_w, sim_metric):
    #word_2_vec: a dictionary of word-context vectors. The vector could be a sparse (dictionary) or dense (numpy array).
    #w_vec: the context vector of a particular query word `w`. It could be a sparse vector (dictionary) or dense vector (numpy array).
    #exclude_w: the words you want to exclude in the responses. It is a set in python.
    #sim_metric: the similarity metric you want to use. It is a python function
    # which takes two word vectors as arguments.

    # return: an iterable (e.g. a list) of up to 10 tuples of the form (word, score) where the nth tuple indicates the nth most similar word to the input word and the similarity score of that word and the input word
    # if fewer than 10 words are available the function should return a shorter iterable
    #
    # example:
    #[(cat, 0.827517295965), (university, -0.190753135501)]
    
    match_list = []
    most_similar = word_2_vec.similar_by_vector(w_vec, topn=15)
    
    for tpl in most_similar:
        if tpl[0] not in exclude_w: match_list.append(tpl)
        
    match_list = sorted( match_list, key = lambda x: x[1], reverse = True)
    
    if len(match_list)>10: return match_list[:10]
    return match_list

    
def show_nearest(word_2_vec, w_vec, exclude_w, sim_metric):
    #word_2_vec: a dictionary of word-context vectors. The vector could be a sparse (dictionary) or dense (numpy array).
    #w_vec: the context vector of a particular query word `w`. It could be a sparse vector (dictionary) or dense vector (numpy array).
    #exclude_w: the words you want to exclude in the responses. It is a set in python.
    #sim_metric: the similarity metric you want to use. It is a python function
    # which takes two word vectors as arguments.

    # return: an iterable (e.g. a list) of up to 10 tuples of the form (word, score) where the nth tuple indicates the nth most similar word to the input word and the similarity score of that word and the input word
    # if fewer than 10 words are available the function should return a shorter iterable
    #
    # example:
    #[(cat, 0.827517295965), (university, -0.190753135501)]
    
    match_list = []
    for another_word, another_vector in word_2_vec.iteritems():
        if another_word not in exclude_w and type(w_vec) == type(another_vector):
            match_list.append( (another_word, sim_metric(w_vec, another_vector)) )
        
    match_list = sorted( match_list, key = lambda x: x[1], reverse = True)
    
    if len(match_list)>10: return match_list[:10]
    return match_list

if __name__ == '__main__':
    pass
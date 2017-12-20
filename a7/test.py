'''
Created on Dec 1, 2017

@author: anand
'''

def word_matches(h, ref):
    return sum(1 for w in h if w in ref)

def sup(h, ref):
    bi_h = create2grams(h)
    bi_ref = create2grams(ref)
    bi_ref_set = set(bi_ref)
    return word_matches(bi_h, bi_ref_set)
    
    
    
    



def create2grams(sample_list):
    res=[]
    if len(sample_list)==1 :
        return sample_list
    for i in range(len(sample_list)):
        if (i!=len(sample_list)-1):
            res.append(sample_list[i]+" "+sample_list[i+1])
            #print i
    return res







h1=  ['Republican', 'leaders', 'justify', 'its', 'policy', 'necessary', 'to', 'combat', 'electoral', 'fraud.']
h2= ['Republican', 'leaders', 'justify', 'its', 'policy', 'of', 'necessity', 'in', 'the', 'fight', 'against', 'electoral', 'fraud.']     
ref = ['Republican', 'leaders', 'justified', 'their', 'policy', 'by', 'the', 'need', 'to', 'combat', 'electoral', 'fraud.']
sup(h1,h2,ref)
#create2grams(h1)
'''
Created on Oct 3, 2017

@author: anand
'''

from __future__ import division
from tree import Tree
from bigfloat import bigfloat,log10

data=[]
with open('train.trees.pre.unk') as filestream:
    #for line in filestream:
    data = [line.rstrip('\n') for line in filestream]




datanew=[]
for line in data:
    line=(Tree.from_str(line))
    datanew.append(line)

#print datanew
grammar_dict={}
for tree in datanew:
    #print tree
    nodes=tree.bottomup()
    for node in nodes:
        #print 'current node:',node.label
        children=node.children
        if children == []: continue
        root=node.label
        #print 'Root is:',root
        childName=' '
        for child in children:
            childName +=child.label
            childName += ' '
        #print childName
        if root+' ->'+childName in grammar_dict:
            grammar_dict[root+' ->'+childName] += 1
        else:
            grammar_dict[root+' ->'+childName] = 1

print grammar_dict
print 'Unique Grammar Rules=',len(grammar_dict.keys())
new= [key for key, val in grammar_dict.iteritems() if val == max(grammar_dict.values())]
for items in new:
    print "Most Frequent Rule is:-",items,"and the count is=",grammar_dict[items]


keys=grammar_dict.keys()


def getDenominator(each, keys):
    count = 0
    seach = each.split(' ', 1)
    if(seach[0]=='RB'):
        pass

    # print '&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&'
    # print seach[0]
    for key in keys:
        if seach[0] == key.split(' ', 1)[0]:
            count = count + 1
    return count

prob_dict={}
for each in keys:
    num=grammar_dict[each]
    den=getDenominator(each,keys)
    #print 'num=',num,'den=',den
    #print round((num/den),2)
    prob_dict[each]=log10(bigfloat(float(num/den)))
print '################################################'
#print prob_dict
#print 'prob dict length:',len(prob_dict.keys())

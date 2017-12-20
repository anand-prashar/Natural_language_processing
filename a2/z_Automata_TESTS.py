'''
Created on Sep 13, 2017

@author: anand
'''
import fst
import string, sys
from fsmutils import composechars, trace

def tAutomata():
    f= fst.FST('epsilon_test')
    
    f.add_state('start')
    f.initial_state = 'start'
    f.add_state('1_state')
    f.add_state('ep_final_state')
    
    f.add_state('EPSILON_Intermediate')
    
    #f.set_final('start')
    f.set_final('1_state')
    f.set_final('ep_final_state')
    
    f.add_arc('start','EPSILON_Intermediate',[],['ep_path'])
    
    f.add_arc('EPSILON_Intermediate','ep_final_state',['E'],['ep_to_Final'])
    
    f.add_arc('start','1_state',['1'],['1_path'])
    
    #print f
    return f


tA= tAutomata()
#print trace(tA, ['1'])

print tA.transduce(['E'])    
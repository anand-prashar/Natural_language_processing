'''
Created on Sep 30, 2017

@author: anand
'''

import sys
from tree import Tree
from bigfloat import log10, bigfloat
from nltk import word_tokenize
from time import clock

#################################################

def q1_parse_input_trees(tree_unk_file):
    f=open(tree_unk_file,'r')
    
    
    fileData = f.read()
    data = fileData.split('\n')
    
    inputTrees = []
    for line in data:
        if line=='': continue
        inputTrees.append(Tree.from_str(line) )
    
    rules_dict = {}
    for tree in inputTrees:
        if tree == '': continue   
        
        nodes = tree.bottomup()
        children = None
        
        for node in nodes:   
            children = node.children
            if children == []:  continue
            
            rules_dict.setdefault( str(node),{} )
            # if leaf node(a terminal), add a string else tuple
            right_rule = None
            if len(children[0].children)==0: right_rule = str(children[0])  #<<<<<<<<<---- CONVERT LEAF NODES TO LOWER??
            else: right_rule =  tuple( map(lambda x: str(x), node.children) )    
            
            rules_dict[str(node)].setdefault( right_rule,{'count':0,'probability':0})
            
            rules_dict[str(node)] [right_rule]['count'] +=1
    
    #SMOOTHEN <unk>
    for k,v in rules_dict.iteritems():
        if '<unk>' not in v: 
            rules_dict[k].setdefault( '<unk>',{'count':0,'probability':0})    
            rules_dict[k]['<unk>']['count']+=1
            
    q1_answer=[ [None,[None]],0]
    for left_rule, right_rule in rules_dict.iteritems():
        
        denominator=0
        for r_rule, count_prob_dict in right_rule.iteritems():
            denominator+=count_prob_dict['count']
            
            if count_prob_dict['count'] > q1_answer[1]:
                q1_answer[1] = count_prob_dict['count']
                q1_answer[0][0] = left_rule
                q1_answer[0][1] = r_rule
                
        for r_rule, count_prob_dict in right_rule.iteritems():
            count_prob_dict['probability'] = log10( bigfloat( float(count_prob_dict['count'])/ denominator ) )
    
    print 'QUESTION 1 - Most Frequent Rule: ',q1_answer[0][0],'->',q1_answer[0][1],'    Occcourence =',q1_answer[1]
           
    

            
    
    #===========================================================================
    # import csv
    # with open('Rules.csv','wb') as f:
    #     cw=csv.writer(f,delimiter=',',quoting=csv.QUOTE_ALL)
    #     for k,v in rules_dict.iteritems():
    #         pk=True
    #         for k2,v2 in v.iteritems():
    #             if pk:
    #                 cw.writerow([k,k2,v2])
    #                 pk = False
    #             else: cw.writerow(['',k2,v2])
    #===========================================================================
     
    #print 'CSV PRINTED'   
    return rules_dict
             
 
#########################################################################
        
def cky_unary_filler(cellId, score_dict,backTrack_dict,rules_dict, currentRuleL):
    currentRuleL = (currentRuleL,)
    for unary_key,v in rules_dict.iteritems():
        if currentRuleL in v:
            calcProb = score_dict[cellId][currentRuleL[0]][1] + rules_dict[unary_key][currentRuleL ]['probability']
            score_dict[cellId].setdefault(unary_key, None)
            
            if ( score_dict[cellId][unary_key] == None) or \
                ( calcProb > score_dict[cellId][ unary_key ][1]) :
                    
                    score_dict[cellId][unary_key] = (currentRuleL, calcProb)
                    backTrack_dict[cellId][unary_key] = cellId
            
                    cky_unary_filler(cellId, score_dict,backTrack_dict,rules_dict, unary_key )        
            
           
def CKY_fill_cells_2nd_level_onwards(x,y, rules_dict, score_dict, backTrack_dict):
    hor_cord = (x,x+1)
    ver_cord = (x+1,y)
 
    
    while hor_cord != (x,y):
        
        left_section_list   = score_dict[ hor_cord]
        bottom_section_list = score_dict[ ver_cord]
        
        for left_section, prob_l in left_section_list.iteritems():
            for bottom_section, prob_b in bottom_section_list.iteritems():
                
                for RULE_LHS, RHS in rules_dict.iteritems():
                    if (left_section, bottom_section) in RHS:
                        
                        
                        new_prob = RHS[ (left_section, bottom_section) ]['probability'] +\
                                    prob_l[1] + prob_b[1]
                                    
                        # SHOULD I CHECK IF RULE_LHS already exists, and compare prob before replacing
                        #score_dict[(x, y)].setdefault(RULE_LHS, ())
                        if RULE_LHS not in score_dict[(x, y)] or score_dict[(x, y)][RULE_LHS][1] < new_prob:
                            score_dict[(x, y)][RULE_LHS] = ( (left_section, bottom_section), new_prob )
                            backTrack_dict[(x, y)][RULE_LHS] = (hor_cord, ver_cord)
                            
                            cky_unary_filler( (x, y), score_dict, backTrack_dict, rules_dict, RULE_LHS )
        
        hor_cord = ( hor_cord[0], hor_cord[1]+1 )
        ver_cord = ( ver_cord[0]+1, ver_cord[1] )  
        
#################

 

def CKY(score_dict, backTrack_dict, rules_dict, dev_strings):        
    #dev_strings = 'The flight should be eleven a.m tomorrow .'
    #dev_strings = 'Which is last ?'
    dev_strings = map(lambda x:x ,word_tokenize(dev_strings))  #??????????????
    
    # create matrix
    level_count = len(dev_strings)
    
    for level in range(level_count):
        x = 0
        y = x+(level+1)
        while y<=level_count:
            score_dict.setdefault((x,y), {} )
            backTrack_dict.setdefault((x,y), {} )
            x+=1
            y+=1
    
                         
    for index in range(level_count):
        
        # fill lowest level lexical entries
        terminal_found = False
        for A in rules_dict:
            if dev_strings[index] in rules_dict[A]:  # it will match only for strings as terminals, not tuples which are non-terminals
                score_dict[(index, index+1)].setdefault(A,(None,0))
                backTrack_dict[(index, index+1)].setdefault(A,None)
                terminal = dev_strings[index]
                
                if ( score_dict[(index, index+1)][A][0] == None) or \
                ( score_dict[(index, index+1)][A][1] < rules_dict[A][ terminal ]['probability']) :
                    
                    score_dict[(index, index+1)][A] = (terminal, rules_dict[A][ terminal ]['probability'])
                    backTrack_dict[(index, index+1)][A] = (index)
                    
                    cky_unary_filler( (index, index+1), score_dict,backTrack_dict, rules_dict, A)
                    terminal_found = True
                
                
        if not terminal_found: 
            terminal = '<unk>'  
            for A in rules_dict: 
                if terminal in rules_dict[A]:
                    score_dict[(index, index+1)][A] =( terminal, rules_dict[A][ terminal ]['probability'] ) #right is probability
                    backTrack_dict[(index, index+1)][A] = (index)
                    
                    cky_unary_filler( (index, index+1), score_dict,backTrack_dict, rules_dict, A)
                    
        # unary rules... not needed ?
        # ??? #
    
    # higher order in hierarchy
    for index in range(1, level_count):
        x = 0
        y = x + index+1
        
        while y <= level_count:
            CKY_fill_cells_2nd_level_onwards(x,y, rules_dict, score_dict, backTrack_dict)
            x += 1; y += 1
        
    #print backTrack_dict

def generate_tree(score_dict, backTrack_dict,tokenized_test, nodeId, selectedRuleLHS, POS_levels):
    
    #case 1: hit the leaf
    if type(nodeId) is int: 
        return  tokenized_test[nodeId]   
    
    #case 2: currently at POS tag, whose child is lexeme
    elif type(backTrack_dict[nodeId][ selectedRuleLHS])  is not tuple:
        return  '(' +selectedRuleLHS+' '+tokenized_test[ backTrack_dict[nodeId][ selectedRuleLHS] ] +')'
    
    else:  #a tuple
        
        #case 3: currently at unary hierarchy - 1 child
        if type(backTrack_dict[nodeId][ selectedRuleLHS][0]) is int:
            left_childId  = backTrack_dict[nodeId][ selectedRuleLHS ]
            left_rule  = score_dict[nodeId][ selectedRuleLHS ][0][0]
            return '(' +selectedRuleLHS+' '+generate_tree(score_dict, backTrack_dict, tokenized_test, left_childId, left_rule, POS_levels)  +')' 
        
        #case 4: currently at binary hierarchy - 2 children
        else:
            left_childId  = backTrack_dict[nodeId][ selectedRuleLHS ][0]
            left_rule  = score_dict[nodeId][ selectedRuleLHS ][0][0]
            right_childId = backTrack_dict[nodeId][ selectedRuleLHS ][1]
            right_rule = score_dict[nodeId][ selectedRuleLHS ][0][1]             
            return '('+ selectedRuleLHS +' '+\
                generate_tree(score_dict, backTrack_dict, tokenized_test, left_childId, left_rule, POS_levels)  +' '+\
                generate_tree(score_dict, backTrack_dict, tokenized_test, right_childId, right_rule, POS_levels)  +')'            
    
           

def q2_parse_devtrain_file(rules_dict, tfile):
    
    result = []
    timeTaken = []
    inputStrLength = []
    
    with open(tfile) as f:
        dev_train = f.readlines()
    
    line=0
    line1Prob = None
    
    for test_string in dev_train:
        
        line+=1
        inputStrLength.append(len(test_string))
        startTime = clock()
                
        if test_string == '': continue
        score_dict = {}; backTrack_dict = {}

        CKY(score_dict, backTrack_dict, rules_dict, test_string)

        tokenized_test = word_tokenize(test_string)
        
        #get root node and pass for recursion --------------------------- TO PRINT TREES
        root_rules_List = []
        root = (0, len( tokenized_test))
        for left_rule, right_tuple in score_dict[root].iteritems():
            root_rules_List.append([left_rule, right_tuple])
        
        POS_levels= set()
        for i in range(len(tokenized_test)):
            POS_levels.add((i,i+1))    
        
        if root_rules_List:
            maxRuleLHS = max(root_rules_List, key = lambda value: value[1][1])
            opLine = generate_tree(score_dict, backTrack_dict, tokenized_test ,root, maxRuleLHS[0], POS_levels   )  #<<<<<< Recursion
            
            if line==1:
                line1Prob = maxRuleLHS[1][1]
        else:
            opLine = ''    

        #print opLine
        #print score_dict
        #print backTrack_dict
        endTime = clock()
        result.append(opLine)
        timeTaken.append(endTime-startTime)
    
    print 'QUESTION 2 - Line 1 Parser Op: ',result[0]
    print 'QUESTION 2 - Line 1 Log Prob: ', line1Prob
    return result, inputStrLength, timeTaken

def plot(inputStrLength, timeTaken):
    
    import matplotlib.pyplot as plt
    import math
    
    fig= plt.figure()
    ax = plt.gca()
    
    inputStrLength = [math.log10(x) for x in inputStrLength]
    timeTaken = [math.log10(x) for x in timeTaken]
    
    y_power3=[]
    y_power2=[]
    for i in range(len(inputStrLength)):
        y_power3.append( pow(inputStrLength[i], 3) )
        y_power2.append( pow(inputStrLength[i], 2) )
        #print inputStrLength[i],',', timeTaken[i]
    
    y3_min = min(y_power3) 
    yt_min = min(timeTaken)
    y2_min = min(y_power2)
    #print yt_min-y3_min
    #print yt_min-y2_min
    
    for i in range(len(y_power3)):
        y_power3[i] = y_power3[i]+yt_min-y3_min#* yt_max
        y_power2[i] = y_power2[i]+yt_min-y2_min
        
    ax.scatter(inputStrLength, timeTaken, s=10, c='b', marker="s", label='result')
    ax.scatter(inputStrLength, y_power3, s=10, c='r', marker="o", label='power3')
    ax.scatter(inputStrLength, y_power2, s=10, c='g', marker="x", label='power2')
    
    plt.legend(loc='upper left');
       
    plt.xlabel('Length of strings(log scale)')
    plt.ylabel('Time to parse(log scale)')
    #ax.set_yscale('symlog')
    #ax.set_xscale('symlog')
    
    plt.show()
    
def saveToFile(fileName, opLines): 
    if opLines:
        with open(fileName,'wb') as f:
            for line in opLines:
                f.write(line+'\n')
    
    print 'Saved Program result as:',fileName            
                
###############################################################################################################################
###############################################################################################################################

if __name__ == '__main__':
    
    train_trees_pre_unk_file = sys.argv[1] #'train.trees.pre.unk'
    
    dev_strings_file = sys.argv[2]#'dev.strings'
    
    dev_train_postfile = sys.argv[3] #dev.parses
    
    rules_dict = q1_parse_input_trees(train_trees_pre_unk_file)
    
    opLines, inputStrLength, timeTaken = q2_parse_devtrain_file(rules_dict, dev_strings_file)
    
    plot(inputStrLength, timeTaken)
    
    saveToFile(dev_train_postfile,opLines)


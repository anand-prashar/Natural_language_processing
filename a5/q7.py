'''
Created on Oct 21, 2017

@author: anand
'''
import distsim

def readFile(reasoningFile):
    
    reasoningData = {}
    with open(reasoningFile) as f:
        key = None
        for line in f:
            if len(line)==0 or line[:2] == '//': continue
            if line[0] == ':': 
                key = line[2:].strip() 
                reasoningData.setdefault(key,[])
                continue
            if key == None:
                print 'Invalid file format'; exit
            
            reasoningData[key].append( [word.strip() for word in line.split(' ') if word!=''] )
    
    return reasoningData        

def q7_answer(reasoningData):
    
    def _get_n_best_count(analogy_returnedVectors, n_best):
        #count of words in n_best range - if they also hold right value
        count=0
        for correct_retVec_tpl in analogy_returnedVectors:
            if n_best > len(correct_retVec_tpl[1]): 
                if correct_retVec_tpl[0] in correct_retVec_tpl[1][:len(correct_retVec_tpl[1]) ]: count+=1
            elif   correct_retVec_tpl[0] in correct_retVec_tpl[1][:n_best ]:                     count+=1
                
        return float(count)
    
    word_to_vec_dict = distsim.load_word2vec("nyt_word2vec.4k")
    
    relation_group = {}
    result_comp = {}
    col_len= max([len(x) for x in reasoningData])

    print '\n1 NEGATIVE EXAMPLE FROM EACH GROUP( Element3: Incorrect Prediction / Correct Value):\n'    
    for groupName, list_of_analogies in reasoningData.iteritems():
        relation_group[groupName] = []
        result_comp.setdefault(groupName, {'matched':0, 'unmatched':0})
        incorrect_pred_example_shown = False
    
        
        for analogy in list_of_analogies:
            
            returned_vectors =  distsim.show_nearest(word_to_vec_dict,
                            word_to_vec_dict[analogy[0]]- word_to_vec_dict[analogy[1]]+word_to_vec_dict[ analogy[3]],# <-THE CORE OF RESASONING
                                                   set([analogy[0], analogy[1], analogy[3]]),
                                                   distsim.cossim_dense)
            returned_vectors = [ x[0] for x in returned_vectors]
            relation_group[groupName].append( (analogy[2], returned_vectors) )   
                
            if analogy[2] == returned_vectors[0]:
                result_comp[groupName]['matched']+=1
            else:
                result_comp[groupName]['unmatched']+=1
                if not incorrect_pred_example_shown:
                    print groupName.ljust(col_len), ' Predicted / Actual : ',\
                        analogy[0]+" : "+ analogy[1]+ " :: "+ returned_vectors[0]+'/'+analogy[2]+' : '+ analogy[3]
                incorrect_pred_example_shown = True   
    
    del word_to_vec_dict
    ########################### Print analysis
    
    relation_kind_accuracy = []            
    for groupName, match_unmatch_dict in result_comp.iteritems():   
        relation_kind_accuracy.append( [groupName, round(float(match_unmatch_dict['matched'])/
                                                           (match_unmatch_dict['matched']+match_unmatch_dict['unmatched']),3) ] )     
    
    relation_kind_accuracy = sorted(relation_kind_accuracy, key = lambda x: x[1], reverse = True)
    print '\nGROUPS SORTED BY REASONING ACCURACY:'
    for groupName,accuracy in relation_kind_accuracy:
        print groupName.ljust(col_len), ' Accuracy:',  accuracy
    print '\n'
        
    #result_table = []
    print ''.ljust(col_len),'TOP_1','\t','TOP_5','\t','TOP_10'
    for groupName, analogy_returnedVectors in relation_group.iteritems():
        result_row = [groupName]
        
        
        for n_best in [1,5,10]:
            
            top_n = _get_n_best_count(analogy_returnedVectors, n_best)
            result_row.append( round(top_n/ len(analogy_returnedVectors), 3) )
        
        #result_table.append(result_row)
        print result_row[0].ljust(col_len),result_row[1],'\t',result_row[2],'\t',result_row[3]
    print '\n'    
############################################################################################
############################################################################################

from time import time

t1= time()
reasoningData = readFile('word-test.v3.txt')
q7_answer(reasoningData)

print 'Time Taken: ',round(time()-t1,2),' seconds'
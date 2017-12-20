import numpy as np

def run_viterbi(emission_scores, trans_scores, start_scores, end_scores):
    """Run the Viterbi algorithm.

    N - number of tokens (length of sentence)
    L - number of labels

    As an input, you are given:
    - Emission scores, as an NxL array
    - Transition scores (Yp -> Yc), as an LxL array
    - Start transition scores (S -> Y), as an Lx1 array
    - End transition scores (Y -> E), as an Lx1 array

    You have to return a tuple (s,y), where:
    - s is the score of the best sequence
    - y is a size N array of integers representing the best sequence.
    """
    
    L = start_scores.shape[0]
    N = emission_scores.shape[0]
    assert end_scores.shape[0] == L; assert trans_scores.shape[0] == L; assert trans_scores.shape[1] == L; assert emission_scores.shape[1] == L
    
    viterbi_table   = np.empty(shape=(L,N) ); viterbi_table[:] = np.NAN
    backTrack_table = np.empty(shape=(L,N) ); backTrack_table[:] = np.NAN
    
    
    viterbi_table[:,0] = start_scores + emission_scores[0,:] #Filling 1st Column = col 0

    for vit_col_id in range(1, N): # 2nd col onwards
        
        for vit_row_id in range(L):
            
            possible_sel_list = viterbi_table[:, vit_col_id-1] + trans_scores[:, vit_row_id] + emission_scores[vit_col_id, vit_row_id] 
            chosen_cell_rowid = np.argmax( possible_sel_list)
            
            viterbi_table[  vit_row_id, vit_col_id] = possible_sel_list[ chosen_cell_rowid]
            backTrack_table[vit_row_id, vit_col_id] = chosen_cell_rowid

            
    # last </s>
    possible_sel_list = end_scores + viterbi_table[:, N-1]

    y=[ np.argmax( possible_sel_list ) ]  # start tracing path now - reached end !
    s = possible_sel_list[y] # prob. of max sentence
    
    for col_index in range(N-1, 0, -1):  # start, stop at 1, go in reverse
        y.append( int(backTrack_table[ y[-1], col_index]) )
        
        
    return (s, list(reversed(y)) )

######################################### TEST ###########################################


#===============================================================================
# if __name__ == '__main__':
#     
#     # emission_scores, trans_scores, start_scores, end_scores
#     
#     start_scores    = np.array([.3, .1, .3, .2, .1 ])
#     end_scores      = np.array( [ .05, .05, 0, 0, .1 ])
#     
#     trans_scores    = np.array([[.2, .4, .01 ,3, .04],
#                                  [.3, .05, .3, .2, .1],
#                                  [.9, .01, .01, .01, .07],
#                                  [.4, .05, .4, .1, .05],
#                                  [.1, .5, .1, .1, .1]] )
#     
#     emission_scores  = np.array([[0, 0, .7, 0, 0],   #the 
#                                  [.4, .1, 0, 0, 0],  #doctor
#                                  [.1, .9, 0, 0, 0],  #is
#                                  [0, 0, 0, 1, .1]])  #in
#     
#     
#     print run_viterbi(emission_scores, trans_scores, start_scores, end_scores)
#===============================================================================
#!/usr/bin/env python
import distsim
word_to_vec_dict = distsim.load_word2vec("nyt_word2vec.4k")
#===============================================================================
# king = word_to_vec_dict['king']
# man = word_to_vec_dict['man']
# woman = word_to_vec_dict['woman']
# ret = distsim.show_nearest(word_to_vec_dict,
#                            king-man+woman,                      # <-------------------------------  THE CORE OF RESASONING
#                            set(['king','man','woman']),
#                            distsim.cossim_dense)
# print("king : man :: {} : woman".format(ret[0][0]))
#===============================================================================


king = word_to_vec_dict['great']
man = word_to_vec_dict['greatest']
woman = word_to_vec_dict['biggest']
ret = distsim.show_nearest(word_to_vec_dict,
                           king-man+woman,                      # <-------------------------------  THE CORE OF RESASONING
                           set(['great','greatest','biggest']),
                           distsim.cossim_dense)
print("king : man :: {} : woman".format(ret[0][0]))


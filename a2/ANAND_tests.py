'''
Created on Sep 14, 2017

@author: anand
'''

from french_count import french_count, prepare_input

f= french_count()
for user_input in range(1000):
    print user_input, '-->',
    print " ".join(f.transduce(prepare_input(user_input)))
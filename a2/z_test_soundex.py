'''
Created on Sep 5, 2017

@author: anandpc
'''

from fst import FST
import string, sys
from fsmutils import composechars, trace
from multiprocessing.connection import CHALLENGE

def letters_to_numbers():
    """
    Returns an FST that converts letters to numbers as specified by
    the soundex algorithm
    """

    # Let's define our first FST
    f1 = FST('soundex-generate')

    # Indicate that '1' is the initial state
    f1.add_state('start')
    f1.initial_state = 'start'
    f1.add_state('0')
    f1.set_final('0')
    for letter in string.ascii_letters:
        f1.add_arc('start', '0', (letter), (letter))   # for 1st letter in IP

    removal_letters_set = {'a','e','i','o','u','h','w','y'}
    for removeChar in list(removal_letters_set):
        f1.add_arc('0','0',(removeChar), () )
        
    soundex_letter_lkp = [ (['b','f','p','v'], '1' ),
                            (['c','g','j','k','q','s','x','z'], '2'),
                            (['d','t'], '3' ),
                            (['l'], '4'),
                            (['m','n'], '5'),
                            (['r'], '6')
                         ]
    soundex_chars_set=set()
    for charList, state in soundex_letter_lkp:
        soundex_chars_set=soundex_chars_set.union( set(charList))  
        f1.add_state(state)
        f1.set_final(state)
        
    #build automata
    for charList, state in soundex_letter_lkp:
        
        for char in charList:
            f1.add_arc('0',state, (char), (state)) #1st jump 
            f1.add_arc(state,state, (char), ())   # self loop
            
        for char in list(removal_letters_set):    # for vowelsset
            f1.add_arc(state, '0', (char), ())    
        
        for char in list( soundex_chars_set.difference(set(charList))):  # any other char from different group will cause return to 0 state, with OP
            for returnCharList, returnState in soundex_letter_lkp:
                if char in returnCharList:
                    f1.add_arc( state, returnState, (char), (returnState))   

    return f1

    # The stub code above converts all letters except the first into '0'.
    # How can you change it to do the right conversion?

def truncate_to_three_digits():
    """
    Create an FST that will truncate a soundex string to three digits
    """

    # Ok so now let's do the second FST, the one that will truncate
    # the number of digits to 3
    f2 = FST('soundex-truncate')

    # Indicate initial and final states
    f2.add_state('1')
    f2.initial_state = '1'
    f2.set_final('1')
    
    f2.add_state('2')
    f2.set_final('2')
    
    f2.add_state('3')
    f2.set_final('3')
    
    f2.add_state('4')
    f2.set_final('4')
    
    f2.add_state('5')
    f2.set_final('5')


    # Add the arcs
    possible_chars = string.digits+ string.letters
    for letter in possible_chars:
        f2.add_arc('1', '2', (letter), (letter))
        f2.add_arc('2', '3', (letter), (letter))
        f2.add_arc('3', '4', (letter), (letter))
        f2.add_arc('4', '5', (letter), (letter))
        f2.add_arc('5', '5', (letter), ())

    return f2

    # The above stub code doesn't do any truncating at all -- it passes letter and number input through
    # what changes would make it truncate digits to 3?

def add_zero_padding():
    #===========================================================================
    # #Now, the third fst - the zero-padding fst
    # f3 = FST('soundex-padzero')
    #  
    # # Indicate initial and final states
    # f3.add_state('1')
    # f3.initial_state = '1'
    #  
    # f3.add_state('2')
    # f3.add_state('3')
    # f3.add_state('4')
    # f3.add_state('5')
    #  
    # #f3.set_final('2')
    # #f3.set_final('3')
    # #f3.set_final('4')
    # f3.set_final('5')
    #  
    # # Add the arcs
    # possible_chars = string.digits+ string.letters
    # for letter in possible_chars:
    #     f3.add_arc('1', '2', (letter), (letter))
    #      
    #     f3.add_arc('2', '3', (letter), (letter))
    #      
    #      
    #     f3.add_arc('3', '4', (letter), (letter))
    #      
    #      
    #     f3.add_arc('4', '5', (letter), (letter))
    #      
    #      
    #     f3.add_arc('5', '5', (letter), (letter))
    #      
    # #===========================================================================
    # #f3.add_arc('1', '2', (), ('0'))
    # f3.add_arc('2', '3', (), ('0'))
    # f3.add_arc('3', '4', (), ('0'))
    # f3.add_arc('4', '5', (), ('0'))
    # #===========================================================================
    # return f3
    #===========================================================================
    
    f3 = FST('soundex-padzero')
    f3.add_state('1')
    f3.add_state('1a')
    f3.add_state('1b')
    f3.add_state('2')
      
    f3.initial_state = '1'
    f3.set_final('2')
  
    for letter in string.letters:
        f3.add_arc('1', '1', (letter), (letter))
    for number in xrange(10):
        f3.add_arc('1', '1', (str(number)), (str(number)))
      
    f3.add_arc('1', '1a', (), ('0'))
    f3.add_arc('1a', '1b', (), ('0'))
    f3.add_arc('1b', '2', (), ('0'))
    return f3
        
    

    # The above code adds zeroes but doesn't have any padding logic. Add some!


    
if __name__ == '__main__':
    user_input =  'Euler'.strip() #raw_input().strip()
    f1 = letters_to_numbers()
    f2 = truncate_to_three_digits()
    f3 = add_zero_padding()

    #if user_input:
    #print("%s -> %s" % (user_input, composechars(tuple(user_input), f1,f2,f3)))
    
    print str(f1)
    #print f1.transduce(list('Peterson'))

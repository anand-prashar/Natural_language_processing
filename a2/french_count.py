import sys
from fst import FST
from fsmutils import composewords, trace

kFRENCH_TRANS = {0: "zero", 1: "un", 2: "deux", 3: "trois", 4:
                 "quatre", 5: "cinq", 6: "six", 7: "sept", 8: "huit",
                 9: "neuf", 10: "dix", 11: "onze", 12: "douze", 13:
                 "treize", 14: "quatorze", 15: "quinze", 16: "seize",
                 20: "vingt", 30: "trente", 40: "quarante", 50:
                 "cinquante", 60: "soixante", 100: "cent"}

kFRENCH_AND = 'et'

def prepare_input(integer):
    assert isinstance(integer, int) and integer < 1000 and integer >= 0, \
      "Integer out of bounds"
    return list("%03i" % integer)


def french_count():
    f = FST('french')

    f.add_state('start')
    f.initial_state = 'start'
    
    for index in range(10):
        f.add_state('H'+str(index))
        f.add_state('T'+str(index))
        f.add_state('U'+str(index))
        f.add_state('U1'+str(index))
        f.set_final('U'+str(index))
        f.set_final('U1'+str(index))
        
    f.add_state('H:(T0-T9)_COMMON')
    f.add_state('T:(U2-U9)_COMMON')
    f.add_state('T:(U11-U19)_COMMON')
    
    
    # Prepare 100s
    for i in range(10):
        if i==0: opList= []
        elif i ==1: opList = [ kFRENCH_TRANS[100] ]
        else: opList = [ kFRENCH_TRANS[i] + ' '+kFRENCH_TRANS[100] ]
        f.add_arc('start','H'+str(i), [str(i)], opList )    
        if i !=0: f.add_arc('H'+str(i), 'H:(T0-T9)_COMMON', [], [])   # 0 has special case, connections made in line 58
    #- special case 0 
    f.add_state('0_case')
    f.add_arc('H0','0_case',['0'],[])
    f.add_arc('0_case', 'U0',['0'],[kFRENCH_TRANS[0]])
    f.add_arc('0_case', 'U0',['1'],[kFRENCH_TRANS[1]])
    f.add_arc('0_case', 'T:(U2-U9)_COMMON',[],[])
        
    # Prepare 10s - arcs to reach state
    for i in range(10):
        if i==0 or i==1: opList = []
        elif i<=6: opList = [ kFRENCH_TRANS[i*10] ]
        elif i==7: opList = [ kFRENCH_TRANS[60] ]
        else:      opList = [ kFRENCH_TRANS[4]+' '+kFRENCH_TRANS[20] ]
        f.add_arc('H:(T0-T9)_COMMON','T'+str(i), [str(i)], opList ) 
        if i !=0: f.add_arc('H0', 'T'+str(i), [str(i)], opList ) 
        
    # Prepare 10s - arcs to exit to 1s                                         - Major Mapping BEGIN
    f.add_arc('T0', 'U0', ['0'], [])
    f.add_arc('T0', 'U1', ['1'], [kFRENCH_TRANS[1]])
    f.add_arc('T0', 'T:(U2-U9)_COMMON', [], [])
    
    f.add_arc('T1', 'T:(U11-U19)_COMMON', [], [])
    f.add_arc('T1', 'U10', ['0'], [kFRENCH_TRANS[10]])
    
    f.add_arc('T2', 'U0', ['0'], [])
    f.add_arc('T2', 'U1', ['1'], [kFRENCH_AND+' '+kFRENCH_TRANS[1]])
    f.add_arc('T2', 'T:(U2-U9)_COMMON', [], [])
    
    f.add_arc('T3', 'U0', ['0'], [])
    f.add_arc('T3', 'U1', ['1'], [kFRENCH_AND+' '+kFRENCH_TRANS[1]])
    f.add_arc('T3', 'T:(U2-U9)_COMMON', [], [])
    
    f.add_arc('T4', 'U0', ['0'], [])
    f.add_arc('T4', 'U1', ['1'], [kFRENCH_AND+' '+kFRENCH_TRANS[1]])
    f.add_arc('T4', 'T:(U2-U9)_COMMON', [], [])
    
    f.add_arc('T5', 'U0', ['0'], [])
    f.add_arc('T5', 'U1', ['1'], [kFRENCH_AND+' '+kFRENCH_TRANS[1]])
    f.add_arc('T5', 'T:(U2-U9)_COMMON', [], [])
    
    f.add_arc('T6', 'U0', ['0'], [])
    f.add_arc('T6', 'U1', ['1'], [kFRENCH_AND+' '+kFRENCH_TRANS[1]])
    f.add_arc('T6', 'T:(U2-U9)_COMMON', [], [])
    
    for i in range(10):
        if i == 1: opList = [ kFRENCH_AND + ' '+kFRENCH_TRANS[i+10] ]
        elif i in [7,8,9]: opList = [ kFRENCH_TRANS[10]+' '+kFRENCH_TRANS[i] ]
        else:      opList = [ kFRENCH_TRANS[i+10] ]
        f.add_arc('T7', 'U'+str(10+i), [str(i)], opList )
    #=========================================================================== weird behavior on epsilon, backup above
    # f.add_arc('T7', 'U10', ['0'], [kFRENCH_TRANS[10]])
    # f.add_arc('T7', 'U11', ['1'], [kFRENCH_AND+' '+kFRENCH_TRANS[11]])
    # f.add_arc('T7', 'T:(U11-U19)_COMMON', [], [])
    #===========================================================================

    f.add_arc('T8', 'U0', ['0'], [])
    f.add_arc('T8', 'U1', ['1'], [kFRENCH_TRANS[1]])
    f.add_arc('T8', 'T:(U2-U9)_COMMON', [], [])
    
    f.add_arc('T9', 'U10', ['0'], [kFRENCH_TRANS[10]])
    f.add_arc('T9', 'T:(U11-U19)_COMMON', [], [])
    # Prepare 10s - arcs to exit to 1s                                         - Major Mapping END      
        
        
    # prepare Common: 1s
    for i in range(1,10):
        if i!=1: f.add_arc('T:(U2-U9)_COMMON', 'U'+str(i), [str(i)], [ kFRENCH_TRANS[i]])
        if i+10 not in [17,18,19]: f.add_arc('T:(U11-U19)_COMMON', 'U'+str(10+i), [str(i)], [ kFRENCH_TRANS[i+10]])
        else:                      f.add_arc('T:(U11-U19)_COMMON', 'U'+str(10+i), [str(i)],  [ kFRENCH_TRANS[10]+' '+kFRENCH_TRANS[i]])

    return f

if __name__ == '__main__':
    string_input = raw_input()
    user_input = int(string_input)
    f = french_count()
    if string_input:
        print user_input, '-->',
        print " ".join(f.transduce(prepare_input(user_input)))

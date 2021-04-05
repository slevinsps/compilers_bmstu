from lab2 import elimination_of_recursion_indirect, remove_unattainable_symbols, elimination_of_recursion_immediate_1

def compare_grammatics(grammatic1, grammatic2):
    res = set(grammatic1['nonterminal']) != set(grammatic2['nonterminal']) or \
           set(grammatic1['terminal']) != set(grammatic2['terminal']) or \
           grammatic1['startsymbol'] != grammatic2['startsymbol'] or \
           grammatic1['rules'] != grammatic2['rules']

    return res
        

def test_remove_immediate_recursion():
    test_arr = [
        # 2.27
        {
            'grammatic':{ 
                            'nonterminal': ['E', 'T', 'F'], 
                            'terminal': ['+', '*', '(', ')', 'a'], 
                            'startsymbol': 'E', 
                            'rules': {
                                    'E': [['E', '+', 'T'], ['T']], 
                                    'T': [['T', '*', 'F'], ['F']], 
                                    'F': [['(', 'E', ')'], ['a']]}
                        },
            'expected': { 
                            'nonterminal': ['E', 'T', 'F', 'E1', 'T1'], 
                            'terminal': ['+', '*', '(', ')', 'a'], 
                            'startsymbol': 'E', 
                            'rules': {
                                    'E': [['T'], ['T', 'E1']],
                                    'E1': [['+', 'T'], ['+', 'T', 'E1']],
                                    'T': [['F'], ['F', 'T1']],
                                    'T1': [['*', 'F'], ['*', 'F', 'T1']], 
                                    'F': [['(', 'E', ')'], ['a']]}
                        }
        },       

    ]

    for test in test_arr:
        failed_flag = False
        grammatic = test['grammatic']
        expected_grammatic = test['expected']
        elimination_of_recursion_grammatic = elimination_of_recursion_immediate_1(grammatic)
        
        if compare_grammatics(expected_grammatic, elimination_of_recursion_grammatic):
           print('Failed in test_remove_immediate_recursion \nexpected:', expected_grammatic, '\nget:', elimination_of_recursion_grammatic)
           failed_flag = True
           break

    if not failed_flag:
        print('All passed in test_remove_immediate_recursion')



def test_remove_indirect_recursion():
    test_arr = [
        # https://neerc.ifmo.ru/wiki/index.php?title=Устранение_левой_рекурсии
        {
            'grammatic':{ 
                            'nonterminal': ['A', 'S'], 
                            'terminal': ['a', 'b'], 
                            'startsymbol': 'A', 
                            'rules': {
                                    'A': [['S', 'a'], ['A', 'a']], 
                                    'S': [['A', 'b']]}
                        },
            'expected': { 
                            'nonterminal': ['A', 'S', 'A1', 'S1'], 
                            'terminal': ['a', 'b'], 
                            'startsymbol': 'A', 
                            'rules': {
                                    'A': [['S', 'a', 'A1']], 
                                    'A1': [['a', 'A1'], ['eps']], 
                                    'S': [['S1']], 
                                    'S1': [['a', 'A1', 'b', 'S1'], ['eps']]}
                        }
        },
        # https://neerc.ifmo.ru/wiki/index.php?title=Устранение_левой_рекурсии
        {
            'grammatic':{
                            'nonterminal': ['A', 'S'], 
                            'terminal': ['a', 'b', 'y'], 
                            'startsymbol': 'A', 
                            'rules': {
                                    'A': [['S', 'a']], 
                                    'S': [['S', 'b'], ['S', 'a', 'y'], ['b']]}
                        },
            'expected': { 
                            'nonterminal': ['A', 'S', 'S1'], 
                            'terminal': ['a', 'b', 'y'], 
                            'startsymbol': 'A', 
                            'rules': {
                                    'A': [['S', 'a']], 
                                    'S': [['b', 'S1']],
                                    'S1': [['b', 'S1'], ['a', 'y', 'S1'], ['eps']]}
                        }
        },
        # 4.7
        {
            'grammatic':{ 
                            'nonterminal': ['E', 'T', 'F'], 
                            'terminal': ['+', '*', '(', ')', 'a'], 
                            'startsymbol': 'E', 
                            'rules': {
                                    'E': [['E', '+', 'T'], ['T']], 
                                    'T': [['T', '*', 'F'], ['F']], 
                                    'F': [['a'], ['(', 'E', ')']]}
                        },
            'expected': { 
                            'nonterminal': ['E', 'T', 'F', 'E1', 'T1'], 
                            'terminal': ['+', '*', '(', ')', 'a'], 
                            'startsymbol': 'E', 
                            'rules': {
                                    'E': [['T', 'E1']],
                                    'E1': [['+', 'T', 'E1'], ['eps']],
                                    'T': [['F', 'T1']],
                                    'T1': [['*', 'F', 'T1'], ['eps']], 
                                    'F': [['a'], ['(', 'F', 'T1', 'E1', ')']]}
                        }
        },
        # 4.9
        {
            'grammatic':{
                            'nonterminal': ['S', 'A'], 
                            'terminal': ['a', 'b', 'c', 'd'], 
                            'startsymbol': 'S', 
                            'rules': {
                                    'S': [['A', 'a'], ['b']], 
                                    'A': [['A', 'c'], ['S', 'd'], ['eps']]}
                        },
            'expected': {
                            'nonterminal': ['S', 'A', 'A1'], 
                            'terminal': ['a', 'b', 'c', 'd'], 
                            'startsymbol': 'S', 
                            'rules': {
                                    'S': [['A', 'a'], ['b']], 
                                    'A': [['b', 'd', 'A1'], ['A1']],
                                    'A1': [['c', 'A1'], ['a', 'd', 'A1'], ['eps']]}
                        }
        },
        

    ]

    for test in test_arr:
        failed_flag = False
        grammatic = test['grammatic']
        expected_grammatic = test['expected']
        elimination_of_recursion_grammatic = elimination_of_recursion_indirect(grammatic)
        # elimination_of_recursion_grammatic = remove_unattainable_symbols(elimination_of_recursion_grammatic)    
        if compare_grammatics(expected_grammatic, elimination_of_recursion_grammatic):
           print('Failed in test_remove_indirect_recursion \nexpected:', expected_grammatic, '\nget:', elimination_of_recursion_grammatic)
           failed_flag = True
           break

    if not failed_flag:
        print('All passed in test_remove_indirect_recursion')


def test_remove_unattainable_symbols():
    test_arr = [
        {
            'grammatic':{ 
                            'nonterminal': ['A', 'S', 'F'], 
                            'terminal': ['a', 'b'], 
                            'startsymbol': 'A', 
                            'rules': {
                                    'A': [['S', 'a'], ['A', 'a']], 
                                    'S': [['A', 'b']], 
                                    'F': [['A', 'a'], ['S', 'b']]}
                        },
            'expected': { 
                            'nonterminal': ['A', 'S'], 
                            'terminal': ['a', 'b'], 
                            'startsymbol': 'A', 
                            'rules': {
                                    'A': [['S', 'a'], ['A', 'a']], 
                                    'S': [['A', 'b']]}
                        }
        },
        {
            'grammatic':{ 
                            'nonterminal': ['A', 'S', 'F'], 
                            'terminal': ['a', 'b', 'n', 't'], 
                            'startsymbol': 'A', 
                            'rules': {
                                    'A': [['S', 'a'], ['A', 'a']], 
                                    'S': [['A', 'b']], 
                                    'F': [['A', 'n'], ['S', 't']]}
                        },
            'expected': { 
                            'nonterminal': ['A', 'S'], 
                            'terminal': ['a', 'b'], 
                            'startsymbol': 'A', 
                            'rules': {
                                    'A': [['S', 'a'], ['A', 'a']], 
                                    'S': [['A', 'b']]}
                        }
        },
        {
            'grammatic':{ 
                            'nonterminal': ['A', 'S', 'F', 'F2', 'F3'], 
                            'terminal': ['a', 'b', 'n', 't'], 
                            'startsymbol': 'A', 
                            'rules': {
                                    'A': [['S', 'a']], 
                                    'S': [['eps']],
                                    'F': [['A', 'b']], 
                                    'F2': [['A', 'n'], ['S', 't']],
                                    'F3': [['eps']]}
                        },
            'expected': { 
                            'nonterminal': ['A', 'S'], 
                            'terminal': ['a'], 
                            'startsymbol': 'A', 
                            'rules': {
                                    'A': [['S', 'a']], 
                                    'S': [['eps']]}
                        }
        },
    ]

    for test in test_arr:
        failed_flag = False
        grammatic = test['grammatic']
        expected_grammatic = test['expected']
        remove_unattainable_grammatic = remove_unattainable_symbols(grammatic)
        
        if compare_grammatics(expected_grammatic, remove_unattainable_grammatic):
           print('Failed in test_remove_unattainable_symbols \nexpected:', expected_grammatic, '\nget:', remove_unattainable_grammatic)
           failed_flag = True
           break

    if not failed_flag:
        print('All passed in test_remove_unattainable_symbols')

def test():
    test_remove_indirect_recursion()
    test_remove_unattainable_symbols()
    test_remove_immediate_recursion()

if __name__ == '__main__':
    test()

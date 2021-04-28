from lab2 import elimination_of_recursion_indirect, \
                 elimination_of_recursion_immediate_1, \
                 remove_unattainable_symbols, \
                 left_factorization

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
        {
            'grammatic':{ 
                            'nonterminal': ['S', 'T'], 
                            'terminal': ['a'], 
                            'startsymbol': 'S', 
                            'rules': {
                                    'S': [['T', 'a']]
                            }
                        },
            'expected': { 
                            'nonterminal': ['S', 'T'], 
                            'terminal': ['a'], 
                            'startsymbol': 'S', 
                            'rules': {
                                    'S': [['T', 'a']]
                            }
                        }
        },    
        {
            'grammatic':{ 
                            'nonterminal': ['S'], 
                            'terminal': ['a'], 
                            'startsymbol': 'S', 
                            'rules': {
                                    'S': [['S', 'a']]
                            }
                        },
            'expected': { 
                            'nonterminal': ['S', 'S1'], 
                            'terminal': ['a'], 
                            'startsymbol': 'S', 
                            'rules': {
                                    'S': [['S1']],
                                    'S1': [['a'], ['a', 'S1']]
                            }
                        },
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
                                    'F': [['a'], ['(', 'E', ')']]}
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
        {
            'grammatic':{ 
                            'nonterminal': ['S', 'T'], 
                            'terminal': ['a'], 
                            'startsymbol': 'S', 
                            'rules': {
                                    'S': [['T', 'a']]
                            }
                        },
            'expected': { 
                            'nonterminal': ['S', 'T'], 
                            'terminal': ['a'], 
                            'startsymbol': 'S', 
                            'rules': {
                                    'S': [['T', 'a']]
                            }
                        }
        },    
        {
            'grammatic':{ 
                            'nonterminal': ['S'], 
                            'terminal': ['a'], 
                            'startsymbol': 'S', 
                            'rules': {
                                    'S': [['S', 'a']]
                            }
                        },
            'expected': { 
                            'nonterminal': ['S', 'S1'], 
                            'terminal': ['a'], 
                            'startsymbol': 'S', 
                            'rules': {
                                    'S': [['S1']],
                                    'S1': [['a', 'S1'], ['eps']]
                            }
                        },
        },    
        {
            'grammatic':{ 
                            'nonterminal': ['A, B, C, D'], 
                            'terminal': ['a, b'], 
                            'startsymbol': 'A', 
                            'rules': {
                                    'A': [['B', 'A']],
                                    'B': [['C', 'b', 'A'], ['B', 'a', 'B'], ['eps']],
                                    'C': [['A', 'A'], ['B', 'C'], ['a', 'C']]
                            }
                        },
            'expected': { 
                            'nonterminal': ['A, B, C, D', 'B1', 'C1'], 
                            'terminal': ['a, b'], 
                            'startsymbol': 'A', 
                            'rules': {
                                    'A': [['B', 'A']],
                                    'B': [['C', 'b', 'A', 'B1'], ['B1']],
                                    'C': [['B1', 'A', 'A', 'C1'], ['B1', 'C', 'C1'], ['a', 'C', 'C1']],
                                    'B1': [['a', 'B', 'B1'], ['eps']],
                                    'C1': [['b', 'A', 'B1', 'A', 'A', 'C1'], ['b', 'A', 'B1', 'C', 'C1'], ['eps']]
                            }
                        },
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
        {
            'grammatic':{ 
                            'nonterminal': ['S', 'T'], 
                            'terminal': ['a'], 
                            'startsymbol': 'S', 
                            'rules': {
                                    'S': [['T', 'a']]
                            }
                        },
            'expected': { 
                            'nonterminal': ['S', 'T'], 
                            'terminal': ['a'], 
                            'startsymbol': 'S', 
                            'rules': {
                                    'S': [['T', 'a']]
                            }
                        }
        },    
        {
            'grammatic':{ 
                            'nonterminal': ['S'], 
                            'terminal': ['a'], 
                            'startsymbol': 'S', 
                            'rules': {
                                    'S': [['S', 'a']]
                            }
                        },
            'expected': { 
                            'nonterminal': ['S'], 
                            'terminal': ['a'], 
                            'startsymbol': 'S', 
                            'rules': {
                                    'S': [['S', 'a']]
                            }
                        },
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



def test_left_factorization():
    test_arr = [
        {
            'grammatic':{ 
                            'nonterminal': ['S', 'E'], 
                            'terminal': ['i', 't', 'e', 'a'], 
                            'startsymbol': 'S', 
                            'rules': {
                                    'S': [['i', 'E', 't', 'S'], ['i', 'E', 't', 'S', 'e', 'S'], ['a']], 
                                    'E': [['b']]}
                        },
            'expected': { 
                            'nonterminal': ['S', 'E', 'S1'], 
                            'terminal': ['i', 't', 'e', 'a'], 
                            'startsymbol': 'S', 
                            'rules': {
                                    'S': [['i', 'E', 't', 'S', 'S1'], ['a']], 
                                    'S1': [['e', 'S'], ['eps']],
                                    'E': [['b']]}
                        }
        },
        {
            'grammatic':{ 
                            'nonterminal': ['stmt', 'expr'], 
                            'terminal': ['if', 'then', 'else'], 
                            'startsymbol': 'stmt', 
                            'rules': {
                                    'stmt': [['if', 'expr', 'then', 'stmt', 'else', 'stmt'], ['if', 'expr', 'then', 'stmt']]
                            }
                        },
            'expected': { 
                            'nonterminal': ['stmt', 'stmt1', 'expr'], 
                            'terminal': ['if', 'then', 'else'],
                            'startsymbol': 'stmt', 
                            'rules': {
                                    'stmt': [['if', 'expr', 'then', 'stmt', 'stmt1']], 
                                    'stmt1': [['else', 'stmt'], ['eps']],
                            }
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
                            'nonterminal': ['A', 'S', 'F'], 
                            'terminal': ['a', 'b', 'n', 't'], 
                            'startsymbol': 'A', 
                            'rules': {
                                    'A': [['S', 'a'], ['A', 'a']], 
                                    'S': [['A', 'b']], 
                                    'F': [['A', 'n'], ['S', 't']]}
                        }
        },
        {
            'grammatic':{ 
                            'nonterminal': ['S', 'T'], 
                            'terminal': ['a'], 
                            'startsymbol': 'S', 
                            'rules': {
                                    'S': [['T', 'a']]
                            }
                        },
            'expected': { 
                            'nonterminal': ['S', 'T'], 
                            'terminal': ['a'], 
                            'startsymbol': 'S', 
                            'rules': {
                                    'S': [['T', 'a']]
                            }
                        }
        },    
        {
            'grammatic':{ 
                            'nonterminal': ['S'], 
                            'terminal': ['a'], 
                            'startsymbol': 'S', 
                            'rules': {
                                    'S': [['S', 'a']]
                            }
                        },
            'expected': { 
                            'nonterminal': ['S'], 
                            'terminal': ['a'], 
                            'startsymbol': 'S', 
                            'rules': {
                                    'S': [['S', 'a']]
                            }
                        },
        },   
        {
            'grammatic':{ 
                            'nonterminal': ['S'], 
                            'terminal': ['a', 'b', 'c'], 
                            'startsymbol': 'S', 
                            'rules': {
                                    'S': [['S', 'a'], ['S', 'b'], ['S', 'c']]
                            }
                        },
            'expected': { 
                            'nonterminal': ['S', 'S1'], 
                            'terminal': ['a', 'b', 'c'], 
                            'startsymbol': 'S', 
                            'rules': {
                                    'S': [['S', 'S1']],
                                    'S1': [['a'], ['b'], ['c']]
                            }
                        },
        },   

    ]

    for test in test_arr:
        failed_flag = False
        grammatic = test['grammatic']
        expected_grammatic = test['expected']
        left_factorization_grammatic = left_factorization(grammatic)
        
        if compare_grammatics(expected_grammatic, left_factorization_grammatic):
           print('Failed in test_left_factorization \nexpected:', expected_grammatic, '\nget:', left_factorization_grammatic)
           failed_flag = True
           break

    if not failed_flag:
        print('All passed in test_left_factorization')


def test():
    test_remove_indirect_recursion()
    test_remove_unattainable_symbols()
    test_remove_immediate_recursion()
    test_left_factorization()

if __name__ == '__main__':
    test()





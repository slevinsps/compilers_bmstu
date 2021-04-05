from lab2 import elimination_of_recursion_indirect


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

    ]

    for test in test_arr:
        failed_flag = False
        grammatic = test['grammatic']
        expected_grammatic = test['expected']
        new_grammatic = elimination_of_recursion_indirect(grammatic)
        if set(expected_grammatic['nonterminal']) != set(new_grammatic['nonterminal']) or \
           set(expected_grammatic['terminal']) != set(new_grammatic['terminal']) or \
           expected_grammatic['startsymbol'] != new_grammatic['startsymbol'] or \
           expected_grammatic['rules'] != new_grammatic['rules']:

           print('Failed in test_remove_indirect_recursion \nexpected:', expected_grammatic, '\nget:', new_grammatic)
           failed_flag = True
           break

    if not failed_flag:
        print('All passed in test_remove_indirect_recursion')

def test():
    test_remove_indirect_recursion()

if __name__ == '__main__':
    test()

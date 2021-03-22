from parse import Lexer, Parser, Token, State, NFA, DFA



def compile(p, debug = False):
    
    def print_tokens(tokens):
        for t in tokens:
            print(t)

    lexer = Lexer(p)
    parser = Parser(lexer)
    
    tokens = parser.parse()
    if debug:
        print_tokens(tokens) 

    # for i in range(len(tokens)):
    #     print(tokens[i])

    nfa = NFA()
    nfa.build(tokens)

    dfa = DFA()
    dfa.convert_nfa_to_dfa(nfa)
    
    return nfa, dfa

def test():
    test_array = [
        {'pattern': '(0|(1(01*(00)*0)*1)*)*',
         'string_array': [(['0', '00', '11', '000', '011', '110', '0000', '0011', '0110', '1001', '1100', '1111', '00000'], True),
                          (['01', '01010', '0111100111', '100', 'abas'], False)]
        },
        {'pattern': '(a(b|c))*c',
         'string_array': [(['abc', 'abababababc', 'acc', 'c'], True),
                          (['aaaa', 'baba', 'abb', 'ababababa', 'bbbbb'], False)]
        }
    ]
    
    error = False
    for test in test_array:
        nfa, dfa = compile(test['pattern'])
        for pattern_test_array in test['string_array']:
            string_array = pattern_test_array[0]
            expected = pattern_test_array[1]
            for string in string_array:
                res = dfa.match(string)
                if res != expected:
                    error = True
                    print('[Error dfa]', 'pattern = ', test['pattern'], '; string = ', string, '; res = ', res, '; expected = ', expected)
                res = nfa.match(string)
                if res != expected:
                    error = True
                    print('[Error nfa]', 'pattern = ', test['pattern'], '; string = ', string, '; res = ', res, '; expected = ', expected)
    
    if not error:
        print('All tests passed')

def main():
    test()
    # p = '(0|(1(01*(00)*0)*1)*)*'
    p = '(a(b|c))*c'
    nfa, dfa = compile(p)
    s = 'abc'
    res_nfa = nfa.match(s)
    res_dfa = dfa.match(s)
    print('pattern = ', p, '; string = ', s, '; res_nfa = ', res_nfa, '; res_dfa = ', res_dfa)

main()


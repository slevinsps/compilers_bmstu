from precedence import Precedence
from exception import CompileError
from parser import GrammaticParser
from lexer import Lexer


def test():
    tests = [
        {
            'code': '''{
                            a = 5 * 5 <= 6 - (((10)));
                            b = 6 + 6;
                            c = a * b
                        }
                    ''',
            'res': True
        },
        {
            'code': '''{
                            a = 8 / 2 + 5 - 6
                        }
                    ''',
            'res': True
        },
        {
            'code': '''{
                            a = (8 / 2 + ((5))) * (6 - 3)
                        }
                    ''',
            'res': True
        },
        {
            'code': '''{
                            a = (8 / 2 + ((5))) * (6 - 3) <= 5 + 3 - 6
                        }
                    ''',
            'res': True
        },
        {
            'code': '''{
                            a = 5;
                            b = 6 - 6;
                            c = 7;
                            d = a + b - c;
                            e = (c * d) - (5 - 6)
                        }
                    ''',
            'res': True
        },
        {
            'code': '''{
                            a = 5 < 6 + 3;
                            b = 6 / 8 >= 8 * 3;
                            c = ((98)) * 2 <> 3 * 2 * (6 + 3) - 15 / (3 * 8)
                        }
                    ''',
            'res': True
        },
        {
            'code': '''{
                            a = 5 - ((5 + 2)
                        }
                    ''',
            'res': False
        },
        {
            'code': '''{
                            a = 5 - (5 + 2))
                        }
                    ''',
            'res': False
        },
        {
            'code': '''{
                            a = 
                        }
                    ''',
            'res': False
        },
        {
            'code': '''{
                            5 
                        }
                    ''',
            'res': False
        },
        {
            'code': '''{
                            5 <= -
                        }
                    ''',
            'res': False
        },
    ]

    grammaticParser = GrammaticParser()
    lexer = Lexer()
    grammar_path = './gr.txt'
    precedenceHandler = Precedence()
    grammatic = grammaticParser.parse(grammar_path)
    precedenceHandler.buildOperatorPrecedenceMatrix(grammatic)
    
    error_flag = False
    for test in tests:
        try:
            tokens = lexer.lex(test['code'])
            precedenceHandler.checkCode(grammatic, tokens)  
        except CompileError as err:
            if test['res']:
                print('Error in ', test['code'])
                print(err)
                error_flag = True
    if not error_flag:
        print('All tests pass')

def main():
    test()

main()
from compiler import Compiler 
from exception import CompileError

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
                            c = ((98)) * 2 == 3 * 2 * (6 + 3) - 15 / (3 * 8)
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

    compiler = Compiler()
    error_flag = False
    for test in tests:
        try:
            compiler.compile(test['code'])
        except CompileError:
            if test['res']:
                print('Error in ', test['code'])
                error_flag = True
    if not error_flag:
        print('All tests pass')

def main():
    test()

main()
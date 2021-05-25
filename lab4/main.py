from parser import GrammaticParser
from precedence import Precedence
from lexer import Lexer
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--grammar_path", help="path to grammatic file", required=True)
    parser.add_argument("-c", "--code_path", help="path to code file", required=True)
    args = parser.parse_args()
    grammar_path = args.grammar_path
    code_path = args.code_path

    grammaticParser = GrammaticParser()
    lexer = Lexer()

    precedenceHandler = Precedence()
    grammatic = grammaticParser.parse(grammar_path)
    precedenceHandler.buildOperatorPrecedenceMatrix(grammatic)
    print('Lt ', precedenceHandler.Lt)
    print('Rt ', precedenceHandler.Rt)
    precedenceHandler.printMatrix()

    with open(code_path, 'r') as f:
        source = f.read()

    tokens = lexer.lex(source)

    all_terminal_symbols, used_rules = precedenceHandler.checkCode(grammatic, tokens)  
    for i in range(len(used_rules)):
        print(used_rules[i][0],':', used_rules[i][1])
    print('Обратная польская запись:')
    print(all_terminal_symbols)


if __name__ == '__main__':
    main()
import argparse
from lexer import Lexer
from ast_builder import AstTreeBuilder

class Compiler():
    def __init__(self):
        self.lexer = Lexer()
        self.astTreeBuilder = AstTreeBuilder()
    
    def compile(self, source):
        self.lexer.lex(source)
        root = self.astTreeBuilder.build(self.lexer)
        
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", help="path to code sps file", required=True)
    args = parser.parse_args()
    path = args.path

    compiler = Compiler()

    with open(path, 'r') as f:
        source = f.read()
        compiler.compile(source)
        compiler.astTreeBuilder._draw_tree()

 

if __name__ == '__main__':
    main()
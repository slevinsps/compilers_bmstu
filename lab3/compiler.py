import argparse
from lexer import Lexer

class CompileError(Exception):
    def __init__(self, message="Compile error"):
        self.message = message
        super().__init__(self.message)
    def __str__(self):
        return self.message

class Node():
    def __init__(self, operations = None, nodes = None, is_leaf = False, node_name = 'NO_NAME'):
        self.operations = operations
        self.nodes = nodes
        self.is_leaf = is_leaf
        self.node_name = node_name
    
class AstTreeBuilder():
    def __init__(self):
        self.lexer = None
        self.root = Node()

    def _draw_tree(self):
        children = self.root.nodes
        print(self.root.node_name + ' -', end = ' ')
        print('op:', self.root.operations, end = ' ')
        print('nodes:', end = ' ')
        for n in self.root.nodes:
            if n is not None and not n.is_leaf:
                print(n.node_name, end = ' ')
        print()
        while len(children) > 0:
            new_children = []
            for i in range(len(children)):
                if children[i] is None:
                    continue

                print(children[i].node_name + ' -', end = ' ')
                print('op:', children[i].operations, end = ' ')
                print('nodes:', end = ' ')
                if children[i].is_leaf:
                    print(children[i].nodes[0], end = ' ')
                else:
                    for n in children[i].nodes:
                        if n is not None:
                            print(n.node_name, end = ' ')
                print()
                if children[i].nodes is not None and not children[i].is_leaf:
                    new_children += children[i].nodes
            children = new_children

    def factor(self):
        lex = self.lexer.next()
        if lex is not None and lex['type'] == 'OP_closebrackets':
            raise CompileError()
        item = lex
        is_leaf = True
        if lex is not None and lex['type'] == 'OP_openbrackets':
            is_leaf = False
            item = self.arithmetic_expression()
            lex = self.lexer.next()
            # print('s', self.lexer.num)
            if lex is None or lex['type'] != 'OP_closebrackets':
                raise CompileError()
        res = None
        if item is not None:
            res = Node(None, [item, None], is_leaf = is_leaf, node_name = 'factor')

        return res

    def term(self):
        item1 = self.factor()
        if item1 is None:
            raise CompileError()
        item2 = None
        op = None
        lex = self.lexer.next()
        if lex is not None:
            while lex is not None and lex['type'] == 'OP_mullike':
                if item2 is not None:
                    item1 = Node(op, [item1, item2], node_name = 'term')
                op = lex
                item2 = self.factor()
                if item2 is None:
                    raise CompileError()
                
                lex = self.lexer.next()
            else:
                self.lexer.prev()
 
        return Node(op, [item1, item2], node_name = 'term')

    def arithmetic_expression(self):
        item1 = self.term()
        if item1 is None:
            raise CompileError()
        item2 = None
        op = None
        lex = self.lexer.next()
        if lex is not None:
            while lex is not None and lex['type'] == 'OP_addlike':
                if item2 is not None:
                    item1 = Node(op, [item1, item2], node_name = 'arithmetic_expression')
                op = lex
                item2 = self.term()
                if item2 is None:
                    raise CompileError()
                
                lex = self.lexer.next()
            else:
                self.lexer.prev()
        return Node(op, [item1, item2], node_name = 'arithmetic_expression')
        
    def expression(self, ):
        item1 = self.arithmetic_expression()
        item2 = None
        if item1 is None:
            raise CompileError()
        op = None
        print(self.lexer.num)
        print(len(self.lexer.tokens))
        lex = self.lexer.next()
        if lex is not None:
            print(lex)
            if lex['type'] == 'OP_comparelike':
                op = lex
                item2 = self.arithmetic_expression()
                if item2 is None:
                    raise CompileError()
            else:
                raise CompileError()

        return Node(op, [item1, item2], node_name = 'expression')


    def operator():

    def operator_list_tail():

    def operator_list():
    
    def block(self):
        lex = self.lexer.next()
        if lex is None or lex['type'] != 'OP_blockopenbrackets':
            raise CompileError()
        item = self.operator_list()
        lex = self.lexer.next()
        if lex is None or lex['type'] != 'OP_blockclosebrackets':
            raise CompileError()


    def programm(self):
        item = self.block()
        self.root.operations = None
        self.root.nodes = [item, None]
        self.root.node_name = 'programm'

    def build(self, lexer):
        self.lexer = lexer
        self.expression()
        # print(self.lexer.num)
        # print(len(self.lexer.tokens))
        if self.lexer.num < len(self.lexer.tokens):
            raise CompileError()
            

class Compiler():
    def __init__(self):
        self.lexer = Lexer()
        self.astTreeBuilder = AstTreeBuilder()
    
    def compile(self, source):
        self.lexer.lex(source)
        root = self.astTreeBuilder.build(self.lexer)
        self.astTreeBuilder._draw_tree()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", help="path to code sps file", required=True)
    args = parser.parse_args()
    path = args.path

    compiler = Compiler()

    with open(path, 'r') as f:
        source = f.read()
        compiler.compile(source)
 

if __name__ == '__main__':
    main()
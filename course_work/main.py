import sys
from antlr4 import *
from grammar.LuaLexer import LuaLexer
from grammar.LuaParser import LuaParser
from LuaListener import LuaListener
from antlr4.tree.Trees import Trees
from utils import draw_tree, print_var_matrix, print_labels


def main(argv):
  input_stream = FileStream(argv[1], encoding = "cp1251")
  lexer = LuaLexer(input_stream)
  stream = CommonTokenStream(lexer)
  parser = LuaParser(stream)
  tree = parser.block()
  # print(Trees.toStringTree(tree, None, parser))
  listener = LuaListener()
  walker = ParseTreeWalker()
  walker.walk(listener, tree)
  listener.handleInfo()
  
  draw_tree(listener.function_dict)
  print_var_matrix(listener)
  print_labels(listener)
  
if __name__ == '__main__':
    main(sys.argv)
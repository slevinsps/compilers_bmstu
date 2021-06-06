import sys
from antlr4 import *
from grammar.LuaLexer import LuaLexer
from grammar.LuaParser import LuaParser
from LuaListener import LuaListener
from antlr4.tree.Trees import Trees
from utils import draw_tree


def main(argv):
  input_stream = FileStream(argv[1])
  lexer = LuaLexer(input_stream)
  stream = CommonTokenStream(lexer)
  parser = LuaParser(stream)
  tree = parser.block()
  listener = LuaListener()
  walker = ParseTreeWalker()
  walker.walk(listener, tree)
  listener.handleInfo()
  print(Trees.toStringTree(tree, None, parser))
  draw_tree(listener.function_dict)
 
if __name__ == '__main__':
    main(sys.argv)
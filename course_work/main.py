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
  print('-' * 100)
  print('Local vars')
  for key in listener.func_local_var_dict:
    local_vars =  list(listener.func_local_var_dict[key])
    if len(local_vars) != 0:
      print('func = ', key)
      print('local vars = ', local_vars)
  print('-' * 100)
  print('Global vars')
  for key in listener.func_global_var_dict:
    global_vars = list(listener.func_global_var_dict[key])
    if len(global_vars) != 0:
      print('func = ', key)
      print('global vars = ', global_vars)
 
if __name__ == '__main__':
    main(sys.argv)
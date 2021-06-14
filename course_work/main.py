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
  print(Trees.toStringTree(tree, None, parser))
  listener = LuaListener()
  walker = ParseTreeWalker()
  walker.walk(listener, tree)
  listener.handleInfo()
  

  
  draw_tree(listener.function_dict)
  print('-' * 100)
  print('Local vars')
  for key in listener.func_local_var_dict:
    global_vars = listener.func_local_var_dict[key]
    if len(global_vars) != 0:
      if listener.function_dict[key].local:
        print('local func', key, end = ' ')
      else:
        print('func', key, end = ' ')
      print(':', end = ' ')
      for var, value in global_vars.items():
        print(var, '=',  listener.func_var_dict[key][var], end = '; ')
      print()

  print('-' * 100)
  print('Global vars')
  for key in listener.func_global_var_dict:
    global_vars = listener.func_global_var_dict[key]
    if len(global_vars) != 0:
      if listener.function_dict[key].local:
        print('local func', key, end = ' ')
      else:
        print('func', key, end = ' ')
      print(':', end = ' ')
      for var, value in global_vars.items():
        print(var, '=',  listener.func_var_dict[key][var], end = '; ')
      print()
  
if __name__ == '__main__':
    main(sys.argv)
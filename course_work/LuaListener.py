from grammar.LuaListener import LuaListener as LuaListenerDeclaration
from exception import CompileError


class Node:
  def __init__(self, name):
    self.name = name
    self.next = []
  
class LuaListener(LuaListenerDeclaration):
  def __init__(self):
    super().__init__()
    self.base_name_function = '_G'
    self.function_dict = {self.base_name_function: Node(self.base_name_function)}
    self.func_var_dict = {}
    self.func_var_dict[self.base_name_function] = []
    self.func_local_var_dict = {}
    self.func_local_var_dict[self.base_name_function] = set()
    self.func_global_var_dict = {}
    self.func_global_var_dict[self.base_name_function] = set()
    self.func_func_dict = {}
    self.func_func_dict[self.base_name_function] = []
    self.defined_functions = [self.base_name_function]
    self.reserved_func_names = {'print' : ['string', None], 
                                'io.read' : ['string', 'string'], 
                               }

    self.current_var = None
    

  def handleInfo(self):
    for key, val in self.func_func_dict.items():
      for v in val:
        if v in self.function_dict:
          self.function_dict[key].next.append(self.function_dict[v]) 
        elif v in self.reserved_func_names:
          self.function_dict[key].next.append(Node(v)) 
        else:
          raise CompileError('No such function name ' +  str(v))

  def enterFuncname(self, ctx):
    # print('funcname = ', ctx.getText())
    funcname = ctx.getText()
    self.function_dict[funcname] = Node(funcname)
    self.defined_functions.append(funcname)
    self.func_var_dict[funcname] = []
    self.func_func_dict[funcname] = []
    self.func_local_var_dict[funcname] = set()
    self.func_global_var_dict[funcname] = set()

  def exitFuncname(self, ctx):
    pass

  def enterFuncbody(self, ctx):
    pass

  def exitFuncbody(self, ctx):
    self.defined_functions.pop()

  def enterPrefixexp(self, ctx):
    # print('prefixexp = ', ctx.getText())
    pass

  def exitPrefixexp(self, ctx):
    pass

  def enterVar_(self, ctx):
    # print('Var_ = ', ctx.getText())
    var_name = ctx.getText()
    current_funtion = self.defined_functions[-1]
    self.func_var_dict[current_funtion].append(var_name)
    self.current_var = var_name
    
  def exitVar_(self, ctx):
    pass

  def enterArgs(self, ctx):
    if self.current_var:
      current_funtion = self.defined_functions[-1]
      self.func_func_dict[current_funtion].append(self.current_var)
      self.current_var = None

  def exitArgs(self, ctx):
      pass

  def enterVarlist(self, ctx):
    global_var_name = ctx.getText()
    current_funtion = self.defined_functions[-1]
    self.func_global_var_dict[current_funtion].add(global_var_name)

  def exitVarlist(self, ctx):
    pass



  def enterAttnamelist(self, ctx):
    local_var_name = ctx.getText()
    current_funtion = self.defined_functions[-1]
    self.func_local_var_dict[current_funtion].add(local_var_name)

  def exitAttnamelist(self, ctx):
    pass

  def enterRetstat(self, ctx):
    # print('RETURN', ctx.getText())
    pass

  def exitRetstat(self, ctx):
    pass

  def enterEveryRule(self, ctx):
    # print(ctx.getText())
    pass
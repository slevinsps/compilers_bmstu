import string
from grammar.LuaListener import LuaListener as LuaListenerDeclaration
from exception import CompileError


class Node:
  def __init__(self, name, args = '', local = False):
    self.name = name
    self.local = local
    self.args = args
    self.next = []
  
class LuaListener(LuaListenerDeclaration):
  def __init__(self):
    super().__init__()
    self.base_name_function = '_G'
    self.function_dict = {self.base_name_function: Node(self.base_name_function)}
    self.func_var_dict = {}
    self.func_var_dict[self.base_name_function] = {}
    self.func_local_var_dict = {}
    self.func_local_var_dict[self.base_name_function] = {}
    self.func_global_var_dict = {}
    self.func_global_var_dict[self.base_name_function] = {}
    self.func_func_dict = {}
    self.func_func_dict[self.base_name_function] = []
    self.defined_functions = [self.base_name_function]
    self.reserved_func_names = {'print' : ['string', None], 
                                'io.read' : ['string', 'string'], 
                               }

    self.current_var_ = None
    self.labels = []
    
  def _add_function(self, funcname, args = '', local = False):
    self.function_dict[funcname] = Node(funcname, args, local)  
    self.defined_functions.append(funcname)
    self.func_var_dict[funcname] = {}
    self.func_func_dict[funcname] = []
    self.func_local_var_dict[funcname] = {}
    self.func_global_var_dict[funcname] = {}
    self.local_flag = False


  def _get_value(self, ctx):
    res = None 
    if ctx.number() is not None:
      res = (float(ctx.number().getText()), 'number')
    elif ctx.string() is not None:
      res = (ctx.string().getText().strip("'"), 'string')
    elif ctx.prefixexp() is not None:
      res = (ctx.prefixexp().getText(), 'prefixexp')
    else: 
      res = (ctx.getText(), 'other')
    return res
    
  def _get_exp_table(self, ctx):
    if ctx.tableconstructor() is None:
      return self._get_value(ctx)[0]

    field_dict = {}
    fieldlist = ctx.tableconstructor().fieldlist()
    if fieldlist is not None:
      for field in fieldlist.field():
        key = field.NAME().getText()
        value = self._get_exp_table(field.exp()[0])
        field_dict[key] = value
    
    return field_dict

  def _update_variables(self, ctx, mode = 'global'):

    if mode == 'global':
      ctx_list = ctx.varlist
      var_dict = self.func_global_var_dict
    elif mode == 'local':
      ctx_list = ctx.attnamelist
      var_dict = self.func_local_var_dict
    else:
      return 

    if ctx_list() is not None:
      vars_array = []
      exp_array = []

      if mode == 'global':
        var_names = ctx_list().var_()
      elif mode == 'local':
        var_names = ctx_list().NAME()
      
      # название переменных
      childs_varlist = list(var_names)
      for i in range(len(childs_varlist)):
        var_name = childs_varlist[i].getText()
        var_fields = []
        if childs_varlist[i].getChildCount() > 0 and childs_varlist[i].varSuffix() is not None and len(childs_varlist[i].varSuffix()) != 0:
          var_name = childs_varlist[i].NAME().getText()
          for j in range(len(childs_varlist[i].varSuffix())):
            if childs_varlist[i].varSuffix()[j].exp() is not None:
              var_field, var_type = self._get_value(childs_varlist[i].varSuffix()[j].exp())
              if var_type != 'string' and var_type != 'number':
                raise CompileError('Error in table suffix type: ' +  str(var_field))
            else:
              var_field = childs_varlist[i].varSuffix()[j].NAME().getText()
            var_fields.append(var_field)
        vars_array.append({'name': var_name, 'field': var_fields})
      # значение переменных
      childs_explist = list(ctx.explist().exp())
      for i in range(len(childs_explist)):
        if childs_explist[i].tableconstructor() is not None:
          field_dict = self._get_exp_table(childs_explist[i])
          exp_array.append(field_dict)
        else:
          exp_array.append(self._get_value(childs_explist[i])[0])

      # присваивание переменных
      for i in range(len(vars_array)):
        res = 'nil'
        if i < len(exp_array):
          res = exp_array[i]
        
        var = vars_array[i]
        current_funtion = self.defined_functions[-1]
        if len(var['field']) > 0:
          var_dict_current = var_dict[current_funtion][var['name']]
          func_var_dict = self.func_var_dict[current_funtion][var['name']]
          for j in range(len(var['field']) - 1):
            var_dict_current = var_dict_current[var['field'][j]]
            func_var_dict = func_var_dict[var['field'][j]]
          
          var_dict_current[var['field'][-1]] = res
          func_var_dict[var['field'][-1]] = res
        else:
          var_dict[current_funtion][var['name']] = res
          self.func_var_dict[current_funtion][var['name']] = res


  def handleInfo(self):
    for key, val in self.func_func_dict.items():
      for v in val:
        if v in self.function_dict:
          self.function_dict[key].next.append(self.function_dict[v]) 
        elif v in self.reserved_func_names:
          self.function_dict[key].next.append(Node(v)) 
        else:
          raise CompileError('No such function name ' +  str(v))


  def enterStat(self, ctx):
    self._update_variables(ctx, 'global')
    self._update_variables(ctx, 'local')
    if ctx.label() is not None:
      label_name = ctx.label().NAME().getText()
      self.labels.append(label_name)

  def exitStat(self, ctx):
    pass

  def enterFuncname(self, ctx):
    pass
    

  def exitFuncname(self, ctx):
    pass

  def enterFuncbody(self, ctx):
    childs_parent = list(ctx.parentCtx.getChildren())
    args = ''
    if ctx.parlist() is not None:
      args = ctx.parlist().getText()
   
    local = False
    if childs_parent[0].getText() == 'local':
      local = True
      funcname = childs_parent[2].getText()
    else:
      if len(childs_parent) == 3:
        funcname = childs_parent[1].getText()
      else:
        current_funtion = self.defined_functions[-1]
        funcname = current_funtion + '_<inner_returned_func>'
    self._add_function(funcname, args, local)
    

  def exitFuncbody(self, ctx):
    self.defined_functions.pop()

  def enterPrefixexp(self, ctx):
    pass

  def exitPrefixexp(self, ctx):
    pass

  def enterVar_(self, ctx):
    var_name = ctx.getText()
    self.current_var_ = var_name
    
  def exitVar_(self, ctx):
    pass

  def enterArgs(self, ctx):
    if self.current_var_:
      current_funtion = self.defined_functions[-1]
      self.func_func_dict[current_funtion].append(self.current_var_)
      self.current_var_ = None

  def exitArgs(self, ctx):
      pass

  def enterVarlist(self, ctx):
    pass

  def exitVarlist(self, ctx):
    pass


  def enterExplist(self, ctx):
    pass

  def exitExplist(self, ctx):
    pass

  def enterAttnamelist(self, ctx):
    pass

  def exitAttnamelist(self, ctx):
    pass

  def enterRetstat(self, ctx):
    pass

  def exitRetstat(self, ctx):
    pass

  def enterEveryRule(self, ctx):
    pass
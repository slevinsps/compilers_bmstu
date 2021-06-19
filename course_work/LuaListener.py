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
    self.func_var_type_dict = {}
    self.func_var_type_dict[self.base_name_function] = {}
    self.func_local_var_dict = {}
    self.func_local_var_dict[self.base_name_function] = {}
    self.func_global_var_dict = {}
    self.func_global_var_dict[self.base_name_function] = {}
    self.func_func_dict = {}
    self.func_func_dict[self.base_name_function] = []
    self.defined_functions = [self.base_name_function]
    self.reserved_func_names = {'print' : ['string', None], 
                                'io.read' : ['string', 'string'],
                                'ipairs' : [],
                                'pairs': [],
                                'error' : []
                               }

    self.current_var_ = None
    self.labels = []
    
  def _add_function(self, funcname, args = '', local = False, parent = None):
    self.function_dict[(funcname, parent)] = Node((funcname, parent), args, local) 
    self.defined_functions.append((funcname, parent))
    self.func_var_dict[(funcname, parent)] = {}
    self.func_var_type_dict[(funcname, parent)] = {}
    self.func_func_dict[(funcname, parent)] = []
    self.func_local_var_dict[(funcname, parent)] = {}
    self.func_global_var_dict[(funcname, parent)] = {}
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
      res = (ctx.getText(), 'expression')
    return res
    
  def _get_exp_table(self, ctx):
    if ctx.tableconstructor() is None:
      var_field, var_type = self._get_value(ctx)
      if var_type == 'prefixexp':
        if len(ctx.prefixexp().nameAndArgs()) != 0:
          var_field = f'<func> {var_field}'
        else:
          var_field = f'<var> {var_field}'
      return var_field, var_type


    field_dict = {}
    array = {}
    counter = 1
    fieldlist = ctx.tableconstructor().fieldlist()
    if fieldlist is not None:
      for field in fieldlist.field():
        value, type_ = self._get_exp_table(field.exp()[0])
        if field.NAME() is None:
          if field.getText()[0] == '[':
            key, key_type_ = self._get_exp_table(field.exp()[0])
            value, val_type_ = self._get_exp_table(field.exp()[1])
            if key_type_ == 'string':
              key = key.strip('"')
              field_dict[key] = value
            elif key_type_ == 'number':
              key = int(key)
              if key < 1:
                raise CompileError(f'Index {key} out of range')
              array[key] = value
          else:
            array[counter] = value
            counter += 1
        else:
          key = field.NAME().getText()
          field_dict[key] = value
    return {'dict': field_dict, 'array': array, 'methods': []}, 'table'

  def _update_variables(self, ctx, mode = 'global'):

    if mode == 'global':
      ctx_list = ctx.varlist
      var_dict = self.func_global_var_dict
      var_dict_other = self.func_local_var_dict
    elif mode == 'local':
      ctx_list = ctx.attnamelist
      var_dict = self.func_local_var_dict
      var_dict_other = self.func_global_var_dict
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
              if var_type == 'number':
                var_field = int(var_field)
              elif var_type == 'prefixexp':
                var_field = f'<var> {var_field}'
                print('AAA', var_field)
                return 
              elif var_type == 'string':
                var_field = var_field.replace('"', '').replace("'", '')
              else:
                raise CompileError('Error in table suffix type: ' +  str(var_field))
            else:
              var_field = childs_varlist[i].varSuffix()[j].NAME().getText()
            var_fields.append(var_field)
        vars_array.append({'name': var_name, 'field': var_fields})

      # значение переменных
      childs_explist = list(ctx.explist().exp())
      for i in range(len(childs_explist)):
        if childs_explist[i].tableconstructor() is not None:
          var_value, var_type = self._get_exp_table(childs_explist[i])
          exp_array.append([var_value, var_type])
        else:
          var_field, var_type = self._get_value(childs_explist[i])
          if var_type == 'prefixexp':
            if len(childs_explist[i].prefixexp().nameAndArgs()) != 0:
              var_type = 'func'
              var_field = f'<func> {var_field}'
            else:
              var_type = 'var'
              var_field = f'<var> {var_field}'
          exp_array.append([var_field, var_type])

      # присваивание переменных
      for i in range(len(vars_array)):
        res = ['nil', 'nil']
        if i < len(exp_array):
          res = exp_array[i]
        
        var = vars_array[i]
        current_funtion = self.defined_functions[-1]
        if len(var['field']) > 0:
          if var['name'] not in self.func_var_dict[current_funtion]:
            if var['name'] not in self.function_dict[current_funtion].args:
              var_name = var['name']
              raise CompileError(f'No such variable {var_name}')
            else:
              self.func_var_dict[current_funtion][var['name']] = [{}, {}]

          func_var_dict = self.func_var_dict[current_funtion][var['name']]
          for j in range(len(var['field']) - 1):
            field = var['field'][j]
            dict_, array_ = func_var_dict['dict'], func_var_dict['array']
            if type(field) == int and field >= 1 and field <= len(array_):
              func_var_dict = array_[field]
            else:
              func_var_dict = dict_[field]

          field = var['field'][-1]
          if type(field) == int:
            if field >= 1:
              func_var_dict['array'][field] = res[0]
            else:
              raise CompileError(f'Index {field} out of range')
          else:
            func_var_dict['dict'][field] = res[0]

        else:
          var_dict[current_funtion][var['name']] = res[0]
          if var['name'] in var_dict_other[current_funtion]:
            del var_dict_other[current_funtion][var['name']]

          self.func_var_dict[current_funtion][var['name']] = res[0]
          self.func_var_type_dict[current_funtion][var['name']] = res[1]


  def handleInfo(self):
    for key, val in self.func_func_dict.items():
     
      for v in val:
        var_name = v[0]['name'] 
        var_name_orig = v[0]['name_orig']
        fields = v[0]['field']
        current_funtion = v[1]
        full_name = (var_name_orig, current_funtion)

        v_copy = full_name
        base_func = v_copy[0]
        v_arr = [full_name]
        while v_copy != self.base_name_function:
          v_copy = v_copy[1]
          v_arr.append((base_func, v_copy))
        
        check_flag = False
        for v_nested in v_arr:
          if v_nested in self.function_dict:
            check_flag = True
            self.function_dict[key].next.append(self.function_dict[v_nested]) 
            break
          elif v_nested[0] in self.reserved_func_names:
            check_flag = True
            self.function_dict[key].next.append(Node((v_nested[0], self.base_name_function))) 
            break
          # elif v_nested[0] in self.func_var_dict[key] or v_nested[0] in self.function_dict[key].args:
          #   check_flag = True
          #   break
        if not check_flag:
          exist_var, exist_method = self._check_var_exists(v[0], current_funtion)
          func_name = var_name_orig
          if exist_method:
            func_name = var_name_orig
          else:
            if exist_var:
              func_name = '<var> ' + var_name_orig
            else:
              if var_name not in self.function_dict[current_funtion].args:
                raise CompileError(f'No such function {var_name}')
              else:
                func_name = '<arg> ' + var_name_orig
          self.function_dict[key].next.append(Node((func_name, current_funtion))) 

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
    local = False
    current_funtion = self.defined_functions[-1]
    if current_funtion != self.base_name_function:
      local = True
    childs_parent = list(ctx.parentCtx.getChildren())
    args = ''
    if ctx.parlist() is not None:
      args = ctx.parlist().getText().split(',')
   
    if childs_parent[0].getText() == 'local':
      local = True
      funcname = childs_parent[2].getText()
    else:
      if len(childs_parent) == 3:
        funcname = childs_parent[1].getText()

        if '.' in funcname:
          table_name = funcname.split('.')[0]
          if table_name not in self.func_var_dict[current_funtion] and table_name not in self.function_dict[current_funtion].args:
            raise CompileError(f'No such table {table_name}')

          fields = funcname.split('.')[1:-1]
          local = True
          if table_name in self.func_var_dict[current_funtion]:
            func_var_dict = self.func_var_dict[current_funtion][table_name]
            if len(fields) == 0:
              func_var_dict['methods'].append(funcname)
            else:
              for j in range(len(fields) - 1):
                dict_, array_ = func_var_dict['dict'], func_var_dict['array']
                if type(fields[j]) == int and fields[j] >= 1 and fields[j] <= len(array_):
                  if fields[j] not in array_:
                    raise CompileError(f'No such field {fields[j]}')
                  func_var_dict = array_[fields[j]]
                else:
                  if fields[j] not in dict_:
                    raise CompileError(f'No such field {fields[j]}')
                  func_var_dict = dict_[fields[j]]

              field = fields[-1]
              if type(field) == int:
                if field >= 1:
                  if field not in func_var_dict['array'] or type(func_var_dict['array'][field]) is not dict:
                    raise CompileError(f'No such field {field}')
                  func_var_dict['array'][field]['methods'].append(funcname)
                else:
                  raise CompileError(f'Index {field} out of range')
              else:
                if field not in func_var_dict['dict'] or type(func_var_dict['dict'][field]) is not dict:
                  raise CompileError(f'No such field {field}')
                func_var_dict['dict'][field]['methods'].append(funcname)         
      else:
        funcname = current_funtion[0] + '_<inner_returned_func>'
    self._add_function(funcname, args, local, current_funtion)
    

  def exitFuncbody(self, ctx):
    self.defined_functions.pop()

  def enterPrefixexp(self, ctx):
    pass

  def exitPrefixexp(self, ctx):
    pass

  def enterVar_(self, ctx):
    var_name = ctx.getText()
    self.current_var_ = ctx
    
  def exitVar_(self, ctx):
    pass


  def _check_var_exists(self, var, current_funtion):
    var_name = var['name'] 
    fields = var['field']
    method_name = '.'.join([var_name] + fields)
    exist_var = False
    exist_method = False
    if var_name in self.func_var_dict[current_funtion]:
      func_var_dict = self.func_var_dict[current_funtion][var_name]
      if len(fields) == 0:
        exist_var = True
      else:
        for j in range(len(fields) - 1):
          dict_, array_ = func_var_dict['dict'], func_var_dict['array']
          if type(fields[j]) == int and fields[j] >= 1 and fields[j] <= len(array_):
            if fields[j] not in array_:
              raise CompileError(f'No such field {fields[j]}')
            func_var_dict = array_[fields[j]]
          else:
            if fields[j] not in dict_:
              raise CompileError(f'No such field {fields[j]}')
            func_var_dict = dict_[fields[j]]

        field = fields[-1]
        if type(field) == int:
          if field >= 1:
            if field not in func_var_dict['array']:
              raise CompileError(f'No such field {field}')
            exist_var = True
          else:
            raise CompileError(f'Index {field} out of range')
        else:
          if field not in func_var_dict['dict']:
            if method_name not in func_var_dict['methods']:
              raise CompileError(f'No such field {field}')
            else:
              exist_method = True
          exist_var = True

    return exist_var, exist_method

  def enterArgs(self, ctx):

    if not self.current_var_:
      return 

    var_name = self.current_var_.getText()
    var_name_orig = self.current_var_.getText()
    var_fields = []
    if self.current_var_.varSuffix() is not None and len(self.current_var_.varSuffix()) != 0:
      var_name = self.current_var_.NAME().getText()
      for j in range(len(self.current_var_.varSuffix())):
        if self.current_var_.varSuffix()[j].exp() is not None:
          var_field, var_type = self._get_value(self.current_var_.varSuffix()[j].exp())
          if var_type == 'number':
            var_field = int(var_field)
          elif var_type == 'prefixexp':
            var_field = f'<var> {var_field}'
          elif var_type == 'string':
            var_field = var_field.replace('"', '').replace("'", '')
          else:
            raise CompileError('Error in table suffix type: ' +  str(var_field))
        else:
          var_field = self.current_var_.varSuffix()[j].NAME().getText()
        var_fields.append(var_field)
    var = {'name': var_name, 'field': var_fields, 'name_orig': var_name_orig}

    # var_name = self.current_var_.getText()
    current_funtion = self.defined_functions[-1]
    
    self.func_func_dict[current_funtion].append((var, current_funtion))
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
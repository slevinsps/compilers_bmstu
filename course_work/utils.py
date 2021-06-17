import networkx as nx
import random
import matplotlib.pyplot as plt
from terminaltables import AsciiTable
from networkx.drawing.nx_agraph import to_agraph


def hierarchy_pos(G, root=None, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5):
  if not nx.is_tree(G):
      raise TypeError('cannot use hierarchy_pos on a graph that is not a tree')

  if root is None:
      if isinstance(G, nx.DiGraph):
          root = next(iter(nx.topological_sort(G)))  
      else:
          root = random.choice(list(G.nodes))

  def _hierarchy_pos(G, root, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5, pos = None, parent = None):
      if pos is None:
          pos = {root:(xcenter,vert_loc)}
      else:
          pos[root] = (xcenter, vert_loc)
      children = list(G.neighbors(root))
      if not isinstance(G, nx.DiGraph) and parent is not None:
          children.remove(parent)  
      if len(children)!=0:
          dx = width/len(children) 
          nextx = xcenter - width/2 - dx/2
          for child in children:
              nextx += dx
              pos = _hierarchy_pos(G,child, width = dx, vert_gap = vert_gap, 
                                  vert_loc = vert_loc-vert_gap, xcenter=nextx,
                                  pos=pos, parent = root)
      return pos     
  return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)

def get_nodes_edges(function_dict):
  nodes, edges = [], []
  for key, val in function_dict.items():
    if len(val.next) == 0:
      continue
    nodes.append(f'{key}({str(val.args)})' )

    for i in range(len(val.next)):
      edges.append([f'{key}({val.args})', f'{val.next[i].name}({val.next[i].args})' ])
  return nodes, edges



def draw_tree(function_dict, file_name = "func_call.png"):

  nodes, edges = get_nodes_edges(function_dict)
  G=nx.MultiDiGraph()

  for i in range(len(nodes)):
    G.add_node(nodes[i])
  
  for i in range(len(edges)):
    G.add_edge(edges[i][0], edges[i][1])

  G.graph['edge'] = {'arrowsize': '1', 'splines': 'curved'}
  G.graph['graph'] = {'scale': '3'}

  A = to_agraph(G)
  A.layout('dot')
  A.draw(file_name)

def chunkstring(string, length):
  return (string[0+i:length+i] for i in range(0, len(string), length))

def get_matrix(listener, num_func, local_flag = False):
  matrix = [[''] * 4 for i in range(num_func + 1)]
  matrix[0][1], matrix[0][2], matrix[0][3] = 'funcname', 'global', 'local'
  func_count = 1
  for name, variables in listener.func_var_dict.items():
    if local_flag != listener.function_dict[name].local:
      continue
    args = listener.function_dict[name].args
    matrix[func_count][0] = func_count
    func_name = f'{name}({args})'
    str_ = '\n'.join(chunkstring(func_name, 40))
    matrix[func_count][1] = str_

    global_vars = listener.func_global_var_dict[name]
    local_vars = listener.func_local_var_dict[name]
    for var, value in global_vars.items():
      str_ = f'{var}={listener.func_var_dict[name][var]}\n'
      str_ = '\n'.join(chunkstring(str_, 50))
      type_ = listener.func_var_type_dict[name][var]
      matrix[func_count][2] += f'{str_} | type = {type_}\n'
    if len(global_vars) == 0:
      matrix[func_count][2] = '-'
    for var, value in local_vars.items():
      str_ = f'{var}={listener.func_var_dict[name][var]}\n'
      str_ = '\n'.join(chunkstring(str_, 50))
      type_ = listener.func_var_type_dict[name][var]
      matrix[func_count][3] += f'{str_} | type = {type_}\n'
    if len(local_vars) == 0:
      matrix[func_count][3] = '-'
    func_count += 1
  return matrix

def print_var_matrix(listener):
  num_local_functions = 0
  num_global_functions = 0
  for name, variables in listener.func_var_dict.items():
    if listener.function_dict[name].local:
      num_local_functions += 1
    else:
      num_global_functions += 1

  print('Global functions:')
  matrix = get_matrix(listener, num_global_functions, False)
  table = AsciiTable(matrix)
  table.inner_row_border = True
  print(table.table)
  print('\n\n')
  print('Local functions:')
  matrix = get_matrix(listener, num_local_functions, True)
  table = AsciiTable(matrix)
  table.inner_row_border = True
  print(table.table)

def print_labels(listener):
  print('Labels:')
  if len(listener.labels) == 0:
    print('<no lables>')
  for i in range(len(listener.labels)):
    print(listener.labels[i])
import networkx as nx
import random
import matplotlib.pyplot as plt
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
    nodes.append(key)

    for i in range(len(val.next)):
      edges.append([key, val.next[i].name])
  return nodes, edges



def draw_tree(function_dict, file_name = "func_call.png"):

  nodes, edges = get_nodes_edges(function_dict)
  G=nx.MultiDiGraph()

  for i in range(len(nodes)):
    G.add_node(nodes[i])
  
  for i in range(len(edges)):
    G.add_edge(edges[i][0], edges[i][1])

  # # pos = hierarchy_pos(G)
  # pos = nx.spring_layout(G,k=0.15,iterations=20)
  # nx.draw_networkx_labels(G, pos, font_size = 7)
  # nx.draw_networkx_edges(G, pos, arrows=True, arrowstyle='-|>', width = 0.5, arrowsize = 3)
  # plt.savefig(file_name)


  G.graph['edge'] = {'arrowsize': '1', 'splines': 'curved'}
  G.graph['graph'] = {'scale': '3'}

  A = to_agraph(G)
  A.layout('dot')
  A.draw(file_name)

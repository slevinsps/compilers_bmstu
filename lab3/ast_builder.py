import networkx as nx
import matplotlib.pyplot as plt
from exception import CompileError

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
        self.operations_after_expression = set(
            ['OP_blockopenbrackets', 'OP_blockclosebrackets', 'OP_sep']
        )
        self.count = {'f': 0, 'i': 0, 't': 0, 'ae': 0, 
                      'e': 0, 'o': 0, 'olt': 0, 
                      'ol': 0, 'b': 0, 'p': 0}

    def hierarchy_pos(self, G, root=None, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5):
        import random
        '''
        From Joel's answer at https://stackoverflow.com/a/29597209/2966723.  
        Licensed under Creative Commons Attribution-Share Alike 
        
        If the graph is a tree this will return the positions to plot this in a 
        hierarchical layout.
        
        G: the graph (must be a tree)
        
        root: the root node of current branch 
        - if the tree is directed and this is not given, 
        the root will be found and used
        - if the tree is directed and this is given, then 
        the positions will be just for the descendants of this node.
        - if the tree is undirected and not given, 
        then a random choice will be used.
        
        width: horizontal space allocated for this branch - avoids overlap with other branches
        
        vert_gap: gap between levels of hierarchy
        
        vert_loc: vertical location of root
        
        xcenter: horizontal location of root
        '''
        if not nx.is_tree(G):
            raise TypeError('cannot use hierarchy_pos on a graph that is not a tree')

        if root is None:
            if isinstance(G, nx.DiGraph):
                root = next(iter(nx.topological_sort(G)))  #allows back compatibility with nx version 1.11
            else:
                root = random.choice(list(G.nodes))

        def _hierarchy_pos(G, root, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5, pos = None, parent = None):
            '''
            see hierarchy_pos docstring for most arguments

            pos: a dict saying where all nodes go if they have been assigned
            parent: parent of this branch. - only affects it if non-directed

            '''
        
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

    def _draw_tree(self):
        # children = self.root.nodes
        # print(self.root.node_name + ' -', end = ' ')
        # print('op:', self.root.operations, end = ' ')
        # print('nodes:', end = ' ')
        # for i, n in enumerate(self.root.nodes):
        #     if n is not None and not n.is_leaf:
        #         print(str(i + 1) + ' - ' + n.node_name, end = ' ')
        # print('\n' + '-' * 50)
        # while len(children) > 0:
        #     new_children = []
        #     for i in range(len(children)):
        #         if children[i] is None:
        #             continue

        #         print(str(i + 1) + ' - ' + children[i].node_name + ' -', end = ' ')
        #         print('op:', children[i].operations, end = ' ')
        #         print('nodes:', end = ' ')
        #         if children[i].is_leaf:
        #             print(children[i].nodes[0], end = ' ')
        #         else:
        #             for j, n in enumerate(children[i].nodes):
        #                 if n is not None:
        #                     print(str(j + 1) + ' - ' + n.node_name, end = ' ')
        #         print('\n' + '-' * 50)
        #         if children[i].nodes is not None and not children[i].is_leaf:
        #             new_children += children[i].nodes
        #     print('~' * 100)
        #     children = new_children
        G=nx.DiGraph()

        children = self.root.nodes
        G.add_node(self.root.node_name)
        
        for i, n in enumerate(self.root.nodes):
            if n is not None and not n.is_leaf:
                G.add_edge(self.root.node_name, n.node_name)
        while len(children) > 0:
            new_children = []
            for i in range(len(children)):
                if children[i] is None:
                    continue
                
                G.add_node(children[i].node_name)
                if not children[i].is_leaf:
                    for j, n in enumerate(children[i].nodes):
                        if n is not None:
                            G.add_edge(children[i].node_name, n.node_name)
                if children[i].nodes is not None and not children[i].is_leaf:
                    new_children += children[i].nodes
            children = new_children

        pos = self.hierarchy_pos(G)
        # pos = nx.spring_layout(G,k=0.15,iterations=20)
        # T = nx.balanced_tree(2, 5)
        # pos = graphviz_layout(T, prog="twopi")
        # nx.draw_networkx_nodes(G, pos,  node_size = 1000)
        nx.draw_networkx_labels(G, pos, font_size = 7)
        nx.draw_networkx_edges(G, pos, arrows=True, arrowstyle='-|>', width = 0.5, arrowsize = 1)
        plt.savefig("graph.png") # save as png

    def _get_name(self, name, op, val = None):
        new_name = name + str(self.count[name])
        self.count[name] += 1
        if op is not None:
            new_name += ' op: ' + op['value']
        if val is not None and type(val) != Node:
            new_name += 'v:' + val['value']
        return new_name

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
            res = Node(None, [item, None], is_leaf = is_leaf, 
                       node_name = self._get_name('f', None, item))
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
                    item1 = Node(op, [item1, item2], 
                                node_name = self._get_name('t', op))
                op = lex
                item2 = self.factor()
                if item2 is None:
                    raise CompileError()
                
                lex = self.lexer.next()
            else:
                self.lexer.prev()
 
        res = Node(op, [item1, item2], 
                    node_name = self._get_name('t', op))
        return res
                   

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
                    item1 = Node(op, [item1, item2], node_name = self._get_name('ae', op))
                op = lex
                item2 = self.term()
                if item2 is None:
                    raise CompileError()
                
                lex = self.lexer.next()
            else:
                self.lexer.prev()
        return Node(op, [item1, item2], node_name = self._get_name('ae', op))
        
    def expression(self, ):
        item1 = self.arithmetic_expression()
        item2 = None
        if item1 is None:
            raise CompileError()
        op = None
        # print(self.lexer.num)
        # print(len(self.lexer.tokens))
        lex = self.lexer.next()
        if lex is not None:
            if lex['type'] == 'OP_comparelike':
                op = lex
                item2 = self.arithmetic_expression()
                if item2 is None:
                    raise CompileError()
            elif lex['type'] not in self.operations_after_expression:
                # print(lex)
                raise CompileError()
            else:
                self.lexer.prev()

        return Node(op, [item1, item2], node_name = self._get_name('e', op))


    def operator(self):
        lex = self.lexer.next()
        if lex is None or lex['type'] != 'NAME':
            raise CompileError()
        item1 = Node(None, [lex, None], is_leaf = True, node_name = self._get_name('i', None, lex))
        lex = self.lexer.next()
        if lex is None or lex['type'] != 'OP_assignment':
            raise CompileError()

        op = lex
        item2 = self.expression()

        if item2 is None:
            raise CompileError()

        return Node(op, [item1, item2], node_name = self._get_name('o', op))

    def operator_list_tail(self):
        items = []
        lex = self.lexer.next()
        if lex is None or lex['type'] != 'OP_sep':
            self.lexer.prev()
            return None
        item = self.operator()
        if item is None:
            raise CompileError()

       

        items = [item]    
        item = self.operator_list_tail()
        if item is not None:
            items += item.nodes

        return Node(None, items, node_name = self._get_name('olt', None))

    def operator_list(self):
        item = self.operator()
        items = [item]
        item = self.operator_list_tail()
        if item is not None:
            items += item.nodes
        return Node(None, items, node_name = self._get_name('ol', None))

    def block(self):
        lex = self.lexer.next()
        if lex is None or lex['type'] != 'OP_blockopenbrackets':
            raise CompileError()
        item = self.operator_list()
        lex = self.lexer.next()

        if lex is None or lex['type'] != 'OP_blockclosebrackets':
            raise CompileError()

        return Node(None, [item, None], node_name = self._get_name('b', None))

    def programm(self):
        item = self.block()
        self.root.operations = None
        self.root.nodes = [item, None]
        self.root.node_name = self._get_name('p', None)

    def build(self, lexer):
        self.lexer = lexer
        self.programm()
        # print(self.lexer.num)
        # print(len(self.lexer.tokens))
        if self.lexer.num < len(self.lexer.tokens):
            raise CompileError()
            
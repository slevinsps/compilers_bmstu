# regex engine in Python
# parser and classes
# xiayun.sun@gmail.com
# 06-JUL-2013

import pdb

class Token:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return self.name + ":" + self.value

class Lexer:
    def __init__(self, pattern):
        self.source = pattern
        self.symbols = {'(':'LEFT_PAREN', ')':'RIGHT_PAREN', '*':'STAR', '|':'ALT', '\x08':'CONCAT', '+':'PLUS', '?':'QMARK'}
        self.current = 0
        self.length = len(self.source)
       
    def get_token(self): 
        
        if self.current < self.length:
            c = self.source[self.current]
            self.current += 1
            if c not in self.symbols.keys(): # CHAR
                token = Token('CHAR', c)
            else:
                token = Token(self.symbols[c], c)
            return token
        else:
            return Token('NONE', '')

class ParseError(Exception):pass

'''
Grammar for regex:

regex = exp $

exp      = term [|] exp      {push '|'}
         | term
         |                   empty?

term     = factor term       chain {add \x08}
         | factor

factor   = primary [*]       star {push '*'}
         | primary [+]       plus {push '+'}
         | primary [?]       optional {push '?'}
         | primary

primary  = \( exp \)
         | char              literal {push char}
'''

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.tokens = []
        self.lookahead = self.lexer.get_token()
    
    def consume(self, name):
        if self.lookahead.name == name:
            self.lookahead = self.lexer.get_token()
        elif self.lookahead.name != name:
            raise ParseError

    def parse(self):
        self.exp()
        return self.tokens
    
    def exp(self):
        self.term()
        if self.lookahead.name == 'ALT':
            t = self.lookahead
            self.consume('ALT')
            self.exp()
            self.tokens.append(t)

    def term(self):
        self.factor()
        if self.lookahead.value not in ')|':
            self.term()
            self.tokens.append(Token('CONCAT', '\x08'))
    
    def factor(self):
        self.primary()
        if self.lookahead.name in ['STAR', 'PLUS', 'QMARK']:
            self.tokens.append(self.lookahead)
            self.consume(self.lookahead.name)

    def primary(self):
        if self.lookahead.name == 'LEFT_PAREN':
            self.consume('LEFT_PAREN')
            self.exp()
            self.consume('RIGHT_PAREN')
        elif self.lookahead.name == 'CHAR':
            self.tokens.append(self.lookahead)
            self.consume('CHAR')

class State:
    def __init__(self, name):
        self.epsilon = [] # epsilon-closure
        self.transitions = {} # char : state
        self.name = name
        self.is_end = False
        self.is_start = False

    def __str__(self):
        return self.name + ' ' + str(self.is_end) + ' ' + str(self.is_start)

class NodeGraph:
    def __init__(self, start, end):
        self.start = start
        self.end = end # start and end states
        end.is_end = True   

class DFA:
    def __init__(self):
        self.start = None
        self.end = None 
        self.alphabet = []
        self.start_state = []


    def _get_epsilon_closure_recur(self, state, epsilon_closure):
        if state in epsilon_closure:
                return
        epsilon_closure.add(state)
        for eps in state.epsilon:
            self._get_epsilon_closure_recur(eps, epsilon_closure)

    def get_epsilon_closure(self, state):
        epsilon_closure = set()
        self._get_epsilon_closure_recur(state, epsilon_closure)
        return epsilon_closure

    def convert_nfa_to_dfa(self, nfa):
        # nfa.print_graph()

        end_state_set = nfa.end_state
        start_state_set = set([nfa.nfa_head.start])

        start_state = nfa.nfa_head.start
        self.alphabet = nfa.alphabet

        union_state_array = []
        new_transition_array = []
        index_state_array = 0

        
        epsilon_closure = list(self.get_epsilon_closure(start_state))
        union_state_array.append(set(epsilon_closure))

        while index_state_array < len(union_state_array):
            transition = {char: [] for char in self.alphabet}
            epsilon_closure = list(union_state_array[index_state_array])

            for i in range(len(epsilon_closure)): # переходы по символам алфавита в эпсилон окрестности
                for char, value in epsilon_closure[i].transitions.items():
                    transition[char].append(value)
            for char, value in transition.items(): # добавление новых состояний в таблицу
                if len(value) == 0:
                    continue
                
                new_state = []
                for i in range(len(value)):
                    epsilon_closure = list(self.get_epsilon_closure(value[i]))
                    new_state.extend(epsilon_closure)

                transition[char] = new_state
                if set(new_state) not in union_state_array:
                    union_state_array.append(set(new_state))


            new_transition_array.append(transition)
            index_state_array += 1
        
        res_state_array = [State('s' + str(i)) for i in range(len(union_state_array))]
        for i in range(len(union_state_array)):
            if not end_state_set.isdisjoint(union_state_array[i]): # имеют пересечение
                res_state_array[i].is_end = True

            if not start_state_set.isdisjoint(union_state_array[i]): # имеют пересечение
                res_state_array[i].is_start = True

        for i in range(len(new_transition_array)):
            for char, union_state in new_transition_array[i].items():
                if len(union_state) == 0:
                    continue
                index_of_state = union_state_array.index(set(union_state))
                res_state_array[i].transitions[char] = res_state_array[index_of_state]
                
        for i in range(len(res_state_array)):
            if res_state_array[i].is_start:
                self.start_state.append(res_state_array[i])
        # print('new states:')
        # for i in range(len(union_state_array)):
        #     print(i, ':', end = ' ')
        #     arr = list(union_state_array[i])
        #     for a in arr:
        #         print(a, end = ' ')
        #     print()
        # print('---')
        # for i in range(len(new_transition_array)):
        #     print(i, ':', end = ' ')
        #     for key, value in new_transition_array[i].items():
        #         print(key, end = ': ')
        #         for a in value:
        #             print(a, end = ' ')
        #     print()

        # for i in range(len(res_state_array)):
        #     print(res_state_array[i], end = '-> ')
        #     for key, value in res_state_array[i].transitions.items():
        #         print(key, end = ': ')
        #         print(value, end = ' ')
        #     print()

    def match(self,s):
        if not self.start_state:
            print('Build before please')
            return
        
        current_states = self.start_state
        for c in s:
            next_states = set()
            for state in current_states:
                if c in state.transitions.keys():
                    trans_state = state.transitions[c]
                    next_states.add(trans_state)
           
            current_states = next_states

        for s in current_states:
            if s.is_end:
                return True
        return False



class NFA:
    def __init__(self):
        self.alphabet = []
        self.nfa_stack = []
        self.state_count = 0
        self.handlers = {'CHAR':self.handle_char, 'CONCAT':self.handle_concat,
                         'ALT':self.handle_alt, 'STAR':self.handle_rep,
                         'PLUS':self.handle_rep, 'QMARK':self.handle_qmark}
        self.nfa_head = None
        self.end_state = set()

    def print_graph(self):
        ind = 0
        state_array = []
        state_array.append(self.nfa_head.start)
        while ind < len(state_array):
            current_state = state_array[ind]
            print(ind, ')', 'from:', current_state)
            print('by epsilon to:', end=' ')
            for eps_state in current_state.epsilon:
                print(eps_state, end=' ')
                if eps_state not in state_array:
                    state_array.append(eps_state)
                    
            print()
            for char, state in current_state.transitions.items():
                print('by', char, 'to', state, end = ' ')
                if state not in state_array:
                    state_array.append(state)
            
            print()

            ind += 1

    def build(self, tokens):
        char_set = set()
        for t in tokens:
            self.handlers[t.name](t, self.nfa_stack)
            if t.name == 'CHAR':
                char_set.add(t.value)
        self.alphabet = list(char_set)
        self.nfa_head = self.nfa_stack.pop()

    def create_state(self):
        self.state_count += 1
        return State('s' + str(self.state_count))
    
    def handle_char(self, t, nfa_stack):
        s0 = self.create_state()
        s1 = self.create_state()
        s0.transitions[t.value] = s1
        nfa = NodeGraph(s0, s1)
        self.end_state.add(s1)
        nfa_stack.append(nfa)

        # print(s0.name, '--', t.value, '-->', s1.name)
    
    def handle_concat(self, t, nfa_stack):
        n2 = nfa_stack.pop()
        n1 = nfa_stack.pop()
        n1.end.is_end = False
        if n1.end in self.end_state:
            self.end_state.remove( n1.end)

        # n1.end.epsilon.append(n2.start)
        n1.end.epsilon = n2.start.epsilon # new
        n1.end.transitions = n2.start.transitions 

        nfa = NodeGraph(n1.start, n2.end)
        self.end_state.add(n2.end)
        nfa_stack.append(nfa)

     
    def handle_alt(self, t, nfa_stack):
        n2 = nfa_stack.pop()
        n1 = nfa_stack.pop()
        s0 = self.create_state()
        s0.epsilon = [n1.start, n2.start]
        s3 = self.create_state()
        n1.end.epsilon.append(s3)
        n2.end.epsilon.append(s3)
        n1.end.is_end = False
        n2.end.is_end = False
        if n1.end in self.end_state:
            self.end_state.remove(n1.end)
        if n2.end in self.end_state:
            self.end_state.remove(n2.end)

        nfa = NodeGraph(s0, s3)
        self.end_state.add(s3)

        nfa_stack.append(nfa)
    
    def handle_rep(self, t, nfa_stack):
        n1 = nfa_stack.pop()
        s0 = self.create_state()
        s1 = self.create_state()
        s0.epsilon = [n1.start]
        if t.name == 'STAR':
            s0.epsilon.append(s1)
        n1.end.epsilon.extend([s1, n1.start])
        n1.end.is_end = False
        if n1.end in self.end_state:
            self.end_state.remove(n1.end)

        nfa = NodeGraph(s0, s1)
        self.end_state.add(s1)
        nfa_stack.append(nfa)

    def handle_qmark(self, t, nfa_stack):
        n1 = nfa_stack.pop()
        n1.start.epsilon.append(n1.end)
        nfa_stack.append(n1)


    def addstate(self, state, state_set): 
        if state in state_set:
            return
        state_set.add(state)
        for eps in state.epsilon:
            self.addstate(eps, state_set)

    def match(self,s):
        if not self.nfa_head:
            print('Build before please')
            return
        
        current_states = set()
        self.addstate(self.nfa_head.start, current_states)
        
        for c in s:
            next_states = set()
            for state in current_states:
                if c in state.transitions.keys():
                    trans_state = state.transitions[c]
                    self.addstate(trans_state, next_states)
           
            current_states = next_states

        for s in current_states:
            if s.is_end:
                return True
        return False


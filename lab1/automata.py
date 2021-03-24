
class State:
    def __init__(self, name):
        self.epsilon = [] 
        self.transitions = {} 
        self.name = name
        self.is_end = False
        self.is_start = False

    def __str__(self):
        return self.name 

class NodeGraph:
    def __init__(self, start, end):
        self.start = start
        self.end = end 
        end.is_end = True   

# http://neerc.ifmo.ru/wiki/index.php?title=Построение_по_НКА_эквивалентного_ДКА,_алгоритм_Томпсона
# http://neerc.ifmo.ru/wiki/index.php?title=Минимизация_ДКА,_алгоритм_Хопкрофта_(сложность_O(n_log_n))
class DFA:
    def __init__(self):
        self.start = None
        self.end = None 
        self.alphabet = []
        self.start_state = set()

    def print_graph(self):
        current_states = self.start_state
        used_states = set()
        while current_states != set():
            next_states = set()
            for state in current_states:
                used_states.add(state)
                print(state, end = '-> ')
                for key, value in state.transitions.items():
                    print(key, end = ': ')
                    print(value, end = ' ')
                    if value not in used_states:
                        next_states.add(value)
                print()
            current_states = next_states

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
                self.start_state.add(res_state_array[i])

    def _get_inv(self):
        inv = {}

        current_states = self.start_state
        used_states = set()
        while current_states != set():
            next_states = set()
            for state in current_states:
                used_states.add(state)
                for c in state.transitions.keys():
                    trans_state = state.transitions[c]
                    
                    if trans_state not in inv:
                        inv[trans_state] = {char: [] for char in self.alphabet}
                    inv[trans_state][c].append(state)
                    if trans_state not in used_states:
                        next_states.add(trans_state)
            current_states = next_states

        return inv, list(used_states)

    def minimization(self):
        if not self.start_state:
            print('Build before please')
            return

        inv, used_states = self._get_inv()

        f = set(); not_f = set()
        for state in used_states:
            if state.is_end:
                f.add(state)
            else:
                not_f.add(state)
        p = [f, not_f]
        queue = []
        class_ = {}
        for i in range(len(p)):
            for char in self.alphabet:
                queue.append([i, char])
            for state in p[i]:
                class_[state] = i
        while len(queue) > 0:
            c, a = queue.pop()
            involved = {}
            for q in p[c]:
                if q not in inv:
                    continue
                for r in inv[q][a]:
                    i = class_[r]
                    if i not in involved:
                        involved[i] = set()
                    involved[i].add(r)
            
            for i in involved:
                if len(list(involved[i])) < len(list(p[i])):
                    p.append(set())
                    j = len(p) - 1
                    for r in involved[i]:
                        p[i].remove(r)
                        p[j].add(r)
                    if len(list(p[j])) > len(list(p[i])):
                        p[j], p[i] = p[i], p[j]

                    for r in p[j]:
                        class_[r] = j

                    for char in self.alphabet:
                        queue.append([j, char])
    
        for i in range(len(p)):
            similar_state_arr = list(p[i])
            if len(similar_state_arr) <= 1:
                continue

            keep_state = similar_state_arr[0]
            for q in similar_state_arr:
                if q.is_start and q.is_end:
                    keep_state = q
                    break

                if q.is_start or q.is_end:
                    keep_state = q    

            for q in similar_state_arr:
                if q == keep_state:
                    continue            
                for char in inv[q]:
                    for st in inv[q][char]:
                        st.transitions[char] = keep_state
 

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

# https://en.wikipedia.org/wiki/Thompson%27s_construction
class NFA:
    def __init__(self):
        self.alphabet = []
        self.nfa_stack = []
        self.state_count = 0
        
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
            if t.name == 'CHAR':
                self.handle_char(t, self.nfa_stack)
                char_set.add(t.value)
            elif t.name == 'CONCAT':
                self.handle_concat(t, self.nfa_stack)
            elif t.name == 'OR':
                self.handle_or(t, self.nfa_stack)
            elif t.name == 'STAR':
                self.handle_star(t, self.nfa_stack)
                            
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

      
    def handle_concat(self, t, nfa_stack):
        n2 = nfa_stack.pop()
        n1 = nfa_stack.pop()
        n1.end.is_end = False
        if n1.end in self.end_state:
            self.end_state.remove( n1.end)

        n1.end.epsilon = n2.start.epsilon # new
        n1.end.transitions = n2.start.transitions 

        nfa = NodeGraph(n1.start, n2.end)
        self.end_state.add(n2.end)
        nfa_stack.append(nfa)

     
    def handle_or(self, t, nfa_stack):
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
    
    def handle_star(self, t, nfa_stack):
        n1 = nfa_stack.pop()
        s0 = self.create_state()
        s1 = self.create_state()
        s0.epsilon = [n1.start]
        s0.epsilon.append(s1)
        n1.end.epsilon.extend([s1, n1.start])
        n1.end.is_end = False
        if n1.end in self.end_state:
            self.end_state.remove(n1.end)

        nfa = NodeGraph(s0, s1)
        self.end_state.add(s1)
        nfa_stack.append(nfa)


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


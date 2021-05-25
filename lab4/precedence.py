from exception import CompileError
import copy
from terminaltables import AsciiTable


class Precedence:
    def __init__(self):
        self.L = {}
        self.R = {}
        self.Lt = {}
        self.Rt = {}
        self.b_e_symbol = '$'


    def _getRL(self, grammatic):
        for key, vals in grammatic['rules'].items():
            self.L[key] = set()
            self.R[key] = set()
            for val in vals:
                if val[0] != 'eps':
                    self.L[key].add(val[0])
                if val[-1] != 'eps':
                    self.R[key].add(val[-1])
        
        for _set in [self.L, self.R]:
            change = True
            while change:
                change = False
                for key in _set:
                    original = _set[key]
                    new = _set[key].copy()
                    for left in _set[key]:
                        if left in _set and left != key:
                            new |= _set[left]

                    if original != new:
                        change = True
                        _set[key] = new

    def _getRtLt(self, grammatic):
        for key, vals in grammatic['rules'].items():
            self.Lt[key] = set()
            self.Rt[key] = set()
            for val in vals:
                treminals = []
                for symbol in val:
                    if symbol in grammatic['terminal']:
                        treminals.append(symbol)
                if len(treminals) > 0:
                    self.Lt[key].add(treminals[0])
                    self.Rt[key].add(treminals[-1])

        _set_arr = [self.L, self.R]
        _sett_arr = [self.Lt, self.Rt]
        for j in range(len(_set_arr)):
            _set = _set_arr[j]
            _sett = _sett_arr[j]
            change = True
            while change:
                change = False
                for key in _sett:
                    original = _sett[key]
                    new = _sett[key].copy()
                    for left in _set[key]:
                        if left in _set and left != key:
                            new |= _sett[left]

                    if original != new:
                        change = True
                        _sett[key] = new


    def printMatrix(self):
        matrix = [[] for i in range(len(self.terminal) + 1)]

        matrix[0].append('')
        for t in self.terminal:
            matrix[0].append(t)
        for i, t1 in enumerate(self.terminal):
            matrix[i + 1].append(t1)
            for t2 in self.terminal:
                matrix[i + 1].append(self.matrix[t1][t2])

        table = AsciiTable(matrix)
        print(table.table)


    def buildOperatorPrecedenceMatrix(self, grammatic):
        self._getRL(grammatic)
        self._getRtLt(grammatic)
        

        self.matrix = {}
        self.terminal = grammatic['terminal']
        self.terminal.append(self.b_e_symbol)

        for t1 in grammatic['terminal']:
            self.matrix[t1] = {}
            for t2 in grammatic['terminal']:
                self.matrix[t1][t2] = ' '
        
        for key, vals in grammatic['rules'].items():
            for val in vals:
                for i in range(len(val)):
                    symbol = val[i]
                    if symbol in grammatic['terminal']:
                        if i < len(val) - 1 and val[i + 1] in grammatic['nonterminal']:
                            for l in self.Lt[val[i + 1]]:
                                self.matrix[symbol][l] = '<'
                        
                        if i < len(val) - 1 and val[i + 1] in grammatic['terminal']:
                            self.matrix[symbol][val[i + 1]] = '='
                        elif i < len(val) - 2 and val[i + 2] in grammatic['terminal']:
                            self.matrix[symbol][val[i + 2]] = '='

                        if i != 0 and val[i - 1] in grammatic['nonterminal']:
                            for r in self.Rt[val[i - 1]]:
                                if self.matrix[r][symbol] == ' ':
                                    self.matrix[r][symbol] = '>'

            for symbol in self.Lt[grammatic['startsymbol']]:
                self.matrix[self.b_e_symbol][symbol] = '<'

            for symbol in self.Rt[grammatic['startsymbol']]:
                self.matrix[symbol][self.b_e_symbol] = '>'
                        

    def _get_grammatic_with_E(self, grammatic):
        E_grammatic = copy.deepcopy(grammatic['rules'])
        for key in E_grammatic:
            for i in range(len(E_grammatic[key])):
                for j in range(len(E_grammatic[key][i])):
                    symbol = E_grammatic[key][i][j]
                    if symbol in grammatic['nonterminal']:
                        E_grammatic[key][i][j] = 'E'
        return E_grammatic

    def _first_terminal(self, stack, grammatic):
        i = len(stack) - 1
        terminal_symbol = None
        while i >= 0:
            if stack[i] in grammatic['terminal'] or stack[i] == self.b_e_symbol:
                terminal_symbol = stack[i]
                break
            i -= 1
        return terminal_symbol

    def _first_rule(self, stack, stack_real_names, grammatic):
        i = len(stack) - 1
        terminal_symbols = []
        terminal_symbol = None
        rule = []
        
        while len(stack) > 0:
            if stack[-1] == self.b_e_symbol:
                break
            if stack[-1] in grammatic['terminal']:
                if terminal_symbol is None:
                    terminal_symbol = stack[-1]
                    terminal_symbols.append(stack_real_names[-1])
                else:
                    if self.matrix[stack[-1]][terminal_symbol] != '=':
                        break
                    else:
                        terminal_symbol = stack[-1]
                        terminal_symbols.append(stack_real_names[-1])
            rule.append(stack.pop())
            stack_real_names.pop()
            
        rule.reverse()
        return rule, terminal_symbols
            
    def _find_rule_in_grammatic(self, rule, E_rules):
        find_flag = False
        found_rule = None
        for key, vals in E_rules.items():
            for i, v in enumerate(vals):
                if v == rule:
                    find_flag = True
                    found_rule = [key, i]
                    break
            if find_flag:
                break
        return find_flag, found_rule

    def checkCode(self, grammatic, tokens):
        E_rules = self._get_grammatic_with_E(grammatic)
        
        i = 0
        tokens = tokens + [{'type':'end', 'value': self.b_e_symbol}]
        all_terminal_symbols = []
        all_rules = []
        stack = [self.b_e_symbol]
        stack_real_names = []
        while stack != [self.b_e_symbol, 'E'] or i < len(tokens) - 1:
            token = tokens[i]
            token_value = token['value']
            if token['type'] == 'NAME':
                token_value = 'identificator'
            elif token['type'] == 'NUMBER':
                token_value = 'constant'

            first_terminal = self._first_terminal(stack, grammatic)

            sign = self.matrix[first_terminal][token_value]
            if sign == '<' or sign == '=':
                stack.append(token_value)
                stack_real_names.append(token['value'])
                if i < len(tokens) - 1:
                    i += 1
            elif sign == '>':
                rule, terminal_symbols = self._first_rule(stack, stack_real_names, grammatic)
                all_terminal_symbols.extend(terminal_symbols)
                found_flag, found_rule = self._find_rule_in_grammatic(rule, E_rules)
                if found_flag:
                    all_rules.append(found_rule)
                    stack.append('E')
                    stack_real_names.append('E')
                else:
                    raise CompileError('Rule' + str(rule) + 'not found')
            else:
                raise CompileError('No precedence value set for ' + str(first_terminal) + ' ' + str(token_value))
        
        used_rules = []
        for i in range(len(all_rules)):
            key, ind = all_rules[i]
            used_rules.append([key, grammatic['rules'][key][ind]])
        return all_terminal_symbols, used_rules
        
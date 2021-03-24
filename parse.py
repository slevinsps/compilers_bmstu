class Symbol:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return self.name + ":" + self.value

class ParseError(Exception):pass

class Parser:
    def __init__(self):
        self.symbols = []
        self.orig_symbols = []
        self.orig_symbols_index = 0
        self.symbols_dict = {'(':'LP', ')':'RP', '*':'STAR', '|':'OR', 'CONCAT':'CONCAT'}

    def create_symbols(self, pattern):
        for c in pattern:
            if c not in self.symbols_dict.keys(): # CHAR
                token = Symbol('CHAR', c)
            else:
                token = Symbol(self.symbols_dict[c], c)
            self.orig_symbols.append(token)

        self.lookahead = self.orig_symbols[self.orig_symbols_index]
        self.orig_symbols_index += 1
        
        
    def parse(self, pattern):
        if pattern is None or len(pattern) == 0:
            return []

        self.create_symbols(pattern)
        self.handle_symbols()
        return self.symbols
    
    def handle_symbols(self):
        self.handle_concat()
        if self.lookahead.name == 'OR':
            t = self.lookahead
            self.check_and_next('OR')
            self.handle_symbols()
            self.symbols.append(t)

    def handle_concat(self):
        self.handle_star()
        if self.lookahead.value not in ')|':
            self.handle_concat()
            self.symbols.append(Symbol('CONCAT', 'CONCAT'))
    
    def handle_star(self):
        self.handle_char()
        if self.lookahead.name == 'STAR':
            self.symbols.append(self.lookahead)
            self.check_and_next(self.lookahead.name)

    def handle_char(self):
        if self.lookahead.name == 'LP':
            self.check_and_next('LP')
            self.handle_symbols()
            self.check_and_next('RP')
        elif self.lookahead.name == 'CHAR':
            self.symbols.append(self.lookahead)
            self.check_and_next('CHAR')

    def check_and_next(self, name):
        if self.lookahead.name == name:
            if self.orig_symbols_index >= len(self.orig_symbols):
                self.lookahead = Symbol('NONE', '')
            else:
                self.lookahead = self.orig_symbols[self.orig_symbols_index]
            self.orig_symbols_index += 1

        elif self.lookahead.name != name:
            raise ParseError

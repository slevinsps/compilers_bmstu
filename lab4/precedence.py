class Precedence:
    def __init__(self):
        self.L = {}
        self.R = {}
        self.Lt = {}
        self.Rt = {}


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
        print('  ', end='')
        for t in self.terminal:
            print(t, end=' ')
        print()
        for t in self.terminal:
            print(t, end=' ')
            for tt in self.terminal:
                print(self.matrix[t][tt], end= ' ')
            print()

    def buildOperatorPrecedenceMatrix(self, grammatic):
        self._getRL(grammatic)
        self._getRtLt(grammatic)
        self.matrix = {}
        self.terminal = grammatic['terminal']
        for t1 in grammatic['terminal']:
            self.matrix[t1] = {}
            for t2 in grammatic['terminal']:
                self.matrix[t1][t2] = ' '
        
        for key, vals in grammatic['rules'].items():
            for val in vals:
                for i in range(len(val)):
                    symbol = val[i]
                    if symbol in grammatic['terminal']:
                        if i != 0 and val[i - 1] in grammatic['nonterminal']:
                            for r in self.Rt[val[i - 1]]:
                                self.matrix[r][symbol] = '<'
                        if i != len(val) - 1 and val[i + 1] in grammatic['nonterminal']:
                            for l in self.Lt[val[i + 1]]:
                                self.matrix[l][symbol] = '>'
        

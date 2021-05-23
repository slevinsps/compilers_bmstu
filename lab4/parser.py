class GrammaticParser():
    def __init__(self):
        pass

    def parse(self, path):
        nonterminal = []
        terminal = []
        startsymbol = None
        rules = {}
        with open(path, 'r') as f:
            nonterminal = f.readline().strip(' ').strip('\n').split(' ')
            terminal = f.readline().strip(' ').strip('\n').split(' ')
            startsymbol = f.readline().strip(' ').strip('\n')
            for line in f:
                all_productions = line.strip(' ').strip('\n').split('|')
                readed_line = all_productions[0].strip(' ').strip('\n').split(' ')
                symbol = readed_line[0]
                if symbol not in rules:
                    rules[symbol] = [readed_line[2:]]
                else:
                    rules[symbol].append(readed_line[2:])

                for production in all_productions[1:]:
                    readed_line = production.strip(' ').strip('\n').split(' ')
                    rules[symbol].append(readed_line)

        grammatic = {'nonterminal': nonterminal,
                     'terminal': terminal,
                     'startsymbol': startsymbol,
                     'rules': rules}


        return grammatic
        
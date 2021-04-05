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
                readed_line = line.strip(' ').strip('\n').split(' ')
                if readed_line[0] not in rules:
                    rules[readed_line[0]] = []

                rules[readed_line[0]].append(readed_line[2:])

        grammatic = {'nonterminal': nonterminal,
                     'terminal': terminal,
                     'startsymbol': startsymbol,
                     'rules': rules}

        print(grammatic)
        return grammatic
        
from parser import GrammaticParser



def elimination_of_recursion_immediate_1(grammatic):
    new_rules = grammatic['rules'].copy()
    new_nonterminal = grammatic['nonterminal'].copy()

    for left, right in grammatic['rules'].items():
        add_index = 1
        alpha = []
        beta = []
        for i in range(len(right)):
            if right[i][0] == left and len(right[i]) > 1:
                alpha.append(right[i][1:])
            else:
                beta.append(right[i])
        
        if len(alpha) > 0:
            new_symbol = left + str(add_index)
            new_nonterminal.add(new_symbol)
            new_rules[left] = []
            new_rules[new_symbol] = []
            for i in range(len(beta)):
                new_rules[left].append(beta[i])
                new_rules[left].append(beta[i] + [new_symbol])
            for i in range(len(alpha)):
                new_rules[new_symbol].append(alpha[i])
                new_rules[new_symbol].append(alpha[i] + [new_symbol])

    grammatic['rules'] = new_rules
    grammatic['nonterminal'] = new_nonterminal

def elimination_of_recursion_immediate_2(rules):
    new_rules = rules.copy()
    new_nonterminal = set()
    epsilon = 'eps'

    for left, right in rules.items():
        add_index = 1
        alpha = []
        beta = []
        for i in range(len(right)):
            if right[i][0] == left and len(right[i]) > 1:
                alpha.append(right[i][1:])
            else:
                beta.append(right[i])

        if len(beta) == 0:
            beta.append([])
        # print('alpha =', alpha)
        # print('beta =', beta)
        if len(alpha) > 0:
            new_symbol = left + str(add_index)
            new_nonterminal.add(new_symbol)
            new_rules[left] = []
            new_rules[new_symbol] = []

            
            for i in range(len(beta)):
                symbol = beta[i]
                if beta[i] == [epsilon]:
                    symbol = []
                new_rules[left].append(symbol + [new_symbol])
            for i in range(len(alpha)):
                new_rules[new_symbol].append(alpha[i] + [new_symbol])
            new_rules[new_symbol].append([epsilon])

    return new_rules, new_nonterminal


def elimination_of_recursion_indirect(grammatic):
    rules = grammatic['rules']
    nonterminal = list(rules.keys())
    new_nonterminal_arr = grammatic['nonterminal'].copy()
    for i in range(len(nonterminal)):
        Ai = nonterminal[i]
        print(Ai)
        for j in range(i):
            ai_production_array = rules[Ai]
            Aj = nonterminal[j]
            aj_production_array = rules[Aj]

            new_production_array = []

            for k in range(len(ai_production_array)):
                new_production = []
                for p in range(len(ai_production_array[k])):
                    if Aj == ai_production_array[k][p]:
                        for aj_production in aj_production_array:
                            new_production_array.append(new_production + aj_production + ai_production_array[k][p + 1:])
                        new_production = []
                        break      
                    else:
                        new_production.append(ai_production_array[k][p])

                if len(new_production) > 0:
                    new_production_array.append(new_production)

            rules[Ai] = new_production_array

        new_rules, new_nonterminal = elimination_of_recursion_immediate_2({Ai: rules[Ai]})
        new_nonterminal_arr += list(new_nonterminal)
        for a in new_rules:
            rules[a] = new_rules[a]

        print('---')
        print(rules)

    grammatic['rules'] = rules
    grammatic['nonterminal'] = new_nonterminal_arr
    return grammatic
                    

def main():
    path = 'gr1.txt'

    grammaticParser = GrammaticParser()
    grammatic = grammaticParser.parse(path)

    # elimination_of_recursion_immediate1(grammatic)
    grammatic = elimination_of_recursion_indirect(grammatic)

    print(grammatic)


if __name__ == '__main__':
    main()
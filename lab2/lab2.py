from parser import GrammaticParser

# Алгоритм 2.13 из книги АХО А., УЛЬМАН Дж. Теория синтаксического анализа, перевода и компиляции: В 2-х томах. Т.1.: Синтаксический анализ. - М.: Мир, 1978.
def elimination_of_recursion_immediate_1(grammatic):
    new_rules = grammatic['rules'].copy()
    new_nonterminal = set(grammatic['nonterminal'])

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
    grammatic['nonterminal'] = list(new_nonterminal)
    return grammatic

# Алгоритм 4.8 из книги АХО А.В, ЛАМ М.С., СЕТИ Р., УЛЬМАН Дж.Д. Компиляторы: принципы, технологии и инструменты. – М.: Вильямс, 2008
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

    grammatic['rules'] = rules
    grammatic['nonterminal'] = new_nonterminal_arr
    return grammatic


# Алгоритм 2.8 АХО А., УЛЬМАН Дж. Теория синтаксического анализа, перевода и компиляции: В 2-х томах. Т.1.: Синтаксический анализ. - М.: Мир, 1978.
def remove_unattainable_symbols(grammatic):
    nonterminal = set(grammatic['nonterminal'])
    V_pred = set()
    V_next = set([grammatic['startsymbol']])
    while V_next != V_pred:
        V_pred, V_next = V_next, V_pred
        for symbol, production in grammatic['rules'].items():
            if symbol in V_pred:
                for p in production:
                    for i in range(len(p)):
                        if p[i] in nonterminal:
                            V_next.add(p[i])
        V_next |= V_pred
    
    new_grammatic = {}
    new_grammatic['nonterminal'] = list(nonterminal.intersection(V_next))
    new_grammatic['startsymbol'] = grammatic['startsymbol']
    terminal = set()
    rules = {}
    for symbol, production in grammatic['rules'].items():
        if symbol in V_next:
            rules[symbol] = production
            for p in production:
                for i in range(len(p)):
                    if p[i] not in nonterminal and p[i] != 'eps':
                        terminal.add(p[i])

    
    new_grammatic['terminal'] = list(terminal)
    new_grammatic['rules'] = rules
    return new_grammatic

def get_longest_prefix(production):
    production_string_array = []
    for p in production:
        s = ''
        for i in range(len(p)):
            s += p[i]
        production_string_array.append(s)
    production_string_array.sort()
    print(production_string_array)
    
    max_prefix = ''
    for i in range(len(production_string_array) - 1):
        p1 = production_string_array[i]
        p2 = production_string_array[i + 1]
        prefix = ''

        for j in range(min(len(p1), len(p2))):
            if p1[j] == p2[j]:
                prefix += p1[j]
            else:
                if len(prefix) > len(max_prefix):
                    max_prefix = prefix
                prefix = ''
                break
        if len(prefix) > len(max_prefix):
            max_prefix = prefix

    max_prefix_arr = []
    for i in range(len(max_prefix)):
        max_prefix_arr.append(max_prefix[i])

    return max_prefix_arr
    
def left_factorization(grammatic):
    rules = {}
    for symbol, production in grammatic['rules'].items():
        prefix = get_longest_prefix(production)
        if len(prefix) == 0:
            continue
        
        beta_arr = []
        gamma_arr = []

        for p in production:
            if prefix == p[:len(prefix)]:
                beta_arr.append(p[len(prefix):])
            else:
                gamma_arr.append(p)
        
        print(beta_arr, gamma_arr)
        new_symbol = symbol + '1'
        # rules[symbol] = 

def main():
    path = 'gr6.txt'

    grammaticParser = GrammaticParser()
    grammatic = grammaticParser.parse(path)

    ## elimination_of_recursion_immediate1(grammatic)
    # grammatic = elimination_of_recursion_indirect(grammatic)
    # grammatic = remove_unattainable_symbols(grammatic)
    # print(grammatic)
    left_factorization(grammatic)


if __name__ == '__main__':
    main()
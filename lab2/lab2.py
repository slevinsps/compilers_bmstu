from parser import GrammaticParser
import argparse


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
            if len(beta) == 0:
                new_rules[left] = [[new_symbol]]

            for i in range(len(beta)):
                if beta[i][-1] == 'eps':
                    new_rules[left].append([new_symbol])
                    new_rules[left].append(beta[i])
                else:
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
    # print('rules = ', rules)
    new_rules = rules.copy()
    new_nonterminal = set()
    epsilon = 'eps'

    for left, right in rules.items():
        add_index = 1
        alpha = []
        beta = []
        for i in range(len(right)):
            if right[i][0] == left and len(right[i]) >= 1:
                alpha.append(right[i][1:])
            else:
                beta.append(right[i])

        # print('alpha = ', alpha, 'beta = ', beta)
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
    # print(nonterminal)
    for i in range(len(nonterminal)):
        Ai = nonterminal[i]
        for j in range(i):
            ai_production_array = rules[Ai]
            Aj = nonterminal[j]
            aj_production_array = rules[Aj]

            new_production_array = []

            for k in range(len(ai_production_array)):
                new_production = []
                if ai_production_array[k][0] == Aj:
                    for aj_production in aj_production_array:
                            if aj_production[-1] == 'eps':
                                aj_production = aj_production[:-1]
                            new_production_array.append(aj_production + ai_production_array[k][1:])
                else:
                    new_production.extend(ai_production_array[k])

                if len(new_production) > 0:
                    new_production_array.append(new_production)
            rules[Ai] = new_production_array
        # print('AAA')
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
            s += p[i] + '|'
        production_string_array.append(s)
    production_string_array.sort()
    
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

    max_prefix_arr = max_prefix.split('|')[:-1]

    return max_prefix_arr
    
# Алгоритм 4.10 из книги АХО А.В, ЛАМ М.С., СЕТИ Р., УЛЬМАН Дж.Д. Компиляторы: принципы, технологии и инструменты. – М.: Вильямс, 2008
def left_factorization(grammatic):
    rules = {}
    symbol_epsilon_dict = {}

    for symbol, production in grammatic['rules'].items():
        symbol_epsilon_dict[symbol] = False

        prefix = get_longest_prefix(production)
        if len(prefix) == 0:
            continue
        
        new_symbol = symbol

        while len(prefix) > 0:
            new_symbol += '1'
            
            beta_arr = []
            gamma_arr = []

            for p in production:
                if prefix == p[:len(prefix)]:
                    beta = p[len(prefix):]
                    if len(beta) > 0:
                        beta_arr.append(beta)
                    else:
                        symbol_epsilon_dict[new_symbol] = True
                else:
                    gamma_arr.append(p)
            
            grammatic['nonterminal'].append(new_symbol)

            rules[symbol] = [prefix + [new_symbol]] + gamma_arr
            rules[new_symbol] = beta_arr

            production = rules[symbol]
            prefix = get_longest_prefix(production)

    for symbol in rules:
        grammatic['rules'][symbol] = rules[symbol]
        if symbol in symbol_epsilon_dict and symbol_epsilon_dict[symbol]:
            grammatic['rules'][symbol].append(['eps'])
    return grammatic


def print_grammatic(grammatic):
    print('non terminal:', end = ' ')
    for i in range(len(grammatic['nonterminal'])):
        print(grammatic['nonterminal'][i], end = ' ')
    print()
    print('terminal:', end = ' ')
    for i in range(len(grammatic['terminal'])):
        print(grammatic['terminal'][i], end = ' ')
    print()
    print('start symbol:', end = ' ')
    print(grammatic['startsymbol'])
    for symbol, production in grammatic['rules'].items():
        print(symbol, '->', end = ' ') 
        for i in range(len(production)):
            for pi in production[i]:
                print(pi, end = ' ') 
            if i < len(production) - 1:
                print('|', end = ' ')
        print()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", help="path to grammatic txt file", required=True)
    args = parser.parse_args()
    path = args.path

    grammaticParser = GrammaticParser()
    grammatic = grammaticParser.parse(path)

    print('Input grammatic:')
    print_grammatic(grammatic)
    print('----------------')

    # grammatic = elimination_of_recursion_immediate_1(grammatic)
    grammatic = elimination_of_recursion_indirect(grammatic)
    # grammatic = remove_unattainable_symbols(grammatic)
    # grammatic = left_factorization(grammatic)
    print('Output grammatic:')
    print_grammatic(grammatic)

if __name__ == '__main__':
    main()

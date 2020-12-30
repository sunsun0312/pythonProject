# EDIT THE FILE WITH SOLUTION
from collections import defaultdict
from itertools import product

file = input('Which text file do you want to use for the puzzle? ')

# read file and split them by using space
with open(file) as s:
    s_read = s.read()
    if s_read.find('""', None):
        s_read = s_read.replace('""', '" "')
    if s_read.find(':"', None):
        s_read = s_read.replace(':"', ': "')
    test_list = s_read.split()


# change the order of the punctuator which contains double quote marks
# record the index of each question mark, exclaimation mark and full stop
# add every full sentence into another list
def split_sentence(test_list):
    sentence = []
    index_of_punctuator = []
    for i in range(len(test_list)):
        if test_list[i].endswith(','):
            test_list[i] = test_list[i][:-1]
        if test_list[i].endswith('"'):
            if not test_list[i][-2:-1].isalpha():
                test_list[i] = test_list[i].replace(test_list[i][-2:], test_list[i][:-3:-1])

        if test_list[i].endswith('.') or test_list[i].endswith('!') or test_list[i].endswith('?'):
            index_of_punctuator.append(i)
            test_list[i] = test_list[i][:-1]

    if index_of_punctuator:
        sentence.append([test_list[i] for i in range(index_of_punctuator[0] + 1)])
        for j in range(len(index_of_punctuator) - 1):  # 0, 1, 2
            sentence.append([test_list[k] for k in range(index_of_punctuator[j] + 1,\
                                                         index_of_punctuator[j + 1] + 1)])
    return sentence


# drop commas after double question mards
# find Sir in every sentence, and add the word after Sir into the sir_name set
# find Sirs and and index, extract the middle part and add to the sir_name set
# find the contents between two double question marks in every sentence
# find Sir outside these two double question marks
# build a dictionary quote to record the name as key, the sentence as value

def find_names(sentence):
    sir_name = set()
    quote = defaultdict(list)
    for i in range(len(sentence)):
        sentence_index = []
        Sirs_index = []
        for j in range(len(sentence[i])):

            if sentence[i][j].endswith(','):
                sentence[i][j] = sentence[i][j][:-1]

            if 'Sirs' in sentence[i][j]:
                Sirs_index.append(j)
            elif 'Sir' in sentence[i][j]:
                sir_name = sir_name.union([sentence[i][j + 1]])

            if sentence[i][j].startswith('"'):
                sentence_index.append(j)
                sentence[i][j] = sentence[i][j][1:]
            elif sentence[i][j].endswith('"'):
                sentence_index.append(j)
                sentence[i][j] = sentence[i][j][:-1]
        if sentence_index:
            without_quote = sentence[i][:sentence_index[0]] + sentence[i][sentence_index[1] + 1:]
            quote[without_quote[without_quote.index('Sir') + 1]].append([sentence[i][j] \
                                                                         for j in range(sentence_index[0], 
                                                                                        sentence_index[1] + 1)])

        if Sirs_index:
            for k in range(Sirs_index[0] + 1, len(sentence[i])):
                if sentence[i][k] == 'and':
                    sir_name = sir_name.union([sentence[i][m] for m in range(Sirs_index[0] + 1, k)])
                    sir_name = sir_name.union([sentence[i][k + 1]])
    sir_name = list(sir_name)
    return sorted(sir_name), quote


# analyze different sentence and classify them into different situation
# replace I with the exact name of these person

sir_name, quote = find_names(split_sentence(test_list))

situation = {'A': ' least ', 'B': ' most ', 'C': 'exactly one of ', 'D': 'all of ', 'E': ' and ', 'F': ' or ', 'G': ' is ', 'H': ' am '}
try:
    saying_names = defaultdict(list)
    for key, value in quote.items():
        for line in range(len(value)):
            if value[line][0].istitle:
                if value[line][0] == 'Exactly' or value[line][0] == 'All':
                    quote[key][line][0] = value[line][0].lower()
            value[line] = ' ' + ' '.join(value[line][i] for i in range(len(value[line])))
            if ' I ' in value[line]:
                value[line] = value[line].replace(' I ', f' {key} ')

            if 'Knight' in value[line] or 'Knights' in value[line]:
                for i, j in situation.items():
                    if j in value[line]:
                        saying_names[key, i + '1'].append(value[line])
                        break
            elif 'Knave' in value[line] or 'Knaves' in value[line]:
                for i, j in situation.items():
                    if j in value[line]:
                        saying_names[key, i + '2'].append(value[line])
                        break
    # build a new dictionary to record which person are refered to in a sentence, and who talk about these names

    saying_names_1 = defaultdict(list)
    for key, value in saying_names.items():
        for k in range(len(value)):
            a = [None] * len(sir_name)
            if ' us ' in value[k]:
                a = [1] * len(sir_name)
            else:
                for i in range(len(sir_name)):
                    if sir_name[i] not in value[k]:
                        continue
                    else:
                        a[i] = 1
            saying_names_1[key].append(a)

    # list probabilities of every situation, and verify wheather it is matched between the sentence and the person
    # if it is not matched, replace True with False
    # calculate how many True in this dictionary, that is, which situations can be solutions

    truth_table = list(product((0, 1), repeat=len(sir_name)))
    truth_table = dict.fromkeys(truth_table, True)

    for i in truth_table:
        for key, value in saying_names_1.items():
            name, situ = key
            for k in range(len(value)):
                a = 0
                num = 0
                for j in range(len(value[k])):
                    if value[k][j]:
                        a += i[j]
                        num += 1
                if situ in {'D2', 'E2', 'H2', 'G2'}:
                    if i[sir_name.index(name)] != (a == 0):
                        if truth_table[i]:
                            truth_table[i] = False
                        break

                if situ in {'C1', 'H1', 'G1'}:
                    if i[sir_name.index(name)] != (a == 1):
                        if truth_table[i]:
                            truth_table[i] = False
                        break

                if situ in {'A1', 'F1'}:
                    if i[sir_name.index(name)] != (a >= 1):
                        if truth_table[i]:
                            truth_table[i] = False
                        break
                if situ in {'A2', 'F2'}:
                    if i[sir_name.index(name)] != (a < num):
                        if truth_table[i]:
                            truth_table[i] = False
                        break
                if situ in {'D1', 'E1'}:
                    if i[sir_name.index(name)] != (a == num):
                        if truth_table[i]:
                            truth_table[i] = False
                        break

                if situ in {'D1', 'E1'}:
                    if i[sir_name.index(name)] != (a == num):
                        if truth_table[i]:
                            truth_table[i] = False
                        break

                if situ in {'B1'}:
                    if i[sir_name.index(name)] != (a <= 1):
                        if truth_table[i]:
                            truth_table[i] = False
                        break

                if situ in {'B2'}:
                    if i[sir_name.index(name)] != (a >= num - 1):
                        if truth_table[i]:
                            truth_table[i] = False
                        break

                if situ in {'C2'}:
                    if i[sir_name.index(name)] != (a == num - 1):
                        if truth_table[i]:
                            truth_table[i] = False
                        break

    result = []
    for i in truth_table:
        if truth_table[i]:
            result.append(i)

except Exception:
    result = []

print(f'The Sirs are:', ' '.join(f'{i}'
                                 for i in sir_name))
Knight_Knave = {1: 'Knight', 0: 'Knave'}
if len(result) == 0:
    print('There is no solution.')
elif len(result) == 1:
    print(f'There is a unique solution:')
    print('\n'.join(f'Sir {sir_name[i]} is a {Knight_Knave[result[0][i]]}.' for i in range(len(sir_name))))
elif len(result) > 1:
    print(f'There are {len(result)} solutions.')
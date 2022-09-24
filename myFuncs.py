import re

def add(cur_list, champ):
    cur_list.append(champ)

def open_file():
    list_of_lists = [[], [], [], [], []]
    x = 0
    with open('champ_list.txt') as f:
        for line in f:
            line = re.sub("[\(\[].*?[\)\]]", "", line)
            line = line.strip()
            if (line == ""):
                continue
            if (line == "1_cost"):
                x = 0
                continue
            if (line == "2_cost"):
                x = 1
                continue
            if (line == "3_cost"):
                x = 2
                continue
            if (line == "4_cost"):
                x = 3
                continue
            if (line == "5_cost"):
                x = 4
                continue

            list_of_lists[x].append(line)
    return list_of_lists


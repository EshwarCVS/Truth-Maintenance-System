import re

def add(stackLiteral, original, pattern):
    rule = ""
    while stackLiteral:
        item = stackLiteral.pop()
        if item == '+':
            if rules.get(rule):
                rules[rule].append([pattern, original, False])
            else:
                rules[rule] = [[pattern, original, False]]
            rule = ""
        else:
            if item == '*':
                item = ','
            rule = item + rule
    if rules.get(rule):
        rules[rule].append([pattern, original, False])
    else:
        rules[rule] = [[pattern, original, False]]

def assess():
    if not rules:
        return
    rules_shallow = rules.copy()
    for key in rules_shallow.keys():
        found = True
        for k in key.split(','):
            if not TMS.get(k):
                found = False
        if found:
            r_list = rules[key].copy()
            for rule_list in r_list:
                if not rule_list[2]:
                    rule_list[2] = True
                    str = '{' + key + ',' + rule_list[1] + '}'
                    if TMS.get(rule_list[0]):
                        TMS[rule_list[0]].append(str)
                    else:
                        TMS[rule_list[0]] = [str]
                    status.append(rule_list[0]+':'+str)
    if rules_shallow != rules:
        assess()

def delete_lit(literal):
    delete = []
    for key in rules.keys():
        for k in key.split(','):
            if k == literal:
                r_list = rules[key].copy()
                for rule_list in r_list:
                    if rule_list[2]:
                        rule_list[2] = False
                        str = '{' + key + ',' + rule_list[1] + '}'
                        if TMS.get(rule_list[0]):
                            TMS[rule_list[0]].remove(str)
                            delete.append(rule_list[0])
                            if not TMS[rule_list[0]]:
                                TMS.pop(rule_list[0])
                        status.remove(rule_list[0] + ':' + str)
    while delete:
        delete_lit(delete.pop(0))

def delete_rule(rule, literal):
    status.remove(rule)

    rules_shallow = rules.copy()
    for r in rules_shallow:
        l_copy = rules[r].copy()
        for l in l_copy:
            if l[1] == rule:
                rules[r].remove(l)
    rules_shallow = rules.copy()
    for r in rules_shallow:
        if not rules_shallow[r]:
            rules.pop(r)

    def delete_recursive(r,literal):
        to_delete = literal
        delete_rule = ',' + r + '}'
        status_copy = status.copy()
        for i in status_copy:
            if delete_rule in i:
                status.remove(i)
        TMS_list = TMS[to_delete].copy()
        for i in TMS_list:
            if delete_rule in i:
                TMS[to_delete].remove(i)
        if not TMS[to_delete]:
            TMS.pop(to_delete)
            if rules.get(to_delete):
                for i in rules[to_delete]:
                    if i[2]:
                        i[2] = False
                        delete_recursive(i[1],i[0])

    delete_recursive(rule,literal)

input_file = open("TMSInput.txt", 'r').read().split('\n')

status = []
TMS = {}
rules = {}
stack = []

for line in input_file:
    if line.startswith('T'):
        # Tell
        pattern = re.search(r'Tell:\s(([\w]*[\s]*[+*-]*\w)\s->\s(-*\w))', line)
        if pattern:
            status.append(pattern.group(1))
            for i in pattern.group(2):
                stack.append(i)
            add(stack, pattern.group(1), pattern.group(3))
            assess()
            assess()
            continue

        pattern = re.search(r'Tell:\s(-*\s*\w)', line)
        if pattern:
            str = pattern.group(1)
            if TMS.get(str):
                flag = False
                for i in TMS.get(str):
                    if i == str:
                        flag = True
                        break
                if flag == True:
                    continue
                status.append(str)
                TMS[str].append(str)
                assess()
                assess()
                continue
            status.append(str)
            TMS[str] = [str]
            assess()
            assess()
            continue

    elif line.startswith('R'):
        # Retract
        pattern = re.search(r'Retract:\s(([\w]*[\s]*[+*-]*\w)\s->\s(-*\w))', line)
        if pattern:
            if pattern.group(1) in status:
                delete(pattern.group(1),pattern.group(3))
            continue

        pattern = re.search(r'Retract:\s(-*\s*\w)', line)
        if pattern:
            str = pattern.group(1)
            if str in status:
                if TMS.get(str):
                    for i in TMS.get(str):
                        if i == str:
                            TMS[str].remove(i)
                            break
                    delete_lit(str)
                    status.remove(str)
                    if not TMS[str]:
                        TMS.pop(str)
                    continue
            continue

print("Final Status:")
for action in status:
    print(action)
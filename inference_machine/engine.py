import os


def clear():
    if os.name in ('nt', 'dos'):
        os.system("cls")
    elif os.name in ('linux', 'osx', 'posix'):
        os.system("clear")
    else:
        print("\n" * 120)
    # os.system('cls' if os.name == 'nt' else 'clear')


def remove_negative(q):
    negative = False
    if '!' in q:
        parts = q.split('!')
        q = parts[len(parts) - 1]
        negative = (len(parts) - 1) % 2 != 0
    return q, negative


def rules_navigator(knowledge_base, rules, question):
    question, negative = remove_negative(question)

    if question in knowledge_base:
        return True
    if question not in rules:
        return False

    flag = False
    new_rules = rules.copy()
    for conditions in rules[question]:
        new_rules[question].remove(conditions)
        if len(new_rules[question]) == 0:
            new_rules.pop(question)
        for condition in conditions:
            if not rules_navigator(knowledge_base, new_rules, condition):
                flag = True
                break
            c, n = remove_negative(condition)
            if knowledge_base[c] and n or not knowledge_base[c] and not n:
                flag = True
                break
        if flag:
            continue

        knowledge_base[question] = not negative
        return True
    return False

def verf(q, knowledge_base):

    if q[0] == '!':
        if q in knowledge_base:
            return knowledge_base[q]
        elif q[1] in knowledge_base:
            return not knowledge_base[q[1]]
    if q in knowledge_base:
        return knowledge_base[q]
    return None



def forward_chaining(knowledge_base, rules, question):
    elements = []

    for x in rules.keys():
        elements.append(x)

    while elements:
        x = elements.pop(0)
        for i in rules[x]:
            result = True
            for k in i:
                k = verf(k, knowledge_base)
                if k is None:
                    break
                result = result and k
            else:
                knowledge_base[x] = result
                break
            elements.append(x)
    return knowledge_base[question]


def backward_chaining(knowledge_base, rules, question):
    q, negative = remove_negative(question)
    if q in knowledge_base:
        return str(q) + " is " + str(knowledge_base[q])

    if question not in rules and q not in rules:
        return "There isn't a rule that generates the answer, sorry!"

    if rules_navigator(knowledge_base, rules, question):
        return str(q) + " is " + str(knowledge_base[q])

    return "There isn't sufficient conditions to answer the question "


def main():
    print("obs.:For negatives use '!' like !B\n")
    knowledge_base = {}
    rules = {}

    while True:
        print("Enter the knowledge base:")
        while True:
            a = input("The element: ")
            b = input("The value: ")
            knowledge_base[a] = b[0] == "T"
            choice = int(input("Any more element? 1-Yes 2-No"))
            if choice == 2:
                break

        print("Enter the production rules:")
        while True:
            consequence = input("The consequence:")
            if consequence not in rules:
                rules[consequence] = []
            print("Insert the clause conditions separate by enters: \n    -1 to stop")
            clause_conditions = []
            while True:
                clause = input()
                if clause == "-1":
                    break
                clause_conditions.append(clause)
            rules[consequence].append(clause_conditions)
            choice = int(input("Any more rule? 1-Yes 2-No"))
            if choice == 2:
                break

        clear()
        print("knowledge base:")
        print(knowledge_base)
        print("\n")
        print("What is the question?")
        question = input()
        print("What kind of method do you want?")
        print("1- Forward chaining")
        print("2- Backward  chaining")
        print("3- Hybrid")
        choice = int(input())
        if choice == 1:
            print(forward_chaining(knowledge_base, rules, question))
            print("knowledge base:")
            print(knowledge_base)
        elif choice == 2:
            print(backward_chaining(knowledge_base, rules, question))
            print("knowledge base:")
            print(knowledge_base)
        elif choice == 3:
            print("Not yet implemented")
        else:
            print("Invalid choice!")
        print("Do you want to try again? 1-Yes 2-No")
        choice = int(input())
        if choice == 1:
            print("Do you wanna use:")
            print("    1- Previous data")
            print("    2- Start of the beginning")
            choice = int(input())
            if choice == 2:
                knowledge_base = {}
                rules = {}
            clear()
            continue
        else:
            break


if __name__ == '__main__':
    main()

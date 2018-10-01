import re
import sys

curr_step = ""

def remove_var(string):
    string = string.replace("*x", '')
    return string


def remove_part(string, part):
    string = string.replace(part, '')
    return string


def remove_spaces(string):
    string = string.replace(" ", '')
    return string


def resolve_mult_div_regex(matchobj):
    matchobj = matchobj.group(0)
    # print(matchobj)
    matchobj = remove_var(matchobj)
    # print(matchobj)
    matchobj = eval(matchobj)
    # print(matchobj)
    matchobj = str(matchobj)
    # print(matchobj)
    matchobj = matchobj + "*x"
    # print(matchobj)
    return matchobj


def resolve_mult_div(eq, eq_other_side, print_order):
    regex_var_with_mult_div_op = r"(\d*(?:\*|\/)[a-zA-Z](?:(?:\/|\*)?\d+)+)"
    solution_step(eq, eq_other_side, print_order)
    while True:
        eq_sub = re.sub(regex_var_with_mult_div_op, resolve_mult_div_regex, eq, 1)
        if eq_sub == eq:
            break
        eq = eq_sub
        solution_step(eq, eq_other_side, print_order)

    return eq


def transform_negative(element):
    if element[0] == '+':
        element = '-' + element[1:]
    else:
        element = '+' + element[1:]
    return element


def find_var(eq_left, eq_right):
    regex_var = r"((?:\+|\-)?\d*(?:\*|\/)[a-zA-Z](?:(?:\/|\*)?\d+)*)"
    var_left = re.findall(regex_var, eq_left)
    var_right = re.findall(regex_var, eq_right)

    return var_left, var_right


def left_eq(eq_left, eq_right):
    regex_var = r"((?:\+|\-)?\d*(?:\*|\/)[a-zA-Z](?:(?:\/|\*)?\d+)*)"
    var_left, var_right = find_var(eq_left, eq_right)
    print(eq_left, "=", eq_right)

    for i in var_right:
        eq_right = re.sub(regex_var, lambda matchtobj: remove_or_leave(matchtobj, i), eq_right)
        i = transform_negative(i)
        eq_left = eq_left + i
        print(eq_left, "=", eq_right)

    return eq_left, eq_right


def find_const(eq_left, eq_right):
    regex_const = r"((?:\+|\-)\d+)(?!(\d*)(\*|\/)[a-zA-Z])"
    const_left = re.findall(regex_const, eq_left)
    const_right = re.findall(regex_const, eq_right)
    const_left = to_list(const_left)
    const_right = to_list(const_right)
    return const_left, const_right


def to_list(eq):
    eq = [i[0] for i in eq]
    return eq


def remove_or_leave(matchtobj, i):
    matchtobj = matchtobj.group(0)
    if matchtobj == i:
        oposite_i = transform_negative(i)
        print("adding (", oposite_i, ") to both sides")
        return ''
    return matchtobj


def append_plus_sign(eq):
    print("eq before: ", eq)
    if eq[0] != "+" and eq[0] != "-":
        eq = "+" + eq
    print("eq after: ", eq)
    return eq
    pass


def right_eq(eq_left, eq_right):
    eq_left = append_plus_sign(eq_left)
    eq_right = append_plus_sign(eq_right)
    regex_const = r"((?:\+|\-)\d+)(?!(\d*)(\*|\/)[a-zA-Z])"
    const_left, const_right = find_const(eq_left, eq_right)
    print(const_right, eq_right)

    for i in const_left:
        eq_left = re.sub(regex_const, lambda matchtobj: remove_or_leave(matchtobj, i), eq_left)
        i = transform_negative(i)
        eq_right = eq_right + i
        print(eq_left, "=", eq_right)

    const_left, const_right = find_const(eq_left, eq_right)
    const_left = ''.join(const_left)
    const_right = ''.join(const_right)
    new_eq_right = const_right + const_left
    return eq_left, new_eq_right


def make_mult_div(eq, eq_other_side, print_order):
    if "x" not in eq:
        return str(eval(eq))
    eq = separate_variables(eq)
    eq = resolve_mult_div(eq, eq_other_side, print_order)
    return eq


def remove_part(string, part, count=-1):
    string = string.replace(part, '', count)
    return string


def separate_variables(string):
    string = [i for i in re.split(r'([\d.]+|\W+)', string) if i]
    i = 0
    while i < len(string) - 1:
        if re.match(r'([a-zA-Z])', string[i + 1]) and not re.match(r'(\W+)', string[i]):
            string = string[:i + 1] + list("*") + string[i + 1:]
            i += 1
        i += 1
    string = ''.join(string)
    return string


def error(description=-1):
    message = "Something is wrong! Error undefined."
    if description == 1:
        message = "Some operation is generating a non-linear equation"
    print("ERROR!\n" + message)
    sys.exit(message)


def make_distributive(eq, operation, parenthesis):
    # regex_var = r"((?:\+|\-)?\d*)(?=\*[a-zA-Z])"
    value = eq
    eq_var = False
    if "*x" in value:
        value = remove_var(value)
        eq_var = True
    parenthesis_parts = parenthesis.split("+")
    if len(parenthesis_parts) > 1:
        if eq_var:
            error(1)  # generating a non-linear equation
        parenthesis_parts[0] = remove_var(parenthesis_parts[0])
        if operation == "*":
            first = float(value) * float(parenthesis_parts[0])
            second = float(value) * float(parenthesis_parts[1])
        else:
            first = float(value) / float(parenthesis_parts[0])
            second = float(value) / float(parenthesis_parts[1])

        result = str(int(first)) + "*x" + str(int(second))
    else:
        parenthesis_parts = parenthesis_parts[0]
        if "*x" in parenthesis_parts:
            if eq_var:
                error(1)  # generating a non-linear equation
            parenthesis_parts = remove_var(parenthesis_parts)
            if operation == "*":
                aux = float(value) * float(parenthesis_parts)
            else:
                aux = float(value) / float(parenthesis_parts)
            result = str(int(aux)) + "*x"
        else:
            if operation == "*":
                aux = float(value) * float(parenthesis_parts)
            else:
                aux = float(value) / float(parenthesis_parts)
            if eq_var:
                result = str(int(aux)) + "*x"
            else:
                result = str(int(aux))
    return result


def simplify_expression(expression):
    regex_var = r"((?:(?:\+|\-)?\d*(?:\*|\/))+[a-zA-Z](?:(?:\/|\*)?\d+)*)"
    equation1 = expression.group(1)
    operation = expression.group(2)
    equation2 = expression.group(3)

    if "(" in equation1:
        const = equation1
        var = re.findall(regex_var, equation1)
        for i in var:
            const = remove_part(const, i)
        if const != '':
            const = eval(const)
            const = str(const)
        if len(var) != 0:
            var = ''.join(var)
            var = remove_var(var)
            var = eval(var)
            var = str(var)
            var = var + "*x"
        if len(var) != 0 and len(const) != 0:
            equation1 = var + "+" + const
        elif len(var) != 0:
            equation1 = var
        elif len(const) != 0:
            equation1 = const
        var = re.findall(regex_var, equation2)
        if len(var) != 0:
            temp = ''.join(var)
            temp = remove_var(temp)
            temp = eval(temp)
            temp = str(temp)
            temp = temp + "*x"
        else:
            temp = eval(equation2)
            temp = str(temp)
        equation2 = temp
        equation = make_distributive(equation2, operation, equation1)
    else:
        const = equation2
        var = re.findall(regex_var, equation2)
        for i in var:
            const = remove_part(const, i)
        if len(const) != 0:
            const = eval(const)
            const = str(const)
        if len(var) != 0:
            var = ''.join(var)
            var = remove_var(var)
            var = eval(var)
            var = str(var)
            var = var + "*x"
        if len(var) != 0 and len(const) != 0:
            equation2 = var + "+" + const
        elif len(var) != 0:
            equation2 = var
        elif len(const) != 0:
            equation2 = const
        var = re.findall(regex_var, equation1)
        if len(var) != 0:
            temp = ''.join(var)
            temp = remove_var(temp)
            temp = eval(temp)
            temp = str(temp)
            temp = temp + "*x"
        else:
            temp = eval(equation1)
            temp = str(temp)
        equation1 = temp
        equation = make_distributive(equation1, operation, equation2)

    return equation


def solution_step(eq, eq_aux, print_order):
    if print_order == 1:
        step = eq + ' = ' + eq_aux
    else:
        step = eq_aux+ ' = ' + eq
    global curr_step
    if step != curr_step:
        #print("step cmp: ", step, "//", curr_step)
        print(step)
        curr_step = step
    return step


def solve_parentheses(eq, eq_other_side, print_order):
    regex_right_parentheses = r"(\-?(?:\d*\*[a-zA-Z](?:(?:\/|\*(?:\-)?)?\d+)*)*(?:(?:\*|\/(?:\-)?)?\d+)*)(\*|\/)(\((" \
                              r"?:(?:\+|\-)?\d*\*[a-zA-Z](?:(?:\/|\*(?:\-)?)?\d+)*)*(?:(?:\+|\-|\*|\/)?\d+)*\))"
    regex_left_parentheses = r"\(((?:(?:\+|\-)?\d*\*[a-zA-Z](?:(?:(?:\*|\/)(?:\-)?)?\d+)*)*(?:(" \
                             "?:\+|\-|\*|\/)?\d+)*)\)(\*|\/)((?:(?:(?:\-)?\d)*\*[a-zA-Z](?:(?:(?:\*|\/)(" \
                             "?:\-)?)?\d+)*)*(?:(?:\*|\/)?(?:\-)?\d+)*)"

    solution_step(eq, eq_other_side, print_order)
    while True:
        eq_sub = re.sub(regex_right_parentheses, simplify_expression, eq)
        if eq_sub == eq:
            break
        eq = eq_sub

        solution_step(eq, eq_other_side, print_order)
    while True:
        eq_sub = re.sub(regex_left_parentheses, simplify_expression, eq)
        if eq_sub == eq:
            break
        eq = eq_sub
        #print("3")
        solution_step(eq, eq_other_side, print_order)

    eq = remove_part(eq, "(", 1)
    eq = remove_part(eq, ")", 1)
    solution_step(eq, eq_other_side, print_order)
    return eq


def normalize_begin_eq(eq):
    if eq[0] != '-' and eq[0] != '+':
        eq = '+' + eq
    return eq


def parsing(eq_left, eq_right):
    print("Equation:", eq_left, "=", eq_right)
    print("Parentheses Solving:")
    eq_left = solve_parentheses(eq_left, eq_right, 1)
    eq_right = solve_parentheses(eq_right, eq_left, 0)
    eq_left = normalize_begin_eq(eq_left)
    eq_right = normalize_begin_eq(eq_right)

    print("Mult and Div and Sum of Constants:")
    eq_left = make_mult_div(eq_left, eq_right, 1)
    eq_right = make_mult_div(eq_right, eq_left, 0)

    print("Realocation:")
    new_left_eq, new_right_eq = left_eq(eq_left, eq_right)
    new_left_eq, new_right_eq = right_eq(new_left_eq, new_right_eq)
    new_left_eq = remove_var(new_left_eq)
    result_left = eval(new_left_eq)
    result_right = eval(new_right_eq)
    if result_left != 0:
        print("x = ", result_right / result_left)
    else:
        print("Does not have solution")
    print("")


def filter_eq(eq):
    eq = remove_spaces(eq)
    eq = separate_variables(eq)
    eq = eq.split('=')
    before_equals_eq = eq[0]
    after_equals_eq = eq[1]
    return before_equals_eq, after_equals_eq


def solve_linear_equation(eq):
    before_equals_eq, after_equals_eq = filter_eq(eq)
    parsing(before_equals_eq, after_equals_eq)


def get_input():
    equations = ["2x + 4 + (3x + 5x) = 5 + 4 - 4",
                 "((2+2)/2)*2+1x=1707", "((2+2)/2)*2+5*x/50=1707",
                 "(-1x)+5=(1x+2x)*-2*10/5*2+(2*(1+1*(5*0)))",
                 "1x + 2x * 3 + 4x * 2 * 3 + 4 = 2x*4*3+5x*2 - 4",
                 "2x - 4 + 2 - 3x - 5 + 6 = - 3 + 1 + 1x - 4x + 2 - 25 "]
    print("1- Predefined input")
    print("2- Custom input")
    choice = int(input())
    while True:
        if choice == 1:
            return equations
        elif choice == 2:
            print("Insert the equation to be solved:")
            return [input()]
        else:
            print("Invalid choice")


def main():
    equations = get_input()
    for eq in equations:
        solve_linear_equation(eq)


if __name__ == '__main__':
    main()
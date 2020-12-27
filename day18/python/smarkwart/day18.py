import sys

def get_input_data_as_list(file_name):
    """ 
    Reads in data from the given file and returns them as list
        with one entry per line and whitespaced trimmed 
    """
    with open(file_name) as input_file:
        #data_list = list(input_file.readlines())
        #data_list = list(map(list, input_file.readlines()))
        data_list = input_file.readlines()
        data_list = [str.strip(line) for line in data_list]
    return data_list

def calculate(value, operand, next_value):
    #print(f"\tOperation: {value} {operand} {next_value}")
    result = 0
    if operand == '+':
        result = value + next_value
    elif operand == '*':
        result = value * next_value
    return result

def evaluate(expression_string):
    expression_list = list(expression_string)
    expression_list.reverse()
    values = {}
    operands = {}
    level = 0
    #values[level] = 1
    #operands[level] = '*'
    while expression_list:
        char = expression_list.pop()
        #print(f"In: {char}")
        if char == ' ':
            pass
        elif char == '+' or char == '*':
            operands[level] = char
        elif char == '(':
            level += 1
        elif char == ')':
            level -= 1
            if level in operands and level in values:
                values[level] = calculate(values[level], operands[level], values[level+1])
            else:
                values[level] = values[level+1]
            del values[level+1]
            del operands[level+1]
            #print(f"\tVal: {values[level]}")
        else:
            if level in operands and level in values:
                values[level] = calculate(values[level], operands[level], int(char))
            else:
                values[level] = int(char)
            #print(f"\tVal: {values[level]}")
    return values[level]

def evaluate2(expression_string):
    expression_list = list(expression_string)
    expression_list.reverse()
    values = {0:[]}
    operands = {}
    level = 0
    #values[level] = 1
    #operands[level] = '*'
    while expression_list:
        char = expression_list.pop()
        #print(f"In: {char}")
        if char == ' ':
            pass
        elif char == '+' or char == '*':
            operands[level] = char
        elif char == '(':
            level += 1
            values[level] = []
        elif char == ')':
            #print(f"\tLvl: {level} Val: {values[level]}")
            level_result = 1
            for value in values[level]:
                level_result *= value
            level -= 1
            if level in operands and level in values:
                #values[level] = calculate(values[level], operands[level], values[level+1])
                if operands[level] == '+':
                    values[level][-1] = calculate(values[level][-1], operands[level], level_result)
                else:
                    values[level].append(level_result)
            else:
                values[level].append(level_result)
            del values[level+1]
            del operands[level+1]
        else:
            if level in operands and level in values:
                if operands[level] == '+':
                    values[level][-1] = calculate(values[level][-1], operands[level], int(char))
                else:
                    values[level].append(int(char))
            else:
                values[level].append(int(char))
            #print(f"\tVal: {values[level]}")
        #print(values)
        #print(operands)
    result = 1
    for value in values[0]:
        result *= value
    return result

homework = get_input_data_as_list(sys.argv[1])

print(f"Result: {evaluate2(homework[0])}")

results = []
for line, expression in enumerate(homework):
    results.append(evaluate2(expression))
    print(f"#{line}: {expression} = {results[-1]}")

print(f"The sum of all expressions is: {sum(results)}")

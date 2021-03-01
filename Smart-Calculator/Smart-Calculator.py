def multiply(number1, number2):
    return number1 * number2


def addition(number1, number2):
    return number1 + number2


def subtraction(number1, number2):
    return number1 - number2


def partition(number1, number2):
    return number1 / number2


def power(number1, number2):
    return number1**number2


def dell_to_spaces(operation):
    while True:
        if " " in operation:
            operation = operation.replace(" ", "")
        else:
            break
    return operation


def same_time_no(operation):
    if "--" in operation:
        return operation.replace("--", "+")
    if "+-" in operation:
        return operation.replace("+-", "-")
    if '-+' in operation:
        return operation.replace("-+", "-")
    else:
        return operation


# In here we are seperating the counts, then we are calculating
def calculate(operation, mode):
    first_count = ""
    second_count = ""
    if mode in operation:
        index = operation.find(mode)
        if index == 0 and mode == "-":  # For the special status about subtraction
            index = operation[1:].find(mode) + 1
        left_index = index
        right_index = index + 1
        # Left Side
        while 0 <= index:
            index -= 1
            if index == -1:
                if "." in operation[0:left_index]:  # For type of variables
                    first_count = float(operation[index + 1:left_index])
                    break
                elif mode == '/':  # That is special status for division
                    first_count = int(operation[index + 1:left_index])
                    break
                first_count = int(operation[index + 1:left_index])  # For normal operating about type
                break
            if operation[index] == '+' or operation[index] == '-' or operation[index] == '*' or operation[index] == '/'\
                    or operation[index] == '^':
                if operation[index - 1] == '+' or operation[index - 1] == '-' or operation[index - 1] == '*' or \
                        operation[index - 1] == '/' or operation[index - 1] == '^':
                    first_count = operation[index:left_index]
                    break
                elif index - 1 == -1:  # For if it finish in the most left
                    first_count = operation[index:left_index]
                    break
                first_count = operation[index + 1:left_index]
                break
        # Right Side
        index = right_index
        if operation[right_index] == "-" or operation[right_index] == "+":
            index += 1
        while index <= len(operation) - 1:
            if operation[index] == '+' or operation[index] == '-' or operation[index] == '*' or operation[index] == '/'\
                    or operation[index] == '^':
                second_count = operation[right_index:index]
                break
            else:
                second_count = operation[right_index:index + 1]
            index += 1
        # Result Side
        result = 0
        if mode == "*":
            result = multiply(float(first_count), float(second_count))
        elif mode == "/":
            result = partition(float(first_count), float(second_count))
        elif mode == "+":
            result = addition(float(first_count), float(second_count))
        elif mode == "-":
            result = subtraction(float(first_count), float(second_count))
        elif mode == "^":
            result = power(float(first_count), int(second_count))
        result = round(result, 2)
        operation = operation.replace(str(first_count)+mode+str(second_count), str(result))
        operation = same_time_no(operation)  # Little control
        print("=>", operation)  # For showing the operations step by step
        return operation


# If string has any brackets
def if_bracket(operation):
    if "(" in operation:
        bracket_findex = operation.find("(")
        first = bracket_findex
        bracket_lindex = operation.find(")")
        while 0 <= len(operation[bracket_findex:]):
            if "(" in operation[first:bracket_findex] and bracket_findex < bracket_lindex:
                first = bracket_findex
            if ")" in operation[first:bracket_findex]:
                bracket_findex = first
                break
            bracket_findex += 1
        control_operation1 = operation[bracket_findex:bracket_lindex]
        control_operation = operation[bracket_findex-1:bracket_lindex+1]
        print("=>", control_operation)
        result = operations(operation[bracket_findex:bracket_lindex])
        if "+" in result or "*" in result or "/" in result or "^" in result or "-" in result:
            if "-" in result:
                indexminus = result.find("-")
                if indexminus == 0:
                    operation = operation.replace(control_operation, result)
                    return operation
                else:
                    operation = operation.replace(control_operation1, result)
                    return operation
            else:
                operation = operation.replace(control_operation1, result)
                return operation
        else:
            operation = operation.replace(control_operation, result)
            return operation


# Operation Side
def operations(operation):
    control = 1
    while control != 0:
        try:
            if "^" in operation:
                operation = calculate(operation, "^")
                continue
            if '/' in operation:  # For process priority
                if '*' in operation:
                    index1 = operation.find("/")
                    index2 = operation.find("*")
                    if index1 < index2:
                        if "/" in operation:
                            operation = calculate(operation, "/")
                            continue
                        if "*" in operation:
                            operation = calculate(operation, "*")
                            continue
                        else:
                            if "/" in operation:
                                operation = calculate(operation, "/")
                                continue
                            if "*" in operation:
                                operation = calculate(operation, "*")
                                continue
            if "*" in operation:
                operation = calculate(operation, "*")
                continue
            if "/" in operation:
                operation = calculate(operation, "/")
                continue
            if '+' in operation:  # For operation priority
                if '-' in operation:
                    index1 = operation.find("-")
                    index2 = operation.find("+")
                    if index1 < index2:
                        if "-" in operation and index1 != 0:
                            operation = calculate(operation, "-")
                            continue
                        if "+" in operation:
                            operation = calculate(operation, "+")
                            continue
                        else:
                            if "+" in operation:
                                operation = calculate(operation, "+")
                                continue
                            if "-" in operation:
                                operation = calculate(operation, "-")
                                continue
            if "+" in operation:
                operation = calculate(operation, "+")
                continue
            elif "-" in operation:
                operation = calculate(operation, "-")
            else:
                break
        except ValueError:
            break
    return operation


# Main Side
print("----My Calculator----\n#You can enter float or integer number about operating.\n#You can enter positive or "
      "negative numbers.\n#You can enter with space.\n#You can use power operation.\n#You can use brackets in your"
      " operations.\n#Example -4+-4/2*2-3*2^2 .\n#Example 2+4*(12/4)^2-5*-2 .\n")
temp = 2
control = 1
while temp != 0:
    control = 1
    operation = input('Write a operation: ')
    operation = dell_to_spaces(operation)
    operation_control = operation
    print("Solution: ")
    print("=>", operation)
    while control != 0:
        if operation[len(operation)-1] == "-" or operation[len(operation)-1] == "+" \
                or operation[len(operation)-1] == "*" or operation[len(operation)-1] == "/":
            break
        if "(" in operation:
            operation = if_bracket(operation)
            print("=>", operation)
            continue
        else:
            pass
        operation = operations(operation)
        control = 0
    if operation == operation_control:
        print('Please enter a correct operation!\n')
    else:
        print("Result =", operation)
        while True:  # For controlling the step(continue or finish)
            try:
                temp = int(input('\nPress 1 to calculate another operation;\nPress 0 to end of the program;\nAnswer:'))
            except ValueError:
                temp = 3
                pass
            if temp == 1 or temp == 0:
                print('')
                break
            else:
                print("Please enter the correct number!")
print("The program is closed!")

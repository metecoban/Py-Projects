def calculate(pol1, pol2, operation_type):
    c_result = []
    for i in pol1:
        c_result.append(i)
    if operation_type == "-":
        pol2 = subtraction(pol2)
    for i in pol2:
        c_result.append(i)
    for i in range(len(c_result)):
        j = i + 1
        while j < len(c_result):
            if c_result[i][1] == c_result[j][1]:
                c_result[i][0] = c_result[i][0] + c_result[j][0]
                c_result.remove(c_result[j])
                j -= 1
            j += 1
    return c_result


def subtraction(pol):
    for i in range(len(pol)):
        pol[i][0] = pol[i][0] * -1
    return pol


def combining(pol):
    string = ""
    pol = placement(pol)
    if pol[(len(pol) - 1)][0] == 0:
        rotation_type = len(pol) - 1
    else:
        rotation_type = len(pol)
    for i in range(rotation_type):
        if (pol[i][0] == 0 and pol[i][1] == 0) or (pol[i][0] == 0 and pol[i][1] != 0):
            pass
        else:
            if pol[i][1] == 0:
                string += str(pol[i][0])
            else:
                string += str(pol[i][0]) + "x" + "^" + str(pol[i][1])
        if i < len(pol) - 1 and pol[i + 1][0] > 0:
            string += "+"
    return string


def placement(pol):
    n = len(pol)
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if pol[j][1] < pol[j + 1][1]:
                pol[j], pol[j + 1] = pol[j + 1], pol[j]
    return pol


def delete_unnecessary(string):
    while True:
        if " " in string:
            string = string.replace(" ", "")
        if "*" in string:
            string = string.replace("*", "")
        if not (" " in string or "*" in string):
            break
    return string


def separate(pol):
    pol = delete_unnecessary(pol)
    index = pol.count("x") + 1
    s_result = []
    if index == 1:
        s_result.append([int(pol), 0])
    else:
        s_result = [[0] * 2 for i in range(index)]
        value1 = 0
        value2 = 0
        while True:
            left_index = 0
            temp = pol.find("x")
            index = temp
            # Left Side
            if index == 0:
                s_result[value1][value2] = 1
            elif pol[index-1] == "+":
                s_result[value1][value2] = 1
                left_index = index - 1
            elif pol[index-1] == "-":
                s_result[value1][value2] = -1
                left_index = index - 1
            else:
                while index != 0:
                    index -= 1
                    left_index = index
                    if pol[index] == "+" or pol[index] == "-":
                        left_index = index
                        break
                s_result[value1][value2] = int(pol[left_index:temp])
            index = temp + 1
            value2 = 1
            # Right Side
            if len(pol) == index:
                index -= 1
            if pol[index] != "^":
                s_result[value1][value2] = 1
                if index+1 == len(pol):
                    index += 1
            else:
                index += 1
                right_index = index
                while index < len(pol)-1:
                    index += 1
                    if pol[index] == "-" or pol[index] == "+":
                        break
                if not index < len(pol) - 1:
                    index += 1
                    s_result[value1][value2] = int(pol[right_index:index])
                else:
                    s_result[value1][value2] = int(pol[right_index:index])
                if s_result[value1][value2] < 0:
                    print("Entered invalid polynomial. Degree of x must be natural number in polynomial.")
                    exit(0)
            pol = pol.replace(pol[left_index:index], "")
            value1 += 1
            value2 = 0
            if "x" not in pol:
                if "" != pol:
                    s_result[value1][value2] = int(pol)
                break
    return s_result


# -----Test Side-----
print("-----Addition  and Subtraction Program About Polynomial-----\n# Enter both polynomials in one line."
      "\n# When writing the polynomial, do not use expressions such as periods, commas, brackets. "
      "\n# When you use it, the program will display an error message and close.\n# Example of inputs: "
      "\n#   First Polynomial: 4x^5+2x^3-5x+4 \n#   Second Polynomial: 3x^3+4x+5 "
      "\n#   Enter + for adding, enter - for subtracting: +\n#   Result: 4x^5+5x^3-1x^1+9\n")
first_pol = input('First Polynomial: ')
second_pol = input('Second Polynomial: ')
decision = input('Enter + for adding, enter - for subtracting: ')
try:
    first = separate(delete_unnecessary(first_pol))
    second = separate(delete_unnecessary(second_pol))
    if decision == "+":
        result = calculate(first, second, "+")
        print("\nResult: " + combining(result))
    elif decision == "-":
        result = calculate(first, second, "-")
        print("\nResult: " + combining(result))
    else:
        print("Entered invalid value. Only enter + or -.")
except (ValueError, IndexError, Exception):
    print("Entered invalid polynomial. Please enter a valid polynomial.")

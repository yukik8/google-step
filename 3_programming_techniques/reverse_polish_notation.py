#! /usr/bin/python3

def read_number(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal
            decimal /= 10
            index += 1
    return number, index


def calculate(operation, left, right):
    if operation in ('+', '-', '*', '/'):
        if operation == '+':
            ans = left + right
        elif operation == '-':
            ans = left - right
        elif operation == '*':
            ans = left * right
        elif operation == '/':
            ans = left / right
    else:
        print('Invalid character found: ' + operation)
        exit(1)
    return ans


# 操車場アルゴリズム
def shunting_yard_algorithm(line):
    stack = []
    num_queue = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (num, index) = read_number(line, index)
            num_queue.append(num)
        elif line[index] in ('+', '-', '*', '/', '(', 'a', 'i', 'r'):
            stack.append(line[index])
            if line[index] in ('a', 'i'):
                index += 2
            if line[index] == 'r':
                index += 4
            index += 1
        elif line[index] == ')':
            while stack:
                operation = stack.pop()
                if operation == '(':
                    break
                num_queue.append(operation)
            index += 1
    while stack:
        num_queue.append(stack.pop())
    return num_queue


def evaluate(stack):
    result_stack = []
    index = 0
    length = len(stack)
    while index < length:
        print(result_stack)
        if type(stack[index]) in (int, float):
            result_stack.append(stack[index])
        if stack[index] in ('+', '-', '*', '/'):
            b = result_stack.pop()
            a = result_stack.pop()
            result_stack.append(calculate(stack[index], a, b))
        elif stack[index] in ('a', 'i', 'r'):
            a = result_stack.pop()
            if stack[index] == 'a':
                result_stack.append(abs(a))
                index += 2
            elif stack[index] == 'i':
                result_stack.append(int(a))
                index += 2
            elif stack[index] == 'r':
                result_stack.append(round(a))
                index += 4
        index += 1
        print(result_stack[0], index)
    return result_stack[0]


def test(line):
    stack = shunting_yard_algorithm(line)
    print("num_queue:", stack)
    actual_answer = evaluate(stack)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" %
              (line, expected_answer, actual_answer))


# Add more tests to this function :)
def run_test():
    print("==== Test started! ====")
    test("1+2")
    test("1.0+2.1-3")

    test("2*3")  # かけ算
    test("2/3")  # 割り算
    test("2.1*3.3")  # 小数のかけ算
    test("2.1/3.3")  # 小数の割り算
    test("8.0+3*0.7+0.4")  # 掛け算を優先
    test("8.0+3/0.7+0.4")  # 割り算を優先
    test("8.0+3*0.7/0.4")  # 連続して掛け算と割り算
    test("-9+2")  # マイナス
    test("5.5*0")  # ０の掛け算
    # test("5.5/0")  # ０の割り算

    test("8.0+3*(0.7+0.4)")  # かっこの含まれる計算
    test("(3.0+4*(2-1))/5")  # 二重かっこの含まれる計算

    test("8.0+3*abs(-0.7+0.4)")  # absの含まれる計算
    test("8.0+3*int(1.1+0.4)")  # intの含まれる計算
    test("8.0+3*round(1.1+0.4)")  # roundの含まれる計算

    print("==== Test finished! ====\n")


run_test()

while True:
    print('> ', end="")
    line = input()
    nums, stack = shunting_yard_algorithm(line)
    answer = evaluate(nums, stack)
    print("answer = %f\n" % answer)

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


def calculate(operation, left, right, index):
    if operation in ('+', '-', '*', '/'):
        if operation == '+':
            ans = left + right
        elif operation == '-':
            ans = left - right
        elif operation == '*':
            ans = left * right
        elif operation == '/':
            ans = left / right
    elif operation == 'a':
        ans = abs(right)
        index += 2
    elif operation == 'i':
        ans = int(right)
        index += 2
    elif operation == 'r':
        ans = round(right)
        index += 4
    else:
        print('Invalid character found: ' + operation)
        exit(1)
    return ans, index


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
        elif line[index] == ')':
            operation = []
            while 1:
                operation.append(stack.pop())
                if operation[-1] == '(':
                    operation.pop()
                    right = num_queue.pop()
                    current_operation = operation.pop()
                    if current_operation in ('+', '-', '*', '/'):
                        left = num_queue.pop()
                        ans, index = calculate(
                            current_operation, left, right, index)
                    elif current_operation in ('a', 'i', 'r'):
                        ans, index = calculate(
                            current_operation, None, right, index)
                    else:
                        print('Invalid character found: ' + line[index])
                        exit(1)
                    num_queue.append(ans)
        index += 1
    while stack:
        num_queue.append(stack.pop())
    return num_queue, stack


def evaluate(nums, stack):
    result_stack = []
    for token in nums:
        if isinstance(token, float):
            result_stack.append(token)
        elif token in ('+', '-', '*', '/'):
            b = result_stack.pop()
            a = result_stack.pop()
            ans, _ = calculate(token, a, b, 0)
            result_stack.append(ans)
        elif token in ('a', 'i', 'r'):
            a = result_stack.pop()
            ans, _ = calculate(token, None, a, 0)
            result_stack.append(ans)
    return result_stack[0]


def test(line):
    nums, stack = shunting_yard_algorithm(line)
    print("num_queue:", nums)
    actual_answer = evaluate(nums, stack)
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

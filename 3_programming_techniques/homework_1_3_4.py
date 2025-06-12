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
    token = {'type': 'NUMBER', 'number': number}
    return token, index


def read_plus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1


def read_minus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1


def read_times(line, index):
    token = {'type': 'TIMES'}
    return token, index + 1


def read_division(line, index):
    token = {'type': 'DIVISION'}
    return token, index + 1


def read_left_parenthesis(line, index):
    token = {'type': 'LEFT'}
    return token, index + 1


def read_right_parenthesis(line, index):
    token = {'type': 'RIGHT'}
    return token, index + 1


def read_abs(line, index):
    token = {'type': 'ABS'}
    return token, index + 3


def read_int(line, index):
    token = {'type': 'INT'}
    return token, index + 3


def read_round(line, index):
    token = {'type': 'ROUND'}
    return token, index + 5


def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = read_number(line, index)
        elif line[index] == '+':
            (token, index) = read_plus(line, index)
        elif line[index] == '-':
            (token, index) = read_minus(line, index)
        elif line[index] == '*':
            (token, index) = read_times(line, index)
        elif line[index] == '/':
            (token, index) = read_division(line, index)
        elif line[index] == '(':
            (token, index) = read_left_parenthesis(line, index)
        elif line[index] == ')':
            (token, index) = read_right_parenthesis(line, index)
        elif line[index] == 'a':
            (token, index) = read_abs(line, index)
        elif line[index] == 'i':
            (token, index) = read_int(line, index)
        elif line[index] == 'r':
            (token, index) = read_round(line, index)
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens


def evaluate(tokens):
    answer = 0
    tokens.insert(0, {'type': 'PLUS'})  # Insert a dummy '+' token
    index = 1
    while index < len(tokens):
        # かっこの中を再帰的に計算
        if tokens[index]['type'] == 'LEFT':
            right_index = find_right_parenthesis(tokens, index)
            paren_result = evaluate(tokens[index + 1:right_index])
            tokens[index:right_index +
                   1] = [{'type': 'NUMBER', 'number': paren_result}]
        # abs, int, roundの計算
        elif tokens[index]['type'] in ('ABS', 'INT', 'ROUND'):
            right_index = find_right_parenthesis(tokens, index + 1)
            inside_func = evaluate(tokens[index + 2:right_index])
            if tokens[index]['type'] == 'ABS':
                func_result = abs(inside_func)
            elif tokens[index]['type'] == 'INT':
                func_result = int(inside_func)
            else:
                func_result = round(inside_func)
            tokens[index:right_index +
                   1] = [{'type': 'NUMBER', 'number': func_result}]
        else:
            index += 1
    index = 1
    # 掛け算と割り算を優先的に計算
    while index < len(tokens):
        if tokens[index]['type'] == 'TIMES' or tokens[index]['type'] == 'DIVISION':
            left = tokens[index - 1]['number']
            right = tokens[index + 1]['number']
            if tokens[index]['type'] == 'TIMES':
                result = left * right
            else:
                if right == 0:
                    raise ValueError('Division by zero')
                result = left / right
            tokens[index - 1:index +
                   2] = [{'type': 'NUMBER', 'number': result}]
        else:
            index += 1
    index = 1
    # 足し算と引き算を計算
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
            else:
                print('Invalid syntax')
                exit(1)
        index += 1
    return answer


def find_right_parenthesis(tokens, index):  # 閉じかっこのindexを検索
    depth = 0
    for i in range(index, len(tokens)):
        if tokens[i]['type'] == 'LEFT':
            depth += 1
        elif tokens[i]['type'] == 'RIGHT':
            depth -= 1
            if depth == 0:
                return i
    raise ValueError('Unmatched parenthesis')


def test(line):
    tokens = tokenize(line)
    actual_answer = evaluate(tokens)
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
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)

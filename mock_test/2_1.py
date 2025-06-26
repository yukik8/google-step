# 問題2
# ランレングス圧縮された文字列が与えられたとき、それを復元する関数を書いてください。

# input : “a2b1” -> “aab”
#         “a10b12” -> “aaaaaaaaaabbbbbbbbbbbb”
# 必ずアルファベットのあとに数字が来るとする

# isNumber(letter) -> letter 0 ~ 9 -> true, else -> false

# answer = “”
# answer += “a”

def isNumber(num):
    return num in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


def reverse_run_length_long(s):
    answer = []
    i = 0
    while i < len(s):
        print(i, s[i], len(s))
        if not isNumber(s[i]):
            number = []
            times = 0
            alphabet_index = i
            for j in range(alphabet_index + 1, len(s) + 1, 1):
                if j >= len(s) or not isNumber(s[j]):
                    number.reverse()
                    for index in range(len(number)):
                        times += int(number[index]) * (10 ** index)
                    for _ in range(times):
                        answer.append(s[alphabet_index])
                    break
                else:
                    number.append(s[j])
            i = j
    return ''.join(answer)


print(reverse_run_length_long('a10B2b3C4d4'))

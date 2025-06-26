# Input: アルファベットで構成された文字列
# 入力の文字列に含まれるのは小文字か大文字のアルファベットのみ
# “aaaBBbbbCCCCdddd” N

# “aaabbb1cc55d” -> ? “11”

# ランレングス圧縮してほしい

# Output: “a3B2b3C4d4”

# “aab” -> “a2b1”

# 10 “10”

def run_length(s):
    answer = []
    former = 0
    count = 1
    for letter in s:
        if former == letter:
            count += 1
        elif former != letter and former != 0:
            answer.append(former)
            answer.append(str(count))
            count = 1
        former = letter
    answer.append(former)
    answer.append(str(count))
    return ''.join(answer)

# 計算量: O(N)


print(run_length('aaaBBbbbCCCCdddd'))

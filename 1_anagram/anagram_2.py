# 最も高いスコアを持つanagramを返す
def find_anagram(random_word, dictionary):
    sorted_word_to_score = {}
    target_count = letter_count(random_word)
    # 文字の出現回数をカウント
    for word in dictionary:
        # sub anagram に当てはまるもののみを保存
        if is_sub_anagram(letter_count(word), target_count):
            sorted_word = ''.join(sorted(word))
            # スコアが同じsorted_word内で1番高い場合のみsorted_word_to_scoreに格納
            if (sorted_word not in sorted_word_to_score) or (calculate_score(word) > sorted_word_to_score[sorted_word][1]):
                sorted_word_to_score[sorted_word]= (word, calculate_score(word))
    # sub_anagramの中で1番高いスコアを持つwordを返す
    if sorted_word_to_score:
        print(max(sorted_word_to_score.values(), key=lambda x: x[1])[0])
        return max(sorted_word_to_score.values(), key=lambda x: x[1])[0]
    else:
        raise ValueError(f"No anagrams found for '{random_word}'")


# 答えをファイルに出力
def generate_anagram_file(input, output, dictionary):
    # 辞書ファイルをここで読み込む
    with open(dictionary, 'r') as file:
        dictionary=[line.strip() for line in file]
    with open(input, 'r') as fin, open(output, 'w') as fout:
        for line in fin:
            random_word=line.strip()
            try:
                answer=find_anagram(random_word, dictionary)
                fout.write(answer + "\n")
            except ValueError:
                fout.write("\n")


SCORES=[1, 3, 2, 2, 1, 3, 3, 1, 1, 4, 4, 2,
    2, 1, 1, 3, 4, 1, 1, 1, 2, 3, 3, 4, 3, 4]



# スコアを返す                                                                   
def calculate_score(word):
    score = 0
    for character in list(word):
        score += SCORES[ord(character) - ord('a')]
    return score

# 各文字の出現回数をカウントしたリストを返す
def letter_count(word):
    count = [0] * 26
    for letter in list(word.strip()):
        count[ord(letter) - ord('a')] += 1
    return count

# sub anagramであるかどうかを確認する
def is_sub_anagram(word_count, target_count):
    for i in range(26):
        if word_count[i] > target_count[i]:
            return False
    return True



if __name__ == "__main__":
    generate_anagram_file("1_anagram/large.txt",
                  "1_anagram/large_answer.txt", "1_anagram/words.txt")






















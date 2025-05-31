from collections import defaultdict


def find_anagram(path, random_word):
    # ファイルを読み込む
    with open(path, 'r') as file:
        # 改行を除いた辞書のリストを作成
        dictionary = [line.strip() for line in file]
    # 辞書内の全ての単語をソートした新たな辞書sorted_word_to_anagramsを作成する
    sorted_word_to_anagrams = defaultdict(list)
    for word in dictionary:
        key = ''.join(sorted(word))
        sorted_word_to_anagrams[key].append(word)
    # ターゲットの単語をソートしてsorted_word_to_anagramsの中で検索
    sorted_word = ''.join(sorted(random_word))
    if sorted_word in sorted_word_to_anagrams:
        return sorted_word_to_anagrams[sorted_word]
    else:
        raise ValueError(f"No anagrams found for '{random_word}'")

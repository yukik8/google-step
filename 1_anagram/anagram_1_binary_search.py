from collections import defaultdict


def find_anagram(path, random_word):
    with open(path, 'r') as file:
        # 改行を除いた辞書のリストを作成
        dictionary = [line.strip() for line in file]
    new_dictionary = defaultdict(list)
    # 辞書内の単語をソートした新しい辞書を作成
    for word in dictionary:
        new_dictionary[''.join(sorted(word))].append(word)
    # 新しい辞書をソート
    sorted_dict_keys = sorted(new_dictionary.keys())
    # random_word
    sorted_word = ''.join(sorted(random_word))
    # ソートした辞書をめぐる式二分探索で解く
    ok = len(sorted_dict_keys) - 1
    ng = -1
    while abs(ok - ng) > 1:
        mid = (ok + ng) // 2
        if sorted_word <= sorted_dict_keys[mid]:
            ok = mid
        else:
            ng = mid
    if sorted_word == sorted_dict_keys[ok]:
        return new_dictionary[sorted_dict_keys[ok]]
    else:
        raise ValueError(f"No anagrams found for '{random_word}'")
